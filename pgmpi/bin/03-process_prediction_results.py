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


def get_nrep_predictions(pred_rawdata_dir):
    assert os.path.isdir(pred_rawdata_dir), "Cannot find prediction results directory %s. Please execute the prediction jobs first with ./bin/runPredictionJobs.py " % (pred_rawdata_dir)

    fieldnames=["test", "nrep", "msize", "last_runtime_sec", "pred_method", "pred_value"]
    nrep_prediction_data = {}
    
    for f in os.listdir(pred_rawdata_dir):
        if f.endswith(".dat"):      
            data = file_helpers.read_cvs_file(os.path.join(pred_rawdata_dir, f), fieldnames)
            current_test = None
            for data_row in data:
                if current_test == (data_row["test"], data_row["msize"]):
                    continue    # skip this line, already read data for this (test,msize) tuple
                else:
                    current_test = (data_row["test"], data_row["msize"])
                
                    if len(nrep_prediction_data) > 0 and current_test in nrep_prediction_data.keys():
                        # already have the results for this (test,msize) tuple from a different file
                        # add current nrep value
                        test_data = nrep_prediction_data[current_test]
                        test_data.append(int(data_row["nrep"]))
                    else:
                        # create nrep record for the current test
                        nrep_prediction_data[current_test] = [int(data_row["nrep"])] 
                        
    # reformat data into a json-compatible structure
    # replace list of nreps with the maximum value for each (test, msize) tuple
    nrep_prediction_list = []
    for test in nrep_prediction_data.keys():
        maxnreps = max(nrep_prediction_data[test])
        print("[%s][msize=%s] Setting max_nrep=%d " % (test[0], test[1], maxnreps))
        
        nrep_prediction_list.append({
                                     "test" : test[0],
                                     "msize": test[1],
                                     "max_nrep": maxnreps
                                    })
        
    return nrep_prediction_list


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
    
    pred_rawdata_dir = experiment.get_local_pred_output_dir()
    processed_dir = experiment.get_local_pred_processed_dir()

    print "Processing prediction data from %s..." % pred_rawdata_dir
    prediction_data = get_nrep_predictions(pred_rawdata_dir)
    
    assert len(prediction_data) > 0, "No prediction data found or incorrectly formatted. Generate prediction data first"  
    output_file = os.path.join(processed_dir, common_exp_infos.PREDICTION_PROCESSED_OUTPUT_FILENAME)
    file_helpers.write_json_config_file(output_file, prediction_data)

    print("Prediction data summarized into the %s file" % output_file)

    
    

