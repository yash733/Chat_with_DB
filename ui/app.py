import streamlit as st
from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama
from langchain.sql_database import SQLDatabase
from langchain.agents import create_sql_agent
from langchain.callbacks import StreamlitCallbackHandler
from langchain.agents.agent_types import AgentType
import sqlite3
from sqlalchemy import create_engine
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
import os

from config import Config
config = Config()

st.title(config.get_title())

if 'user' not in st.session_state:
    st.session_state.user = {}

# ----- Input ----- #
db_selected = st.sidebar.radio(label='Choose DataBase to work with', options= config.get_radio_option())

if db_selected:
    # ----- DataBase Data ----- #
    if db_selected == 'Use SqlLight 3 DataBase- student.db':
        database_ = 'Local_DB'
        
    else:
        database_ = 'MySql_DB'
        with st.sidebar:
            my_sql_host = st.text_input(label='Provide MySQL Host')
            my_sql_db = st.text_input(label='MySql DataBase')
            my_sql_user = st.text_input(label='User name')
            my_sql_pass = st.text_input(label='MySql Password: ', type= 'password')
    
else: 
    st.error('Kindly select a database to work with.')
    st.rerun()

# ----- LLM MODEL ----- #
with st.sidebar:
    model = st.selectbox(label='Choose LLM model', options= config.get_model())
    if model == 'Groq':
        api = st.text_input(label= 'api key', type= 'password', value='')
        model_type = st.selectbox(label= 'Model Type', options= config.get_groq_model())
        button = False
        if api and button == False and st.button(label= 'Save', key= 'Groq') :
            button = True
            st.session_state.user.update({'model': model, 'model_type': model_type, 'api' : api})

    else:
        model_type = st.selectbox(label= 'Model Type', options= config.get_ollama_model())
        button = False
        if button == False:
            st.session_state.user.update({'model': 'Ollama', 'model_type': model_type})
            button == True

# ----- LLM ----- #
from model import Model

if st.session_state.user['model']:
    model = Model().groq()
else:
    model = Model().ollama()

# ----- database connection -----#
@st.cache_resource(ttl='1h')
def db_config(database_, my_sql_host = None, my_sql_db = None, my_sql_user = None, my_sql_pass = None):
    if database_ == 'Local_DB':
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'../student.db')
        creator = sqlite3.connect(f'file:{db_path}?mode=ro', uri = True) # uri open advance function like read-only, read-write, read-write-create
        return SQLDatabase(create_engine('sqlite:///',creator=creator))
        """'sqlite:///' → Tells SQLAlchemy:
        'Use the SQLite driver, and I’ll provide the connection via other means.'"""

    elif database_ == 'MySql_DB':
        if not (my_sql_host, my_sql_db, my_sql_user, my_sql_pass):
            st.error('Kindly provide all the details inorder to connect with MySQL DataBase')
            st.stop()
        return SQLDatabase(create_engine(f"mysql+mysqlconnector://{my_sql_user}:{my_sql_pass}@{my_sql_host}/{my_sql_db}"))
       
if database_ == 'Local_DB':
    db = db_config(database_)

elif database_ == 'MySql_DB':
    db = db_config(my_sql_host, my_sql_db, my_sql_user, my_sql_pass)

# ----- Toolkit ----- # calling multiple tools managing sql fucntions
tollkit = SQLDatabaseToolkit(llm = model, db = db)

agent = create_sql_agent(
    toolkit= tollkit,
    llm= model,
    verbose= True,
    agent_type= AgentType.ZERO_SHOT_REACT_DESCRIPTION
)
    


