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

from mpiguidelines import common_exp_infos

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


    rscripts_dir = os.path.join(lib_path, common_exp_infos.SCRIPT_DIRS["rscripts"])
    exp_dir = os.path.abspath(os.path.join(base_expdir, options.expname))
    
    if not (os.path.exists(exp_dir) and os.path.isdir(exp_dir)):
        print  "Experiment directory does not exist: %s\n" %  exp_dir
        sys.exit(1)
    
    
    # find output dir
    summary_dir = os.path.join(exp_dir, common_exp_infos.EXEC_RESULTS_DIRS["summary"])
    
    if not (os.path.exists(summary_dir)):
        print  "\nSummarized results do not exist: %s\n" %  summary_dir
        print "Run the ./pgmpi/bin/summarizeData.py script first."
        sys.exit(1)
    

    print("\n------------------------------------------------------------")
    print("\nThe following performance guideline violations have been found in %s:\n" % options.expname)
    script = "%s/pgmpir.R" % (rscripts_dir)
    try:
        routput = subprocess.check_output(["Rscript", script, rscripts_dir, 
                                           summary_dir],
                                           stderr=subprocess.STDOUT
                                        )
        print routput
    except subprocess.CalledProcessError, e:
        print e.output
        exit(1)
        
    print ("Done.")
