# 🧠 University Assistant – Agentic RAG Chatbot (LangGraph + Streamlit)

Uni-Assist is an intelligent university assistant built using LangGraph, LangChain, and Streamlit.
It uses Retrieval-Augmented Generation (RAG) to answer student queries from the university prospectus in real time.

## 🚀 Features

📄 Loads and indexes PDF documents using FAISS vector store

🔍 Retrieves relevant context using Retriever Tool

🤖 Uses Qwen-3-4B-Instruct LLM via HuggingFace Endpoint

💬 Interactive Streamlit chat interface with typewriter-style streaming feature

🧩 Conversation Memory

✅ Resume old conversations using Resume Chat feature

## 🧰 Tech Stack

Frontend	Streamlit

Backend	LangGraph + LangChain

LLM	Qwen/Qwen3-4B-Instruct-2507 (HuggingFace Endpoint)

Embeddings	sentence-transformers/all-MiniLM-L6-v2

Vector Store	FAISS

Document Loader	PyPDFLoader

## 📦 Project Structure
UNI_ASSIST/
│

├── frontend_uni_assist.py    # Streamlit UI

├── uni_assist.py             # RAG + Agent logic (LangGraph pipeline)

├── porspectus.pdf            # Knowledge base

├── .env                      # HuggingFace API keys

└── README.md                 # Project documentation

## ⚙️ How to Run

### Clone the project

git clone https://github.com/abbas-cs/University-Chatbot-Assistant.git
cd uni-assist


### Create and activate virtual environment

python -m venv venv
source venv/bin/activate       # On Windows: venv\Scripts\activate


### Install dependencies

pip install -r requirements.txt


Add environment variables
Create a .env file:

HUGGINGFACEHUB_API_TOKEN=your_api_key_here


### Run the Streamlit app

streamlit run frontend_uni_assist.py


Open in browser: http://localhost:8501

## 🧑‍💻 Usage

Upload or point to your university’s PDF prospectus in uni_assist.py.

Ask questions like:

“What are the admission requirements for BS Computer Science?”
“Who is the Vice Chancellor?”

Chat threads persist during runtime and appear in the sidebar once a message is sent.

## 🧩 Key Improvements

Typewriter streaming output using st.write_stream

Filtered output (only AI messages, no retriever context)

Safe handling of empty chat sessions and missing keys

Memory management using SqliteSaver


Integrate cloud-based persistent checkpoint storage

Support multiple document uploads
