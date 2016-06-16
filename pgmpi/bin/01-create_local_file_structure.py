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
import mpiguidelines.exp_setup_generator as confgen

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
#     parser.add_option("-m", "--machconf",
#                        action="store",
#                        dest="machconf",
#                        type="string",
#                        help="path to machine/benchmark configuration file")
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
        print >> sys.stderr, "Guidelines configuration file invalid"
        parser.print_help()
        sys.exit(1)

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


    confgen.create_exp_dir_structure(options.expname, base_expdir)

    confgen.create_init_config_files(options.expname, base_expdir, options.glconf, options.expconf, options.machconf)

    data = confgen.generate_complete_exp_data(options.expname, base_expdir, options.glconf, options.expconf,
                                              options.machconf, options.local_exec)
    confgen.write_complete_exp_data(options.expname, base_expdir, data)






