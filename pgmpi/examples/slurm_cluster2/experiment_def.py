

from pgmpi.glexp_desc import abs_exp_desc
from pgmpi.experiment import glexp
from pgmpi.machsetup import slurm_cluster


class ExpDescription(abs_exp_desc.AbstractExpDescription):
    # Local directory where the experiment files will be created
    local_basedir = "test_cases/output/myexp100"
    
    
    # Directory on the target machine where the experiment will be copied
    # This directory is also the base path for the generated output files
    remote_basedir = "/home/lv70648/carpenamarie/mpi-guidelines/exp/myexp100"


    # Path to the ReproMPI benchmark installation on the target machine 
    # (more info on how to install ReproMPI can be found here: 
    # https://github.com/hunsa/reprompi)
    benchmark_path_remote = "/home/lv70648/carpenamarie/code/mpibenchmark"

 
    # Path to a local guidelines description file defining the performance 
    # guidelines to be evaluated in the current experiment
    gl_file = "examples/slurm_cluster2/exp_guidelines.json"


    # Path to a local experiment setup file for the current experiment
    config_file = "examples/slurm_cluster2/exp_config.json"


    def setup_exp(self):
        
        machinfo = slurm_cluster.PGMPIMachineConfiguratorSlurm(qos="normal_0064", partition="mem_0064")
   
        exp = glexp.GLExperimentWriter(self.ec, self.gl, self.bench, machinfo, self.local_basedir, self.remote_basedir)

        return exp
    
    
    
    