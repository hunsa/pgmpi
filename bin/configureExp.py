#! /usr/bin/env python

import sys
import os

# in bin
base_path = os.path.dirname( os.path.realpath( sys.argv[0] ) )
#cd ..
base_path = os.path.dirname( base_path )
lib_path = os.path.join( base_path, "lib" )
sys.path.append(lib_path)

from optparse import OptionParser
import mpiguidelines.exp_generator as expgen
from mpiguidelines.common_exp_infos import *

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
    
    
    expgen.initialize_config_files(expname, exp_base_dir)
    
    
    exec_dir_name = expname + "_" + EXEC_BASEDIR
    exp_dir = os.path.join(exp_base_dir, expname)
    assert os.path.isdir(exp_dir), "Cannot find experiment execution directory %s" % (exec_dir_name)
        
    exec_dir = os.path.join(exp_dir, exec_dir_name) 
    exec_input_dir = os.path.join(exec_dir, EXEC_DIRS["input"])
    exec_job_dir = os.path.join(exec_dir, EXEC_DIRS["jobs"])
    execconfig_dir = os.path.join(exec_dir, EXEC_DIRS["config"])
    config_file_name = os.path.join(execconfig_dir, expname + ".json")    
        
    config_data = expgen.get_exp_config_data(expname, exp_base_dir)
    prediction_data = expgen.get_nrep_predictions(expname, exp_base_dir)

    if len(prediction_data) == 0:
        try:
            prediction_cfg = config_data["exp_info"]["prediction"]
            try:
                max_nrep = prediction_cfg["max"]
            except KeyError:
                print >> sys.stderr, "No maximum nrep value specified in the configuration file %s." % (config_file_name)
                max_nrep = 1000
        except KeyError:
            print >> sys.stderr, "No prediction data specified in configuration file %s." % (config_file_name)
            max_nrep = 1000

        print >> sys.stderr, "Warning: no prediction data found or incorrectly formatted. Using the predefined maximum runs %d" % (max_nrep)   

    
    expgen.create_input_file(config_data, prediction_data, exec_input_dir, max_nrep)
    expgen.create_job_file(config_data, exec_job_dir)
    
    
    
    
    
    
    
    
    