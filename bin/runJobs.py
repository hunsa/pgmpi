#! /usr/bin/env python

import sys
import os
import subprocess

base_path = os.path.dirname( os.path.realpath( sys.argv[0] ) )
#cd ..
base_path = os.path.dirname( base_path )
lib_path = os.path.join( base_path, "lib" )
sys.path.append(lib_path)


from optparse import OptionParser
from mpiguidelines.common_exp_infos import *


if __name__ == "__main__":

    parser = OptionParser(usage="usage: %prog [options]")

    parser.add_option("-d", "--expdir",
                       action="store",
                       dest="base_expdir",
                       type="string",
                       help="path to local experiment directory")
    parser.add_option("-f", "--force",
                       action="store_true",
                       dest="force",
                       default = False,
                       help="force results directory overwriting")
    
    (options, args) = parser.parse_args()
    
    if options.base_expdir == None:
        base_expdir = os.path.abspath(base_path)
        print >> sys.stderr, "Warning: Experiment directory not specified. Using current directory %s\n" %  base_path
        parser.print_help()
    else:
        base_expdir = os.path.abspath(options.base_expdir)


    exp_dir = os.path.abspath(base_expdir)    
    if not (os.path.exists(exp_dir) and os.path.isdir(exp_dir)):
        print >> sys.stderr, "Experiment directory does not exist: %s\n" %  exp_dir
        sys.exit(1)
    
    
    jobdir = os.path.join(exp_dir, EXEC_DIRS["jobs"])
    if (not os.path.exists(jobdir)) or len(os.listdir(jobdir)) == 0:
        print >> sys.stderr, "\nGenerated job files do not exist in %s" %  jobdir
        sys.exit(1)
    
    
    outdir = os.path.join(exp_dir, EXEC_DIRS["results"])
    if len(os.listdir(outdir)) > 0:
        if not options.force:
            print >> sys.stderr, "\nJob results already generated in %s. Run script with -f option to overwrite them" %  outdir
            sys.exit(1)    
        else:
            print >> sys.stderr, "\nWarning: Overwriting job results generated in %s." %  outdir
    
    for f in os.listdir(jobdir):
        if f.endswith(".sh"):      
            print("Executing %s..." % f)
            try:
                routput = subprocess.check_output(["sh", os.path.join(jobdir, f)],
                                           stderr=subprocess.STDOUT
                                        )
                print routput
                print("Done\n")
            except subprocess.CalledProcessError, e:
                print("\nAn error has occurred when running job %s" % f)
                print e.output
                exit(1)


            

