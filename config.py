from configparser import ConfigParser
import os, sys

class Config:
    def __inti__(self):
        self.config = ConfigParser()
        self.config.read(f'{os.getcwd()}/config.ini')

    def get_title(self):
        return self.config['DEFAULT'].get('TITLE')
    
    def get_radio_option(self):
        return  self.config['DEFAULT'].get('TITLE').split(', ')