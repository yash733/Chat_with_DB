from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama
import streamlit as st
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class Model:          
    def groq(self):
        model = ChatGroq(api_key= st.session_state.user.get('api'), model = st.session_state.user.get('model_type'))
        return model
    
    def ollama(self):
        model = ChatOllama(model = st.session_state.user.get('model_type'))
        return model