import streamlit as st
from uni_assist import chatbot, return_threads
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
import uuid


st.title('Uni Assistant')

# ************************************ Utility functions ***************************************

def generate_thread_id():
    thread_id = uuid.uuid4()
    return thread_id

def reset_chat():
    if st.session_state['messages_history']:
        thread_id = generate_thread_id()
        st.session_state['thread_id'] = thread_id
        add_thread(st.session_state['thread_id'])
        st.session_state['messages_history'] = []

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def load_conversations(thread_id):
    return chatbot.get_state(config={'configurable': {'thread_id': thread_id}}).values['messages']


# ************************************** Session State *****************************************

if 'messages_history' not in st.session_state:
    st.session_state['messages_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = return_threads()

add_thread(st.session_state['thread_id'])
    

# *********************************************** Sidebar **********************************

with st.sidebar:

    st.title('Uni Assist')

    if st.button('New Chat'):
        reset_chat()

    st.title('My Conversations')

    for thread_id in st.session_state['chat_threads']:
        if st.button(str(thread_id)):
            st.session_state['thread_id'] = thread_id
            messages = load_conversations(thread_id)

            temp_messages = []

            for msg in messages:

                if isinstance(msg, HumanMessage):
                    role='user'
                else:
                    role='assistant'
                
                temp_messages.append({'role': role, 'content': msg.content})
            
            st.session_state['messages_history'] = temp_messages

# ********************************************** Main UI ********************************************

for message in st.session_state['messages_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

user_input = st.chat_input('Type here')

if user_input:

    st.session_state['messages_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)

    config = {'configurable': {'thread_id': st.session_state['thread_id']}}

    with st.chat_message('ai'):

        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
                {'messages': [HumanMessage(content=user_input)]},
                config = config,
                stream_mode='messages'
                )
                if isinstance(message_chunk, AIMessage)
        )
    
    st.session_state['messages_history'].append({'role': 'assistant', 'content': ai_message})