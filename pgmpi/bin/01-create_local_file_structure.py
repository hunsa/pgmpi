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
from mpiguidelines import file_helpers
from mpiguidelines import common_exp_infos

    
def create_exp_dir_structure(expname, exp_base_dir):
    
    exp_dir = os.path.join(exp_base_dir, expname)
    ret = file_helpers.create_local_dir(exp_dir)
    if not ret:
        print ("Specify another experiment name or path to create a new experiment.\n")
        sys.exit(1) 
    
    # create prediction directory tree
    pred_dir_name = expname + "_" + common_exp_infos.PREDICTION_BASEDIR
    pred_dir = os.path.join(exp_dir, pred_dir_name)
    file_helpers.create_local_dir(pred_dir)
    for d in common_exp_infos.PREDICTION_DIRS.values():
        file_helpers.create_local_dir(os.path.join(pred_dir, d))
    for d in common_exp_infos.PREDICTION_RESULTS_DIRS.values():
        file_helpers.create_local_dir(os.path.join(pred_dir, d))
    
    # create experiment execution directory tree
    exec_dir_name = expname + "_" + common_exp_infos.EXEC_BASEDIR
    exec_dir = os.path.join(exp_dir, exec_dir_name)
    file_helpers.create_local_dir(exec_dir)
    for d in common_exp_infos.EXEC_DIRS.values():
        file_helpers.create_local_dir(os.path.join(exec_dir, d))

    # create experiment results directory tree
    for d in common_exp_infos.EXEC_RESULTS_DIRS.values():
        file_helpers.create_local_dir(os.path.join(exp_dir, d))


    #create initial configuration directory
    conf_dir = os.path.join(exp_dir, common_exp_infos.CONFIG_BASEDIR)
    file_helpers.create_local_dir(conf_dir)
    
 
def create_init_config_files(expname, exp_base_dir, glconf, expconf, machconf):
    exp_dir = os.path.join(exp_base_dir, expname)
    assert os.path.isdir(exp_dir)
    
    shutil.copy(glconf, os.path.join(exp_dir, common_exp_infos.CONFIG_BASEDIR))
    shutil.copy(expconf, os.path.join(exp_dir, common_exp_infos.CONFIG_BASEDIR))
    shutil.copy(machconf, os.path.join(exp_dir, common_exp_infos.CONFIG_BASEDIR))
    
    
    

if __name__ == "__main__":

    parser = OptionParser(usage="usage: %prog [options]")

    parser.add_option("-g", "--glconf",
                       action="store",
                       dest="glconf",
                       type="string",
                       help="path to guidelines config file")
    parser.add_option("-e", "--expconf",
                       action="store",
                       dest="expconf",
                       type="string",
                       help="path to exp config file")
    parser.add_option("-m", "--machcode",
                        action="store",
                        dest="machcode",
                        type="string",
                        help="path to machine-specific class file")
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
#     parser.add_option("--local_exec",
#                        action="store_true",
#                        dest="local_exec",
#                        help="Run experiment locally (ignore remote paths)")

    (options, args) = parser.parse_args()

    if options.glconf == None or not os.path.exists(options.glconf):
        print >> sys.stderr, "ERROR: Guidelines configuration file invalid"
        parser.print_help()
        sys.exit(1)

    if options.expconf == None or not os.path.exists(options.expconf):
        print >> sys.stderr, "ERROR: Experiment configuration file invalid"
        parser.print_help()
        sys.exit(1)

    if options.machcode == None or not os.path.exists(options.machcode):
        print >> sys.stderr, "ERROR: Machine configuration file invalid"
        parser.print_help()
        sys.exit(1)

    if options.expname == None:
        print >> sys.stderr, "ERROR: Experiment name not specified"
        parser.print_help()
        sys.exit(1)

    if options.base_expdir == None:
        base_expdir = os.path.abspath(base_path)
        print  "Warning: Experiment directory not specified. Using current directory %s\n" %  base_path
    else:
        base_expdir = os.path.abspath(options.base_expdir)


    create_exp_dir_structure(options.expname, base_expdir)
    create_init_config_files(options.expname, base_expdir, options.glconf, options.expconf, options.machcode)






