'''
Created on Jun 24, 2016

@author: carpenamarie
'''

from pgmpi.expconfig import abs_expconfig
from pgmpi.helpers import file_helpers 

class GLExperimentalConfig (abs_expconfig.AbstractExperimentalConfig):

    
    def __init__(self, exp_conf_file):
        self.__exp_conf_data = file_helpers.read_json_config_file(exp_conf_file)
        self.__exp_conf_filepath = exp_conf_file
    
    def get_conf_filepath(self):
        return self.__exp_conf_filepath
   
    def get_num_nodes(self):
        return self.__exp_conf_data["nodes"]

    def get_num_nnp(self):
        return self.__exp_conf_data["nnp"]
    
    def get_verif_nmpiruns(self):
        return self.__exp_conf_data["nmpiruns"]
    
    def get_prediction_nmpiruns(self):
        return self.__exp_conf_data["prediction"]["nmpiruns"]    
        
    def get_prediction_min_nrep(self):
        return self.__exp_conf_data["prediction"]["min"]

    def get_prediction_max_nrep(self):
        return self.__exp_conf_data["prediction"]["max"]
    
    def get_prediction_step_nrep(self):
        return self.__exp_conf_data["prediction"]["step"]
    
    def get_prediction_methods(self):
        return self.__exp_conf_data["prediction"]["methods"]
    
    def get_prediction_threshold(self, method):
        for i in range(len(self.__exp_conf_data["prediction"]["methods"])):
            if self.__exp_conf_data["prediction"]["methods"][i] == method:
                return self.__exp_conf_data["prediction"]["thresholds"][i]
        return None
        
        
    def get_prediction_window(self, method):
        for i in range(len(self.__exp_conf_data["prediction"]["methods"])):
            if self.__exp_conf_data["prediction"]["methods"][i] == method:
                return self.__exp_conf_data["prediction"]["windows"][i]
        return None
    
    