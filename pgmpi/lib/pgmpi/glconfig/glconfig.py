'''
Created on Jun 24, 2016

@author: carpenamarie
'''
from pgmpi.glconfig.abs_glconfig import AbstractGLConfig
from pgmpi.helpers import file_helpers 

class Guidelines(AbstractGLConfig):


    def __init__(self, gl_config_file):
        self.__gl_conf_data = file_helpers.read_json_config_file(gl_config_file)
        
                
        

    def get_gl_config(self):
        return self.__gl_conf_data 