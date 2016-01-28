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
import mpiguidelines.prediction_exp_generator as predgen

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

    if options.base_expdir == None:
        print >> sys.stderr, "Experiment directory does not exist. Please create it using the ./bin/setupExp script"
        parser.print_help()
        sys.exit(1)
    else:
        base_expdir = os.path.abspath(options.base_expdir)
    
    #exp_dir = os.path.join(base_expdir, options.expname)
    #predgen.create_exp_dir_structure(options.expname, base_expdir)
    
    predgen.initialize_config_files(options.expname, base_expdir)
    predgen.create_input_file(options.expname, base_expdir)
    predgen.create_job_file(options.expname, base_expdir)
    #confgen.create_init_config_files(options.expname, base_expdir)
    
    #exp_file_path = conf.generate_exp_file(options.expconf, options.machconf, exp_dir, options.local_exec)
    
    #data = conf.read_json_config_file(exp_file_path)
    
    #mpiruns =jobgen.generate_mpiruns_list(data)
    #jobgen.generate_job_file(data, mpiruns)
    
    

