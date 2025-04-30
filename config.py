from configparser import ConfigParser
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class Config:
    def __init__(self):
        self.config = ConfigParser()
        self.config.read(f'{os.getcwd()}/config.ini')

    def get_title(self):
        return self.config['DEFAULT'].get('TITLE')
    
    def get_radio_option(self):
        return  self.config['DEFAULT'].get('RADIO').split(', ')
    
    def get_model(self):
        return self.config['DEFAULT'].get('MODEL').split(', ')
    
    def get_groq_model(self):
        return self.config['DEFAULT'].get('VERSION_GROQ').split(', ')
    
    def get_ollama_model(self):
        return self.config['DEFAULT'].get('VERSION_OLLAMA').split(', ')
