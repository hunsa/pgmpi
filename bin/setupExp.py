#! /usr/bin/env python

import sys
import os

# in bin
base_path = os.path.dirname( os.path.realpath( sys.argv[0] ) )
#cd ..
base_path = os.path.dirname( base_path )
lib_path = os.path.join( base_path )
sys.path.append(lib_path)

from optparse import OptionParser
import mpiguidelines.config_helpers as conf
import mpiguidelines.job_generator as jobgen


if __name__ == "__main__":

    parser = OptionParser(usage="usage: %prog [options]")

    parser.add_option("-e", "--expconf",
                       action="store",
                       dest="expconf",
                       type="string",
                       help="path to exp config file")
    parser.add_option("-m", "--machconf",
                       action="store",
                       dest="machconf",
                       type="string",
                       help="path to machine/benchmark configuration file")
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
    parser.add_option("--local_exec",
                       action="store_true",
                       dest="local_exec",
                       help="Run experiment locally (ignore remote paths)")

    (options, args) = parser.parse_args()
 
    if options.expconf == None or not os.path.exists(options.expconf):
        print >> sys.stderr, "Experiment configuration file invalid"
        parser.print_help()
        sys.exit(1)

    if options.machconf == None or not os.path.exists(options.machconf):
        print >> sys.stderr, "Machine configuration file invalid"
        parser.print_help()
        sys.exit(1)

    if options.expname == None:
        print >> sys.stderr, "Experiment name not specified"
        parser.print_help()
        sys.exit(1)

    if options.base_expdir == None:
        base_expdir = os.path.abspath(base_path)
        print  "Warning: Experiment directory not specified. Using current directory %s\n" %  base_path
    else:
        base_expdir = os.path.abspath(options.base_expdir)
    
    exp_dir = os.path.join(base_expdir, options.expname)
    
    exp_file_path = conf.generate_exp_file(options.expconf, options.machconf, exp_dir, options.local_exec)
    
    data = conf.read_json_config_file(exp_file_path)
    
    mpiruns =jobgen.generate_mpiruns_list(data)
    jobgen.generate_job_file(data, mpiruns)
    
    

