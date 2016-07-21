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
    summary_dir = experiment.get_local_verif_processed_dir()

        
    if not (os.path.exists(summary_dir)):
        print  "\nSummarized results do not exist: %s\n" %  summary_dir
        print "Run the ./pgmpi/bin/summarizeData.py script first."
        sys.exit(1)
    

    print("\n------------------------------------------------------------")
    print("\nThe following performance guideline violations have been found:\n" )
    
    rscripts_dir = os.path.join(lib_path, common_exp_infos.SCRIPT_DIRS["rscripts"])
    script = "%s/pgmpir.R" % (rscripts_dir)
    try:
        routput = subprocess.check_output(["Rscript", script, rscripts_dir, 
                                           os.path.abspath(summary_dir)],
                                           stderr=subprocess.STDOUT
                                        )
        print routput
    except subprocess.CalledProcessError, e:
        print e.output
        exit(1)
        
    print ("Done.")
