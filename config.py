from configparser import ConfigParser
import os, sys

class Config:
    def __inti__(self):
        self.config = ConfigParser()
        self.config.read(f'{os.getcwd()}/config.ini')

    def get_title(self):
        return self.config['DEFAULT'].get('TITLE')
    
    def get_radio_option(self):
        return  self.config['DEFAULT'].get('RADIO').split(', ')
    
    def get_model(self):
        print(self.configparser['DEFAULT'].get('MODEL').split(', '))
        return self.configparser['DEFAULT'].get('MODEL').split(', ')
    
    def get_groq_model(self):
        print(self.configparser['DEFAULT'].get('VERSION_GROQ').split(', '))
        return self.configparser['DEFAULT'].get('VERSION_GROQ').split(', ')
    
    def get_ollama_model(self):
        print(self.configparser['DEFAULT'].get('VERSION_OLLAMA').split(', '))
        return self.configparser['DEFAULT'].get('VERSION_OLLAMA').split(', ')
