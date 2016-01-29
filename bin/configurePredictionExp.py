#! /usr/bin/env python

import sys
import os
from optparse import OptionParser

# in bin
base_path = os.path.dirname( os.path.realpath( sys.argv[0] ) )
#cd ..
base_path = os.path.dirname( base_path )
lib_path = os.path.join( base_path, "lib" )
sys.path.append(lib_path)

import mpiguidelines.prediction_exp_generator as predgen
from mpiguidelines.common_exp_infos import *
import mpiguidelines.helpers.file_helpers as helpers

if __name__ == "__main__":

    parser = OptionParser(usage="usage: %prog [options]")

    parser.add_option("-n", "--expname",
                       action="store",
                       dest="expname",
                       type="string",
                       help="unique experiment name")
    parser.add_option("-d", "--expdir",
                       action="store",
                       dest="base_expdir",
                       type="string",
                       help="path to local experiment directory")

    (options, args) = parser.parse_args()

    if options.expname == None:
        print >> sys.stderr, "Experiment name not specified"
        parser.print_help()
        sys.exit(1)
    expname = options.expname

    if options.base_expdir == None:
        print >> sys.stderr, "Experiment directory does not exist. Please create it using the ./bin/setupExp script"
        parser.print_help()
        sys.exit(1)
    else:
        exp_base_dir = os.path.abspath(options.base_expdir)
    
    predgen.initialize_config_files(expname, exp_base_dir)
    
    exec_dir_name = expname + "_" + PREDICTION_BASEDIR
    exp_dir = os.path.join(exp_base_dir, expname)
    assert os.path.isdir(exp_dir), "Cannot find experiment execution directory %s" % (exec_dir_name)
        
    exec_dir = os.path.join(exp_dir, exec_dir_name) 
    exec_input_dir = os.path.join(exec_dir, PREDICTION_DIRS["input"])
    exec_job_dir = os.path.join(exec_dir, PREDICTION_DIRS["jobs"])
        
    
    config_data = predgen.get_exp_config_data(expname, exp_base_dir)
    
    predgen.create_input_file(config_data, exec_input_dir)
    predgen.create_job_file(config_data, exec_job_dir)

    
    

