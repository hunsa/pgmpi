#! /usr/bin/env python

import sys
import os
from optparse import OptionParser

# in bin
base_path = os.path.dirname( os.path.realpath( sys.argv[0] ) )
#cd ..
base_path = os.path.dirname( base_path )
lib_path = os.path.join( base_path, "lib" )
sys.path.append(lib_path)


from pgmpi.helpers import file_helpers
from pgmpi.glexp_desc.abs_exp_desc import AbstractExpDescription  

    
OUTPUT_SEPARATOR = "-" * 30 

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
    experiment.generate_pred_input_files()
    experiment.create_prediction_jobs()
    
    
    print OUTPUT_SEPARATOR
    print OUTPUT_SEPARATOR
    if not experiment.get_exp_dir() == experiment.get_remote_exp_dir():
        print "To execute the experiment: \nCopy: \n\t%s \nTo the target machine in: \n\t%s\n" % (experiment.get_exp_dir(),  os.path.dirname(experiment.get_remote_exp_dir())) 
        print OUTPUT_SEPARATOR
    print "Execute the jobs from: \n\t%s\n" % (experiment.get_remote_pred_job_dir())
    print OUTPUT_SEPARATOR
    