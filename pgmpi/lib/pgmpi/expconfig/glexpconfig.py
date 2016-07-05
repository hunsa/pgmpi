'''
Created on Jun 24, 2016

@author: carpenamarie
'''

from pgmpi.expconfig import abs_expconfig
from pgmpi.helpers import file_helpers 

class GLExperimentalConfig (abs_expconfig.AbstractExperimentalConfig):

    
    def __init__(self, exp_conf_file):
        self.__exp_conf_data = file_helpers.read_json_config_file(exp_conf_file)
        
    
    def get_exp_config(self):
        return self.__exp_conf_data