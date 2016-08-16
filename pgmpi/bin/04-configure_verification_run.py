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
from pgmpi.helpers import common_exp_infos

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

    #include experiment file directory in the path
    sys.path.append(os.path.dirname(options.expfile))


    #instantiate experiment configuration class from user file
    exp_configurator_class = file_helpers.get_class_from_file(options.expfile, AbstractExpDescription)
    exp_configurator = exp_configurator_class() 
    
    experiment = exp_configurator.setup_exp()
    
    
    processed_dir = experiment.get_local_pred_processed_dir()
    pred_file = os.path.join(processed_dir, common_exp_infos.PREDICTION_PROCESSED_OUTPUT_FILENAME)
    
    prediction_data = file_helpers.read_json_config_file(pred_file) 
    assert len(prediction_data) > 0, "No prediction data found or incorrectly formatted. Generate prediction data first"  
    
    
    experiment.generate_verification_input_files(prediction_data)
    experiment.create_verification_jobs()
    
    print OUTPUT_SEPARATOR
    print OUTPUT_SEPARATOR
    if not experiment.get_exp_dir() == experiment.get_remote_exp_dir():
        print "To execute the experiment: \nCopy: \n\t%s \nTo the target machine in: \n\t%s\n" % (experiment.get_exp_dir(), os.path.dirname(experiment.get_remote_exp_dir())) 
        print OUTPUT_SEPARATOR
    print "Execute the guideline verification jobs from: \n\t%s\n" % (experiment.get_remote_verif_job_dir())
    print OUTPUT_SEPARATOR
    
    
  