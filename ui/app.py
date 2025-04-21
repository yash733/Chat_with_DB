import streamlit as st
from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama
from langchain.sql_database import SQLDatabase
from langchain.agents import create_sql_agent
from langchain.callbacks import StreamlitCallbackHandler
from langchain.agents.agent_types import AgentType
import sqlite3
from pathlib import Path

from config import Config
config = Config()

st.title(config.get_title())
