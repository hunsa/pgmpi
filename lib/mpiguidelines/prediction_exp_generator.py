
import json
import os
import sys
from datetime import datetime
from mpiguidelines.benchmark import benchmarks as bench
import config_helpers as helpers
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
    
    pprint.pprint(tests)
    return tests



def create_input_file(expname, exp_base_dir):
    pred_dir_name = expname + "_" + PREDICTION_BASEDIR
    exp_dir = os.path.join(exp_base_dir, expname)
    assert os.path.isdir(exp_dir)
    
    pred_dir = os.path.join(exp_dir, pred_dir_name) 
    pred_input_dir = os.path.join(pred_dir, PREDICTION_DIRS["input"])
    
    config_data = get_exp_config_data(expname, exp_base_dir)
    
    bench_info = config_data["mach_info"]["benchmark"]
    benchmark = bench.BENCHMARKS[bench_info["type"]](bench_info)
    
    print pred_input_dir
    
    input_data = generate_input_file_data(config_data)
    benchmark.generate_input_files(pred_input_dir, 1, input_data)



def create_job_file(expname, exp_base_dir):
    pred_dir_name = expname + "_" + PREDICTION_BASEDIR
    exp_dir = os.path.join(exp_base_dir, expname)
    assert os.path.isdir(exp_dir)
    
    pred_dir = os.path.join(exp_dir, pred_dir_name) 
    pred_job_dir = os.path.join(pred_dir, PREDICTION_DIRS["jobs"])
    
    config_data = get_exp_config_data(expname, exp_base_dir)
    
    bench_info = config_data["mach_info"]["benchmark"]
    benchmark = bench.BENCHMARKS[bench_info["type"]](bench_info)
    
    print pred_job_dir
        
    # input/output directories on the remote server to set inside the job files
    remote_input_dir = os.path.join(
                          os.path.join(config_data["exp_info"]["execution_dir"], pred_dir_name),
                                     PREDICTION_DIRS["input"]
                                     )
    remote_output_dir = os.path.join(
                                     os.path.join(config_data["exp_info"]["execution_dir"], pred_dir_name),
                                     PREDICTION_DIRS["results"]
                                     )

    print config_data["exp_info"]["execution_dir"]
    exp_info = config_data["exp_info"]
    mpirun_call = machine.get_mpi_call(exp_info["nodes"], exp_info["nnp"], config_data["mach_info"])
    assert(mpirun_call != ""), "Could not create mpirun call. Please check the informations provided in the machine configuration file"
    
    benchmark.generate_and_write_prediction_job_files(pred_job_dir, remote_input_dir, remote_output_dir,
                                  mpirun_call, exp_info["nodes"], exp_info["nnp"],
                                  exp_info["prediction"]
                                  )
    
    
    
    




