
import json
import os
import sys
from datetime import datetime
from mpiguidelines.benchmark import benchmarks as bench
import config_helpers as helpers
from common_exp_infos import *
import machine_config as machine
import shutil
from pprint import pprint
 
def initialize_config_files(expname, exp_base_dir):
    exec_dir_name = expname + "_" + EXEC_BASEDIR
    exp_dir = os.path.join(exp_base_dir, expname)
    assert os.path.isdir(exp_dir)

    exec_dir = os.path.join(exp_dir, exec_dir_name)     
    execconfig_dir = os.path.join(exec_dir, EXEC_DIRS["config"])
    
    for f in os.listdir(os.path.join(exp_dir, CONFIG_BASEDIR)):
        file_path = os.path.join(os.path.join(exp_dir, CONFIG_BASEDIR), f)
        shutil.copy(file_path, execconfig_dir)
    

def get_exp_config_data(expname, exp_base_dir):
    exec_dir_name = expname + "_" + EXEC_BASEDIR
    exp_dir = os.path.join(exp_base_dir, expname)
    assert os.path.isdir(exp_dir)
    
    exec_dir = os.path.join(exp_dir, exec_dir_name) 
    execconfig_dir = os.path.join(exec_dir, EXEC_DIRS["config"])
    config_data = helpers.read_json_config_file(os.path.join(execconfig_dir, expname + ".json"))
    
    return config_data



def generate_input_file_data(config_data, pred_info, max_nrep = 0):
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
                    pred_values = [res for res in pred_info if (res["test"] == bench_func and int(res["msize"]) == msize) ]
                    #pprint(pred_values)
                    if len(pred_values) == 1:
                        run[msize] = {
                                      "nreps": pred_values[0]["max_nrep"]
                                      } 
                    else:
                        run[msize] = {
                                      "nreps": max_nrep
                                      }                   
                tests[bench_func] = run
    
    #pprint(tests)
    return tests



def create_input_file(config_data, pred_info, exec_input_dir, max_nrep = 0):
    
    bench_info = config_data["mach_info"]["benchmark"]
    benchmark = bench.BENCHMARKS[bench_info["type"]](bench_info)
    
    input_data = generate_input_file_data(config_data, pred_info, max_nrep)
    benchmark.generate_input_files(exec_input_dir, 1, input_data)
    
    #print exec_input_dir

def get_nrep_predictions(expname, exp_base_dir):
    pred_dir_name = expname + "_" + PREDICTION_BASEDIR
    exp_dir = os.path.join(exp_base_dir, expname)
    pred_dir = os.path.join(exp_dir, pred_dir_name) 
    pred_results_dir = os.path.join(pred_dir, PREDICTION_DIRS["results"])
    assert os.path.isdir(pred_dir), "Cannot find prediction directory %s" % (pred_dir_name)
    assert os.path.isdir(pred_results_dir), "Cannot find prediction results in %s. Please execute the prediction jobs first with ./bin/runPredictionJobs.py " % (pred_results_dir)

       
    nrep_pred_info = get_nrep_info_from_prediction(pred_results_dir)
    for test in nrep_pred_info:
        test["max_nrep"] = max(test["nrep"])
        print("[%s][msize=%s] Setting max_nrep=%d (from prediction list %s)" % (test["test"], test["msize"], test["max_nrep"], test["nrep"]))
        
    return nrep_pred_info



def create_job_file(config_data, exec_job_dir):
    
    bench_info = config_data["mach_info"]["benchmark"]
    benchmark = bench.BENCHMARKS[bench_info["type"]](bench_info)
    
    print exec_job_dir
        
    # input/output directories on the remote server to set inside the job files
    exec_dirname = os.path.basename(os.path.dirname(exec_job_dir))
    remote_input_dir = os.path.join(
                          os.path.join(config_data["exp_info"]["execution_dir"], exec_dirname),
                                     EXEC_DIRS["input"]
                                     )
    remote_output_dir = os.path.join(
                                     os.path.join(config_data["exp_info"]["execution_dir"], exec_dirname),
                                     EXEC_DIRS["results"]
                                     )

    
    exp_info = config_data["exp_info"]
    mpirun_call = machine.get_mpi_call(exp_info["nodes"], exp_info["nnp"], config_data["mach_info"])
    assert(mpirun_call != ""), "Could not create mpirun call. Please check the informations provided in the machine configuration file"
    
    benchmark.generate_and_write_job_files(exec_job_dir, remote_input_dir, remote_output_dir,
                                  mpirun_call, exp_info["nmpiruns"], exp_info["nodes"], exp_info["nnp"]
                                  )
      


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











