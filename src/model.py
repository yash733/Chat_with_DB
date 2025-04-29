from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama
import streamlit as st

class Model:          
    def groq(self):
        model = ChatGroq(api_key= st.session_state.user['api'], model = st.session_state.user['model_type'])
        return model
    
    def ollama(self):
        model = ChatOllama(model = st.session_state.user['model_type'])
        return model