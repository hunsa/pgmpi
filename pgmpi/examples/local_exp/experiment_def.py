

from pgmpi.glexp_desc import abs_exp_desc

class ExpDescription(abs_exp_desc.AbstractExpDescription):
    # Local directory where the experiment files will be created
    local_basedir = "test_cases/output/myexp101"
    
    
    # Directory on the target machine where the experiment will be copied
    # This directory is also the base path for the generated output files
    remote_basedir = local_basedir


    # Path to the ReproMPI benchmark installation on the target machine 
    # (more info on how to install ReproMPI can be found here: 
    # https://github.com/hunsa/reprompi)
    benchmark_path_remote = "/Users/carpenamarie/Work/tuwien2014/code/mpibenchmark"

 
    # Path to a local guidelines description file defining the performance 
    # guidelines to be evaluated in the current experiment
    gl_file = "examples/local_exp/exp_guidelines.json"


    # Path to a local experiment setup file for the current experiment 
    config_file = "examples/local_exp/exp_config.json"


    
    
    