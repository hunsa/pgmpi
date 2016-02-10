
import json
import os
import sys
from datetime import datetime
from mpiguidelines.benchmark import benchmarks as bench
from mpiguidelines.helpers import file_helpers as helpers
from common_exp_infos import *
import machine_config as machine
import shutil
import pprint
 
def initialize_config_files(expname, exp_base_dir):
    pred_dir_name = expname + "_" + PREDICTION_BASEDIR
    exp_dir = os.path.join(exp_base_dir, expname)
    assert os.path.isdir(exp_dir)

    pred_dir = os.path.join(exp_dir, pred_dir_name)     
    predconfig_dir = os.path.join(pred_dir, PREDICTION_DIRS["config"])
    
    for f in os.listdir(os.path.join(exp_dir, CONFIG_BASEDIR)):
        file_path = os.path.join(os.path.join(exp_dir, CONFIG_BASEDIR), f)
        shutil.copy(file_path, predconfig_dir)
    

def get_exp_config_data(expname, exp_base_dir):
    pred_dir_name = expname + "_" + PREDICTION_BASEDIR
    exp_dir = os.path.join(exp_base_dir, expname)
    assert os.path.isdir(exp_dir)
    
    pred_dir = os.path.join(exp_dir, pred_dir_name) 
    predconfig_dir = os.path.join(pred_dir, PREDICTION_DIRS["config"])
    config_data = helpers.read_json_config_file(os.path.join(predconfig_dir, expname + ".json"))
    
    return config_data



def generate_input_file_data(config_data):
    tests = {}
    guidelines = config_data["guidelines"]
    for guideline in guidelines:
        for bench_func in guideline["bench_mpicalls"]:
            for msize in guideline["msizes"]:   
                try: 
                    run = tests[bench_func]
                except KeyError:
                    run = {}
                    
                try: 
                    ms = run[msize]
                except KeyError:                   
                    run[msize] = {
                            "nreps": 0
                          }                   
                tests[bench_func] = run
    
    #pprint.pprint(tests)
    return tests



def create_input_file(config_data, pred_input_dir):

    assert os.path.isdir(pred_input_dir)

    bench_info = config_data["mach_info"]["benchmark"]
    benchmark = bench.BENCHMARKS[bench_info["type"]](bench_info)
    
    print "Generating input data in %s..." % pred_input_dir
    
    input_data = generate_input_file_data(config_data)
    benchmark.generate_input_files(pred_input_dir, 1, input_data)
    print "Done."


def create_job_file(config_data, pred_job_dir):
        
    print "Generating job files in %s..." % pred_job_dir
    
    execution_dir = helpers.get_execution_dir(config_data)
    
    bench_info = config_data["mach_info"]["benchmark"]
    benchmark = bench.BENCHMARKS[bench_info["type"]](bench_info)
        
        
    # input/output directories on the remote server to set inside the job files
    pred_dir_name = config_data["exp_name"] + "_" + PREDICTION_BASEDIR
    remote_input_dir = os.path.join(
                          os.path.join(execution_dir, pred_dir_name),
                                     PREDICTION_DIRS["input"]
                                     )
    remote_output_dir = os.path.join(
                                     os.path.join(execution_dir, pred_dir_name),
                                     PREDICTION_DIRS["raw_data"]
                                     )


    exp_info = config_data["exp_info"]
    
    mpirun_call = machine.get_mpi_call(exp_info["nodes"], exp_info["nnp"], config_data["mach_info"])
    assert(mpirun_call != ""), "Could not create mpirun call. Please check the informations provided in the machine configuration file"
    
    job_header = machine.get_jobfile_header(exp_info["nodes"], exp_info["nnp"], config_data["mach_info"], remote_output_dir)
    mpi_call_suffix = machine.get_mpi_call_suffix(config_data["mach_info"], remote_output_dir)
    mpirun_call = mpirun_call + mpi_call_suffix
    
    benchmark.generate_and_write_prediction_job_files(pred_job_dir, remote_input_dir, remote_output_dir,
                                  mpirun_call, exp_info["nodes"], exp_info["nnp"],
                                  exp_info["prediction"], job_header
                                  )
    print "Done."   
    
    
    
def get_nrep_info_from_prediction(pred_results_dir):
    
    fieldnames=["test", "nrep", "msize", "last_runtime_sec", "pred_method", "pred_value"]
    nrep_prediction_data = []
    
    for f in os.listdir(pred_results_dir):
        if f.endswith(".dat"):      
            #try:
                results = []
                data = helpers.read_cvs_file(os.path.join(pred_results_dir, f), fieldnames)
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
                    #pprint("all data")
                    #pprint(nrep_prediction_data)

            #except Exception:
            #    print ("Prediction results file incorrectly formatted - file path: %s" % (os.path.join(pred_results_dir, f)))
    return nrep_prediction_data



def get_nrep_predictions(pred_results_dir):

    assert os.path.isdir(pred_results_dir), "Cannot find prediction results in %s. Please execute the prediction jobs first with ./bin/runPredictionJobs.py " % (pred_results_dir)

       
    nrep_pred_info = get_nrep_info_from_prediction(pred_results_dir)
    for test in nrep_pred_info:
        test["max_nrep"] = max(test["nrep"])
        print("[%s][msize=%s] Setting max_nrep=%d (from prediction list %s)" % (test["test"], test["msize"], test["max_nrep"], test["nrep"]))
        
    return nrep_pred_info









