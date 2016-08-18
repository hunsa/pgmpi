'''
Created on Jun 24, 2016

@author: carpenamarie
'''
import abc

from pgmpi.experiment import glexp

from pgmpi.benchmark import reproMPIbench
from pgmpi.machsetup import machine_setup_local

class AbstractExpDescription(object):
    __metaclass__ = abc.ABCMeta


    def __init__(self):
        self.bench    = reproMPIbench.GLReproMPIBench(self.benchmark_path_remote)
    
    
    def setup_exp(self):
        
        machinfo = machine_setup_local.PGMPIMachineConfiguratorLocal()
   
        exp = glexp.GLExperimentWriter(self.bench, machinfo)

        return exp
    
    
    