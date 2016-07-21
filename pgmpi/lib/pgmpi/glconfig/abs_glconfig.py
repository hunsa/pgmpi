'''
Created on Jun 24, 2016

@author: carpenamarie
'''
import abc

class AbstractGLConfig():
    __metaclass__ = abc.ABCMeta


    @abc.abstractmethod  
    def get_gl_filepath(self):
        pass