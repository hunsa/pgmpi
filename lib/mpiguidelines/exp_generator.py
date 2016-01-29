
import json
import os
import sys
from datetime import datetime
from mpiguidelines.benchmark import benchmarks as bench
from mpiguidelines.helpers import file_helpers as helpers
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
    
    assert os.path.isdir(exec_input_dir)

    bench_info = config_data["mach_info"]["benchmark"]
    benchmark = bench.BENCHMARKS[bench_info["type"]](bench_info)
    
    print "Generating input data in %s..." % exec_input_dir

    input_data = generate_input_file_data(config_data, pred_info, max_nrep)
    benchmark.generate_input_files(exec_input_dir, 1, input_data)
    
    print "Done."




def create_job_file(config_data, exec_job_dir):
    
    print "Generating job files in %s..." % exec_job_dir
    
    bench_info = config_data["mach_info"]["benchmark"]
    benchmark = bench.BENCHMARKS[bench_info["type"]](bench_info)
    execution_dir = helpers.get_execution_dir(config_data)
        
    # input/output directories on the remote server to set inside the job files
    exec_dirname = os.path.basename(os.path.dirname(exec_job_dir))
    remote_input_dir = os.path.join(
                          os.path.join(execution_dir, exec_dirname),
                                     EXEC_DIRS["input"]
                                     )
    remote_output_dir = os.path.join(
                                     os.path.join(execution_dir, exec_dirname),
                                     EXEC_DIRS["raw_data"]
                                     )

    
    exp_info = config_data["exp_info"]
    mpirun_call = machine.get_mpi_call(exp_info["nodes"], exp_info["nnp"], config_data["mach_info"])
    assert(mpirun_call != ""), "Could not create mpirun call. Please check the informations provided in the machine configuration file"
    
    benchmark.generate_and_write_job_files(exec_job_dir, remote_input_dir, remote_output_dir,
                                  mpirun_call, exp_info["nmpiruns"], exp_info["nodes"], exp_info["nnp"]
                                  )
    print "Done."  
    


