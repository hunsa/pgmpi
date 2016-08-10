#! /usr/bin/env python

import sys
import os
import shutil

# in bin
base_path = os.path.dirname( os.path.realpath( sys.argv[0] ) )
#cd ..
base_path = os.path.dirname( base_path )
lib_path = os.path.join( base_path, "lib" )
sys.path.append(lib_path)

from optparse import OptionParser
from pgmpi.helpers import file_helpers
from pgmpi.glexp_desc.abs_exp_desc import AbstractExpDescription  
    
    

if __name__ == "__main__":

    parser = OptionParser(usage="usage: %prog [options]")

    parser.add_option("-i", "--expfile",
                       action="store",
                       dest="expfile",
                       type="string",
                       help="experiment input file")
    
    
    (options, args) = parser.parse_args()

    if options.expfile == None or not os.path.exists(options.expfile):
        print >> sys.stderr, "ERROR: Experiment setup file not specified or does not exist"
        parser.print_help()
        sys.exit(1)

    #include experiment file directory in the path
    sys.path.append(os.path.dirname(options.expfile))

    #instantiate experiment configuration class from user file
    exp_configurator_class = file_helpers.get_class_from_file(options.expfile, AbstractExpDescription)
    exp_configurator = exp_configurator_class() 
        
    experiment = exp_configurator.setup_exp()

    experiment.create_exp_dir_structure()
    experiment.create_init_config_files()






