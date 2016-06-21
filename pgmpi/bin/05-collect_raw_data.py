#! /usr/bin/env python

import sys
import os
import subprocess

# in bin
base_path = os.path.dirname( os.path.realpath( sys.argv[0] ) )
#cd ..
base_path = os.path.dirname( base_path )
lib_path = os.path.join( base_path, "lib" )
sys.path.append(lib_path)

from optparse import OptionParser
from mpiguidelines.helpers import file_helpers
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

    if options.base_expdir == None:
        base_expdir = os.path.abspath(base_path)
        print  "Warning: Experiment directory not specified. Using current directory %s\n" %  base_path
    else:
        base_expdir = os.path.abspath(options.base_expdir)


    rscripts_dir = os.path.join(lib_path, SCRIPT_DIRS["rscripts"])
    exp_dir = os.path.abspath(os.path.join(base_expdir, options.expname))
    
    exec_dir_name = options.expname + "_" + EXEC_BASEDIR
    exec_dir = os.path.join(exp_dir, exec_dir_name)
    assert os.path.isdir(exp_dir), "Cannot find experiment execution directory %s" % (exec_dir)
    
    
    if not (os.path.exists(exp_dir) and os.path.isdir(exp_dir)):
        print  "Experiment directory does not exist: %s\n" %  exp_dir
        sys.exit(1)
    
    
    rawdata_dir = os.path.join(exec_dir, EXEC_DIRS["raw_data"])
    if (not os.path.exists(rawdata_dir)) or len(os.listdir(rawdata_dir)) == 0:
        print  "\nRaw benchmark output files do not exist in %s" %  rawdata_dir
        print "To generate them, execute the benchmark jobs in %s" % os.path.join(exec_dir, EXEC_DIRS["jobs"])
        sys.exit(1)
    
    output_dir = os.path.join(exp_dir, EXEC_RESULTS_DIRS["alldata"])
    file_helpers.create_local_dir(output_dir)
    output_file = os.path.join(output_dir, "data.txt")
    print(rawdata_dir)
    print (rscripts_dir)
    
    print("\nReading raw data...")
    script = "%s/collectAll.R" % (rscripts_dir)
    try:
        routput = subprocess.check_output(["Rscript", script, rscripts_dir, rawdata_dir, output_file],
                                stderr=subprocess.STDOUT
                                )
        print routput
    except subprocess.CalledProcessError, e:
        print e.output
        exit(1)

    print ("Done.")
