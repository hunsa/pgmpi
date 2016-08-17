

from pgmpi.glexp_desc import abs_exp_desc



class ExpDescription(abs_exp_desc.AbstractExpDescription):
    # Local directory where the experiment files will be created
    local_basedir = "./"
    
    
    # Directory on the target machine where the experiment will be copied
    # This directory is also the base path for the generated output files
    remote_basedir = local_basedir


    # Path to the ReproMPI benchmark installation on the target machine 
    # (more info on how to install ReproMPI can be found here: 
    # https://github.com/hunsa/reprompi)
    benchmark_path_remote = "$HOME/reprompi-0.9.7/bin"

