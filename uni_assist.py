from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEndpointEmbeddings, ChatHuggingFace, HuggingFaceEndpoint
from langchain_community.vectorstores import FAISS
from langchain_core.tools.retriever import create_retriever_tool
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3

load_dotenv()

# ************************************ Data Indexing ******************************************

# Document Loader

PATH = 'porspectus.pdf'

loader = PyPDFLoader(PATH)
docs = loader.load()

# Text Splitter
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunked_docs = splitter.split_documents(docs)

# Embedding Model
embedding_model = HuggingFaceEndpointEmbeddings(repo_id='sentence-transformers/all-MiniLM-L6-v2')

# Vector Store
vector_store = FAISS.from_documents(chunked_docs, embedding_model)

# ********************************************* Components ******************************************

# Retriever 
retriever = vector_store.as_retriever(search_type='similarity', search_kwargs={'k':3})

# Retriever Tool
retriever_tool = create_retriever_tool(
    retriever=retriever,
    name='University Information retriever',
    description="Use this tool to look up factual information from the university prospectus, "
        "such as admission criteria, fee details, programs, and contact info."
)

# LLM Model
llm = HuggingFaceEndpoint(repo_id='Qwen/Qwen3-4B-Instruct-2507')

model = ChatHuggingFace(llm=llm)
model_with_tools = model.bind_tools([retriever_tool])

# **************************************************** Agent ***********************************

# Chat Node
def chat_node(state: MessagesState):
    
    template = (
        '''
    You are a helpful Assistant Chatbot of a University.
    Answer the question to the point from the user according to the provided context.
    if you have not enough infomration, or the question is irrelevant to your role just reply with a short sentence formal message.
        '''
    )

    messages = [SystemMessage(content=template)] + state['messages']
    response = model_with_tools.invoke(messages)

    return {'messages': [response]}

# Tool Node
tool_node = ToolNode([retriever_tool])

# create database
conn = sqlite3.connect('uni_assist.db', check_same_thread=False)

# Graph
checkpointer = SqliteSaver(conn=conn)

graph = StateGraph(MessagesState)

graph.add_node('chat_node', chat_node)
graph.add_node('tools', tool_node)

graph.add_edge(START, 'chat_node')
graph.add_conditional_edges('chat_node', tools_condition)
graph.add_edge('tools', 'chat_node')

chatbot = graph.compile(checkpointer=checkpointer)

def return_threads():
    all_threads = set()

    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])

    if not all_threads:
        return []
    else:
        return [all_threads]