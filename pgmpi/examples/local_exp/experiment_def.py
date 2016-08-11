

from pgmpi.glexp_desc import abs_exp_desc
from pgmpi.expconfig import glexpconfig
from pgmpi.glconfig import glconfig
from pgmpi.experiment import glexp

from pgmpi.benchmark import reproMPIbench
from pgmpi.machsetup import machine_setup_local


class ExpDescription(abs_exp_desc.AbstractExpDescription):

    __local_basedir = "test_cases/output/myexp62"
    __remote_basedir = __local_basedir

    __benchmark_path_remote = "/Users/carpenamarie/Work/tuwien2014/code/mpibenchmark"
 
    __gl_file = "examples/local_exp/exp_guidelines.json"
    __config_file = "examples/local_exp/exp_config.json"


    def setup_exp(self):
        
        ec = glexpconfig.GLExperimentalConfig(self.__config_file)
        gl = glconfig.Guidelines(self.__gl_file)
        
        bench    = reproMPIbench.GLReproMPIBench(self.__benchmark_path_remote)
        machinfo = machine_setup_local.PGMPIMachineConfiguratorLocal()
   
        exp = glexp.GLExperimentWriter(ec, gl, bench, machinfo, self.__local_basedir, self.__remote_basedir)

        return exp
    
    
    
    