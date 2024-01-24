
#install python-dotenv package and then create a .env file where you can add your api key and then 
#import the same using following coommands. 

import streamlit as st
from dotenv import dotenv_values
import openai 
import os
import openai
from llama_index.llms import OpenAI
import pypdf
from llama_index import VectorStoreIndex, SimpleDirectoryReader
from llama_index import ServiceContext, set_global_service_context 
from dotenv import dotenv_values
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]


llm = OpenAI(model="gpt-3.5-turbo", temperature=0.2,chunk_size=1000, chunk_overlap=100)

st.set_page_config(page_title="Chat Geeta, powered by LlamaIndex", page_icon="🕉️", layout="centered", initial_sidebar_state="auto", menu_items=None)
color = "#ff9933"
st.markdown(f' <h1 style="color:{color};"> Chat with Geeta </h1>', unsafe_allow_html=True)



if "messages" not in st.session_state.keys(): # Initialize the chat messages history
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask me a question from Geeta"}
    ]

@st.cache_resource(show_spinner=False)
def load_data():
    with st.spinner(text="Initializing...hang tight! This should take 1-2 minutes."):
        docs = SimpleDirectoryReader("data").load_data()
        llm = OpenAI(model="gpt-3.5-turbo", temperature=0.2)
        service_context = ServiceContext.from_defaults(llm =llm,chunk_size=1000, chunk_overlap=100,system_prompt="You are a guide and here to help, be calm and positive, be polite to the user")
        index = VectorStoreIndex.from_documents(docs, servicecontext=service_context)
        return index

index = load_data()

if "chat_engine" not in st.session_state.keys(): # Initialize the chat engine
        st.session_state.chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)

if prompt := st.chat_input("Your question"): # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages: # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.chat_engine.chat(prompt)
            st.write(response.response)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message) # Add response to message history