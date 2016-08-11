

from pgmpi.glexp_desc import abs_exp_desc
from pgmpi.expconfig import glexpconfig
from pgmpi.glconfig import glconfig
from pgmpi.experiment import glexp

from pgmpi.benchmark import reproMPIbench
from pgmpi.machsetup import slurm_cluster



class MySlurmConfigurator(slurm_cluster.PGMPIMachineConfiguratorSlurm):
    mpirun_call = "mpirun"
    slurm_job_name = "jobPGMPImpirun"
        


class ExpDescription(abs_exp_desc.AbstractExpDescription):

    __local_basedir = "output/myexp100"
    __remote_basedir = "/home/lv70648/carpenamarie/mpi-guidelines/exp/myexp100"

    __benchmark_path_remote = "/home/lv70648/carpenamarie/code/mpibenchmark"
 
    __gl_file = "examples/customized_slurm_cluster1/exp_guidelines.json"
    __config_file = "examples/customized_slurm_cluster1/exp_config.json"


    def setup_exp(self):
        
        ec = glexpconfig.GLExperimentalConfig(self.__config_file)
        gl = glconfig.Guidelines(self.__gl_file)
        
        bench    = reproMPIbench.GLReproMPIBench(self.__benchmark_path_remote)
        machinfo = MySlurmConfigurator(qos="normal_0064", partition="mem_0064")
   
        exp = glexp.GLExperimentWriter(ec, gl, bench, machinfo, self.__local_basedir, self.__remote_basedir)

        return exp
    
    
    
    