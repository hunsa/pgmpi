

from pgmpi.glexp_desc import abs_exp_desc
from pgmpi.experiment import glexp

import machine_conf


class ExpDescription(abs_exp_desc.AbstractExpDescription):

    local_basedir = "test_cases/output/myexp100"
    remote_basedir = "/home/lv70648/carpenamarie/mpi-guidelines/exp/myexp100"

    benchmark_path_remote = "/home/lv70648/carpenamarie/code/mpibenchmark"
 
    gl_file = "examples/customized_slurm_cluster1/exp_guidelines.json"
    config_file = "examples/customized_slurm_cluster1/exp_config.json"


    def setup_exp(self):
       
        machinfo = machine_conf.MySlurmConfigurator(qos="normal_0064", partition="mem_0064")
   
        exp = glexp.GLExperimentWriter(self.ec, self.gl, self.bench, machinfo, self.local_basedir, self.remote_basedir)

        return exp
    
    
    
    