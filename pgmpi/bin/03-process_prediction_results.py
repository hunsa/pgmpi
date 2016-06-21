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
import mpiguidelines.helpers.file_helpers as helpers
from mpiguidelines.common_exp_infos import *


def get_nrep_predictions(pred_rawdata_dir):
    assert os.path.isdir(pred_rawdata_dir), "Cannot find prediction results directory %s. Please execute the prediction jobs first with ./bin/runPredictionJobs.py " % (pred_rawdata_dir)

    fieldnames=["test", "nrep", "msize", "last_runtime_sec", "pred_method", "pred_value"]
    nrep_prediction_data = []
    
    for f in os.listdir(pred_rawdata_dir):
        if f.endswith(".dat"):      
            #try:
                results = []
                data = helpers.read_cvs_file(os.path.join(pred_rawdata_dir, f), fieldnames)
                #pprint(data)
                current_test = ""
                for el in data:
                    if current_test == el["test"]+el["msize"]:
                        continue
                    else:
                        current_test = el["test"]+el["msize"]
                
                    duplicate_el = [res for res in results if (res["test"] == el["test"] and res["msize"] == el["msize"]) ]
                    if len(duplicate_el) > 0:
                        continue # already have the results for this (test,msize) tuple
                    else:
                        results.append({k: el[k] for k in ("test", "nrep", "msize")})
                    
                
                for el in results:
                    pred_values = [res for res in nrep_prediction_data if (res["test"] == el["test"] and res["msize"] == el["msize"]) ]
                    #pprint("pred_values")
                    #pprint(pred_values)
                    if len(pred_values) == 1:
                        pred_values[0]["nrep"].append( int(el["nrep"]) )
                    elif len(pred_values) == 0:
                        el["nrep"] = [int(el["nrep"])]
                        
                        nrep_prediction_data.append(el)
                    else:
                        print("An error occurred. Check configuration files")
                        exit(1)
       
    for test in nrep_prediction_data:
        test["max_nrep"] = max(test["nrep"])
        print("[%s][msize=%s] Setting max_nrep=%d (from prediction list %s)" % (test["test"], test["msize"], test["max_nrep"], test["nrep"]))
        
    return nrep_prediction_data


if __name__ == "__main__":

    parser = OptionParser(usage="usage: %prog [options]")

    parser.add_option("-r", "--raw_data_dir",
                       action="store",
                       dest="pred_rawdata_dir",
                       type="string",
                       help="path to prediction raw data directory")
    parser.add_option("-o", "--output_dir",
                       action="store",
                       dest="pred_results_dir",
                       type="string",
                       help="path to prediction processed data directory")

    (options, args) = parser.parse_args()

    if options.pred_rawdata_dir == None:
        print >> sys.stderr, "Prediction raw data directory does not exist. Please create it by running nrep prediction jobs."
        parser.print_help()
        sys.exit(1)
    if options.pred_results_dir == None:
        print >> sys.stderr, "Prediction output directory does not exist."
        parser.print_help()
        sys.exit(1)
        
            
    print "Processing prediction data from %s..." % options.pred_rawdata_dir
    prediction_data = get_nrep_predictions(options.pred_rawdata_dir)
    
    assert len(prediction_data) > 0, "No prediction data found or incorrectly formatted. Generate prediction data first"  
    output_file = os.path.join(options.pred_results_dir, PREDICTION_PROCESSED_OUTPUT_FILENAME)
    helpers.write_json_config_file(output_file, prediction_data)

    print("Prediction data summarized into the %s file" % output_file)

    
    

