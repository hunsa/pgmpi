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