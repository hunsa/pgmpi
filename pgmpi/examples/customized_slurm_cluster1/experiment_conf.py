

from pgmpi.glexp_desc import abs_exp_desc
from pgmpi.experiment import glexp
from pgmpi.benchmark import reproMPIbench
from pgmpi.machsetup import slurm_cluster



class MySlurmConfigurator(slurm_cluster.PGMPIMachineConfiguratorSlurm):
    mpirun_call = "mpirun"
    slurm_job_name = "jobPGMPImpirun"
        


class ExpDescription(abs_exp_desc.AbstractExpDescription):

    # Path to the ReproMPI benchmark binaries on the target machine 
    # (more info on how to install ReproMPI can be found here: 
    # https://github.com/hunsa/reprompi)
    benchmark_path_remote = "/home/lv70648/carpenamarie/code/mpibenchmark"
 
    
    def setup_exp(self):
        
        bench    = reproMPIbench.GLReproMPIBench(self.benchmark_path_remote)
        machinfo = MySlurmConfigurator(qos = "normal_0064", partition = "mem_0064", account = None, walltime = None)
   
        exp = glexp.GLExperimentWriter(bench, machinfo)

        return exp
    
    
    
    