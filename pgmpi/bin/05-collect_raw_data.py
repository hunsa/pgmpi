#! /usr/bin/env python

import sys
import os
import subprocess
from optparse import OptionParser

# in bin
base_path = os.path.dirname( os.path.realpath( sys.argv[0] ) )
#cd ..
base_path = os.path.dirname( base_path )
lib_path = os.path.join( base_path, "lib" )
sys.path.append(lib_path)


from pgmpi.helpers import file_helpers
from pgmpi.glexp_desc.abs_exp_desc import AbstractExpDescription  
from pgmpi.helpers import common_exp_infos

if __name__ == "__main__":

    parser = OptionParser(usage="usage: %prog [options]")

#===============================================================================
#     parser.add_option("-n", "--expname",
#                        action="store",
#                        dest="expname",
#                        type="string",
#                        help="unique experiment name")
#     parser.add_option("-d", "--expdir",
#                        action="store",
#                        dest="base_expdir",
#                        type="string",
#                        help="path to local experiment directory")
#     
#     (options, args) = parser.parse_args()
#     
#     if options.expname == None:
#         print >> sys.stderr, "Experiment name not specified"
#         parser.print_help()
#         sys.exit(1)
# 
#     if options.base_expdir == None:
#         base_expdir = os.path.abspath(base_path)
#         print  "Warning: Experiment directory not specified. Using current directory %s\n" %  base_path
#     else:
#         base_expdir = os.path.abspath(options.base_expdir)
#===============================================================================

    
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


    exp_configurator = file_helpers.instantiate_class_from_file(options.expfile, AbstractExpDescription)

    experiment = exp_configurator.setup_exp()


    rscripts_dir = os.path.join(lib_path, common_exp_infos.SCRIPT_DIRS["rscripts"])
    rawdata_dir = experiment.get_local_verif_output_dir()
    output_dir = experiment.get_local_verif_alldata_dir()
    
    if (not os.path.exists(rawdata_dir)) or len(os.listdir(rawdata_dir)) == 0:
        print  "\nRaw benchmark output files do not exist in %s" %  rawdata_dir
        print "To generate them, execute the benchmark jobs in %s" % experiment.get_remote_verif_job_dir()
        sys.exit(1)
    
    file_helpers.create_local_dir(output_dir)
    output_file = os.path.join(output_dir, "data.txt")
    print(rawdata_dir)
    print (rscripts_dir)
    
    print("\nReading raw data...")
    script = "%s/collectAll.R" % (rscripts_dir)
    try:
        routput = subprocess.check_output(["Rscript", script, rscripts_dir, 
                                           os.path.abspath(rawdata_dir), 
                                           os.path.abspath(output_file)],
                                stderr=subprocess.STDOUT
                                )
        print routput
    except subprocess.CalledProcessError, e:
        print e.output
        exit(1)

    print ("Done.")
