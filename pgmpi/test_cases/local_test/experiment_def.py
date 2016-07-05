

from pgmpi.glexp_desc.abs_exp_desc import AbstractExpDescription
from pgmpi.machsetup import machine_setup_local
from pgmpi.benchmark import reproMPIbench
from pgmpi.expconfig import glexpconfig
from pgmpi.glconfig import glconfig
from pgmpi.experiment import glexp


class ExpDescription(AbstractExpDescription):

    __local_basedir = "test_cases/output/myexp51"
    __remote_basedir = __local_basedir

    __benchmark_path_remote = "/Users/carpenamarie/Work/tuwien2014/code/mpibenchmark"
 
    __gl_file = "test_cases/local_test/exp_guidelines.json"
    __config_file = "test_cases/local_test/exp_config.json"


    def setup_exp(self):
        
        ec = glexpconfig.GLExperimentalConfig(self.__config_file)
        gl = glconfig.Guidelines(self.__gl_file)
        
        bench    = reproMPIbench.GLReproMPIBench(self.__benchmark_path_remote)
        machinfo = machine_setup_local.PGMPIMachineConfiguratorLocal(self.__remote_basedir)
   
        exp = glexp.GLExperiment(ec, gl, bench, machinfo, self.__local_basedir)

        return exp
    
    
    
    