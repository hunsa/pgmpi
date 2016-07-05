'''
Created on Jun 24, 2016

@author: carpenamarie
'''
import abc

class AbstractExpDescription(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod  
    def setup_exp(self):
        pass