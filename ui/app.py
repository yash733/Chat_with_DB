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
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import Config
config = Config()

from src.model import Model

st.title(config.get_title())

if 'user' not in st.session_state:
    st.session_state.user = {}

if 'messages' not in st.session_state:
    st.session_state.messages = [{'role': 'system', 'content': 'You are an helpful assistant.'}, 
                                {'role': 'assistant', 'content': 'Ask me anything related to the DataBase'}]

if 'model_llm' not in st.session_state:
    st.session_state.model_llm = None

# ----- Display Conversation till present ----- #
for i in st.session_state.messages[1:]:
    st.chat_message(i['role']).write(i['content'])

# ----- Input ----- #
db_selected = st.sidebar.radio(label='Choose DataBase to work with', options= config.get_radio_option())

if db_selected:
    # ----- DataBase Data ----- #
    if db_selected == 'Use SqlLight 3 DataBase- student.db':
        database_ = 'Local_DB'
        
    elif db_selected == 'Connected to your SQL DataBase':
        database_ = 'MySql_DB'
        with st.sidebar:
            if not st.session_state.user.get('my_sql_pass'):
                my_sql_host = st.text_input(label='Provide MySQL Host')
                my_sql_db = st.text_input(label='MySql DataBase')
                my_sql_user = st.text_input(label='User name')
                my_sql_pass = st.text_input(label='MySql Password: ', type= 'password')
                my_sql_button = False

                if my_sql_host and my_sql_db and my_sql_user and my_sql_pass :
                    if st.button('Proceed', key= 'Mysql') and not my_sql_button:
                        st.session_state.user.update({'my_sql_host':my_sql_host, 'my_sql_db': my_sql_db,'my_sql_user':my_sql_user,'my_sql_pass':my_sql_pass})
                        my_sql_button = True
                        st.rerun()
            else:
                with st.expander("Database Details"):
                    st.write('MySQL Host: ',st.session_state.user.get('my_sql_host'))
                    st.write('MySql DataBase: ',st.session_state.user.get('my_sql_db'))
                    st.write('User name: ',st.session_state.user.get('my_sql_user'))
    
    # ----- LLM MODEL ----- #
    with st.sidebar:
        model = st.selectbox(label='Choose LLM model', options= config.get_model())
        if model == 'Groq':
            api = st.text_input(label= 'api key', type= 'password', value='')
            model_type = st.selectbox(label= 'Model Type', options= config.get_groq_model())
            button_ = False
            if api and not button_ and st.button(label= 'Save', key= 'Groq') :
                button_ = True
                st.session_state.user.update({'model': model, 'model_type': model_type, 'api' : api})
                st.session_state.model_llm = Model().groq()

        else:
            model_type = st.selectbox(label= 'Model Type', options= config.get_ollama_model())
            button_ = False
            if not button_ and st.button(label= 'Save', key= 'Ollama'):
                st.session_state.user.update({'model': 'Ollama', 'model_type': model_type})
                button_ = True
                st.session_state.model_llm = Model().ollama()
        

    # ----- database connection -----#
    @st.cache_resource(ttl='1h')
    def db_config(database_, my_sql_host = None, my_sql_db = None, my_sql_user = None, my_sql_pass = None):
        if database_ == 'Local_DB':
            db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'../student.db')
            creator = lambda : sqlite3.connect(f'file:{db_path}?mode=ro', uri = True) # uri open advance function like read-only, read-write, read-write-create
            return SQLDatabase(create_engine('sqlite:///',creator=creator))
            #"""'sqlite:///' → Tells SQLAlchemy:
            #'Use the SQLite driver, and I’ll provide the connection via other means.'"""

        elif database_ == 'MySql_DB':
            if not (my_sql_host, my_sql_db, my_sql_user, my_sql_pass):
                st.error('Kindly provide all the details inorder to connect with MySQL DataBase')
                st.stop()
            return SQLDatabase(create_engine(f"mysql+mysqlconnector://{my_sql_user}:{my_sql_pass}@{my_sql_host}/{my_sql_db}"))
        
    if database_ == 'Local_DB':
        db = db_config(database_)

    elif database_ == 'MySql_DB':
        my_sql_host = st.session_state.user.get('my_sql_host')
        my_sql_db = st.session_state.user.get('my_sql_db')
        my_sql_user = st.session_state.user.get('my_sql_user')
        my_sql_pass = st.session_state.user.get('my_sql_pass')

        if not all([my_sql_host, my_sql_db, my_sql_user, my_sql_pass]):
            st.error("Please provide all MySQL connection details")
            st.stop()
        db = db_config(my_sql_host, my_sql_db, my_sql_user, my_sql_pass)
        
    if db is None:
        st.error("Database connection failed. Please check your configuration.")
        st.stop()

    if st.session_state.model_llm and db:
        
        # ----- Toolkit ----- # calling multiple tools managing sql fucntions
        tollkit = SQLDatabaseToolkit(llm = st.session_state.model_llm, db = db)

        # ----- Agent ----- #
        agent = create_sql_agent(
            toolkit= tollkit,
            llm= st.session_state.model_llm,
            verbose= True,
            agent_type= AgentType.ZERO_SHOT_REACT_DESCRIPTION
        )

        
        user_query = st.chat_input(placeholder= 'Enter your query')

        if user_query:
            st.session_state.messages.append({'role':'user', 'content':user_query})
            st.chat_message('user').write(user_query)

            with st.chat_message('assistant'):
                streamlit_callback=StreamlitCallbackHandler(st.container())
                try:
                    response = agent.run(input= user_query, callbacks=[streamlit_callback], handle_parsing_errors= True)
                    st.session_state.messages.append({"role":"assistant","content":response})
                except ValueError:
                    st.error('Error occured, unable to handle parsing')                    
    
    else:
        st.warning("Please ensure both the model and database connection are configured")

else: 
    st.error('Kindly select a database to work with.')
    st.rerun()

