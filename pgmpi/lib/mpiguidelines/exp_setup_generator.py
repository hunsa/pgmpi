
import json
import os
import sys
from datetime import datetime
from mpiguidelines.benchmark import benchmarks as bench
from mpiguidelines.helpers import file_helpers as helpers
from common_exp_infos import *
import shutil


def write_full_exp_file(exp_dir, config_data):
    ret = helpers.create_local_dir(exp_dir)
    if not ret:
        print ("Specify another experiment name or path to create a new experiment.\n")
        sys.exit(1)        
    

    config_file_path = os.path.join(exp_dir, config_data["exp_name"] + ".json")
    helpers.write_json_config_file(config_file_path, config_data)
    
    
def create_exp_dir_structure(expname, exp_base_dir):
    
    exp_dir = os.path.join(exp_base_dir, expname)
    ret = helpers.create_local_dir(exp_dir)
    if not ret:
        print ("Specify another experiment name or path to create a new experiment.\n")
        sys.exit(1) 
    
    # create prediction directory tree
    pred_dir_name = expname + "_" + PREDICTION_BASEDIR
    pred_dir = os.path.join(exp_dir, pred_dir_name)
    helpers.create_local_dir(pred_dir)
    for d in PREDICTION_DIRS.values():
        helpers.create_local_dir(os.path.join(pred_dir, d))
    for d in PREDICTION_RESULTS_DIRS.values():
        helpers.create_local_dir(os.path.join(pred_dir, d))
    
    # create experiment execution directory tree
    exec_dir_name = expname + "_" + EXEC_BASEDIR
    exec_dir = os.path.join(exp_dir, exec_dir_name)
    helpers.create_local_dir(exec_dir)
    for d in EXEC_DIRS.values():
        helpers.create_local_dir(os.path.join(exec_dir, d))

    # create experiment results directory tree
    for d in EXEC_RESULTS_DIRS.values():
        helpers.create_local_dir(os.path.join(exp_dir, d))


    #create initial configuration directory
    conf_dir = os.path.join(exp_dir, CONFIG_BASEDIR)
    helpers.create_local_dir(conf_dir)
    
 
def create_init_config_files(expname, exp_base_dir, glconf, expconf, machconf):
    exp_dir = os.path.join(exp_base_dir, expname)
    assert os.path.isdir(exp_dir)
    
    shutil.copy(glconf, os.path.join(exp_dir, CONFIG_BASEDIR))
    shutil.copy(expconf, os.path.join(exp_dir, CONFIG_BASEDIR))
    shutil.copy(machconf, os.path.join(exp_dir, CONFIG_BASEDIR))
    
    
def generate_complete_exp_data(expname, exp_base_dir, glconf, expconf, machconf, local_exec = False):
    exp_dir = os.path.join(exp_base_dir, expname)
    assert os.path.isdir(exp_dir)
    
    config_data = {}
    config_data["exp_info"] = helpers.read_json_config_file(expconf)
    config_data["mach_info"] = helpers.read_json_config_file(machconf)
    config_data["guidelines"] = helpers.read_json_config_file(glconf)
    
    config_data["exp_name"] = os.path.basename(exp_dir)
    config_data["exp_info"]["exp_base_dir"] = os.path.dirname(exp_dir)
    config_data = translate_and_set_guideline_names(config_data)
    
    config_data["exp_info"]["local_exec"] = False
    if local_exec:
        config_data["exp_info"]["local_exec"] = True
    return config_data
    
    
def write_complete_exp_data(expname, exp_base_dir, config_data):
    exp_dir = os.path.join(exp_base_dir, expname)
    assert os.path.isdir(exp_dir)
    
    config_data_file = os.path.join(os.path.join(exp_dir, CONFIG_BASEDIR), config_data["exp_name"] + ".json")
    helpers.write_json_config_file(config_data_file, config_data)
    
    
    
def translate_and_set_guideline_names(config_data):
    
    #config_data = helpers.read_json_config_file(config_file)
    bench_info = config_data["mach_info"]["benchmark"]
    benchmark = bench.BENCHMARKS[bench_info["type"]](bench_info)

    new_guidelines = []
    guidelines = config_data["guidelines"]
    for guideline in guidelines:
        calls = [guideline["orig"] ]
        if "mock" in guideline:
            calls.append(guideline["mock"])
        
        translated_calls = benchmark.translate_guideline(calls)
        # use the MPI call names as they were defined, if no benchmark-specific calls exist
        if not translated_calls:
            translated_calls = calls
        
        guideline["bench_mpicalls"] = translated_calls
        new_guidelines.append(guideline)
    config_data["guidelines"] = new_guidelines
    
    return config_data   
    
    
    