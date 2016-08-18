

from pgmpi.glexp_desc import abs_exp_desc



class ExpDescription(abs_exp_desc.AbstractExpDescription):

    # Path to the ReproMPI benchmark installation on the target machine 
    # (more info on how to install ReproMPI can be found here: 
    # https://github.com/hunsa/reprompi)
    benchmark_path_remote = "$HOME/reprompi-0.9.7/bin"

