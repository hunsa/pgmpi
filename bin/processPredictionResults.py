#! /usr/bin/env python

import sys
import os
from pprint import pprint

# in bin
base_path = os.path.dirname( os.path.realpath( sys.argv[0] ) )
#cd ..
base_path = os.path.dirname( base_path )
lib_path = os.path.join( base_path, "lib" )
sys.path.append(lib_path)

from optparse import OptionParser
import mpiguidelines.prediction_exp_generator as predgen
import mpiguidelines.helpers.file_helpers as helpers
from mpiguidelines.common_exp_infos import *

if __name__ == "__main__":

    parser = OptionParser(usage="usage: %prog [options]")

    parser.add_option("-d", "--expdir",
                       action="store",
                       dest="base_expdir",
                       type="string",
                       help="path to prediction experiment directory")

    (options, args) = parser.parse_args()

    if options.base_expdir == None:
        print >> sys.stderr, "Prediction experiment directory does not exist. Please create it using the ./bin/setupExp script"
        parser.print_help()
        sys.exit(1)
    else:
        pred_dir = os.path.abspath(options.base_expdir)
        
    pred_results_dir = os.path.join(pred_dir, PREDICTION_RESULTS_DIRS["summary"])
    pred_rawdata_dir = os.path.join(pred_dir, PREDICTION_DIRS["raw_data"])
    
    print "Processing prediction data from %s..." % pred_rawdata_dir
    prediction_data = predgen.get_nrep_predictions(pred_rawdata_dir)
    
    assert len(prediction_data) > 0, "No prediction data found or incorrectly formatted. Generate prediction data first"  
    output_file = os.path.join(pred_results_dir, PREDICTION_PROCESSED_OUTPUT_FILENAME)
    helpers.write_json_config_file(output_file, prediction_data)

    print("Prediction data summarized into the %s file" % output_file)

    
    

