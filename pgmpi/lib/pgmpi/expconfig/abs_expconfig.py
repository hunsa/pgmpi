'''
Created on Jun 24, 2016

@author: carpenamarie
'''
import abc



class AbstractExperimentalConfig():
    __metaclass__ = abc.ABCMeta

    
    @abc.abstractmethod 
    def get_conf_filepath(self):
        pass
   
    @abc.abstractmethod 
    def get_num_nodes(self):
        pass

    @abc.abstractmethod 
    def get_num_nnp(self):
        pass
    
    @abc.abstractmethod 
    def get_verif_nmpiruns(self):
        pass
    
    @abc.abstractmethod 
    def get_prediction_nmpiruns(self):
        pass
        
    @abc.abstractmethod 
    def get_prediction_min_nrep(self):
        pass

    @abc.abstractmethod 
    def get_prediction_max_nrep(self):
        pass
    
    @abc.abstractmethod 
    def get_prediction_step_nrep(self):
        pass
    
    @abc.abstractmethod 
    def get_prediction_methods(self):
        pass
    
    @abc.abstractmethod 
    def get_prediction_threshold(self, method):
        pass
        
    @abc.abstractmethod 
    def get_prediction_window(self, method):
        pass