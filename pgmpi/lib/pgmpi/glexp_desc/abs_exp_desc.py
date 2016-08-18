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

    
    def setup_exp(self):
        
        bench    = reproMPIbench.GLReproMPIBench(self.benchmark_path_remote)
        machinfo = machine_setup_local.PGMPIMachineConfiguratorLocal()
   
        exp = glexp.GLExperimentWriter(bench, machinfo)

        return exp
    
    
    