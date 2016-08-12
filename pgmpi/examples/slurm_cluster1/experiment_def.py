

from pgmpi.glexp_desc import abs_exp_desc
from pgmpi.expconfig import glexpconfig
from pgmpi.glconfig import glconfig
from pgmpi.experiment import glexp

from pgmpi.benchmark import reproMPIbench
from pgmpi.machsetup import slurm_cluster


class ExpDescription(abs_exp_desc.AbstractExpDescription):
    # Local directory where the experiment files will be created
    __local_basedir = "test_cases/output/myexp100"
    
    
    # Directory on the target machine where the experiment will be copied
    # This directory is also the base path for the generated output files
    __remote_basedir = "/home/carpenamarie/mpi-guidelines/exp/myexp100"


    # Path to the ReproMPI benchmark installation on the target machine 
    # (more info on how to install ReproMPI can be found here: 
    # https://github.com/hunsa/reprompi)
    __benchmark_path_remote = "/home/carpenamarie/code/mpibenchmark"

 
    # Path to a local guidelines description file defining the performance 
    # guidelines to be evaluated in the current experiment
    __gl_file = "examples/slurm_cluster1/exp_guidelines.json"


    # Path to a local experiment setup file for the current experiment
    __config_file = "examples/slurm_cluster1/exp_config.json"


    def setup_exp(self):
        
        ec = glexpconfig.GLExperimentalConfig(self.__config_file)
        gl = glconfig.Guidelines(self.__gl_file)
        
        bench    = reproMPIbench.GLReproMPIBench(self.__benchmark_path_remote)
        machinfo = slurm_cluster.PGMPIMachineConfiguratorSlurm()
   
        exp = glexp.GLExperimentWriter(ec, gl, bench, machinfo, self.__local_basedir, self.__remote_basedir)

        return exp
    
    
    
    