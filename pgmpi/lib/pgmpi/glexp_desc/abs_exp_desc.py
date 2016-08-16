'''
Created on Jun 24, 2016

@author: carpenamarie
'''
import abc

from pgmpi.expconfig import glexpconfig
from pgmpi.glconfig import glconfig
from pgmpi.experiment import glexp

from pgmpi.benchmark import reproMPIbench
from pgmpi.machsetup import machine_setup_local

class AbstractExpDescription(object):
    __metaclass__ = abc.ABCMeta


    def __init__(self):
        self.ec = glexpconfig.GLExperimentalConfig(self.config_file)
        self.gl = glconfig.Guidelines(self.gl_file) 
        self.bench    = reproMPIbench.GLReproMPIBench(self.benchmark_path_remote)
    
    
    def setup_exp(self):
        
        machinfo = machine_setup_local.PGMPIMachineConfiguratorLocal()
   
        exp = glexp.GLExperimentWriter(self.ec, self.gl, self.bench, machinfo, self.local_basedir, self.remote_basedir)

        return exp
    
    
    