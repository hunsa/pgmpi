#! /usr/bin/env python

import sys
import os
import shutil
import imp
import inspect
from optparse import OptionParser
from inspect import isclass

# in bin
base_path = os.path.dirname( os.path.realpath( sys.argv[0] ) )
#cd ..
base_path = os.path.dirname( base_path )
lib_path = os.path.join( base_path, "lib" )
sys.path.append(lib_path)

from mpiguidelines.common_exp_infos import *
import mpiguidelines.helpers.file_helpers as helpers
from machine_setup import *   
from mpiguidelines.benchmark import benchmarks

 
def initialize_config_files(glconf_file, expconf_file, expname, exp_base_dir):
    pred_dir_name = expname + "_" + PREDICTION_BASEDIR
    exp_dir = os.path.join(exp_base_dir, expname)
    assert os.path.isdir(exp_dir)

    pred_dir = os.path.join(exp_dir, pred_dir_name)     
    predconfig_dir = os.path.join(pred_dir, PREDICTION_DIRS["config"])
    
    for f in os.listdir(os.path.join(exp_dir, CONFIG_BASEDIR)):
        file_path = os.path.join(os.path.join(exp_dir, CONFIG_BASEDIR), f)
        shutil.copy(file_path, predconfig_dir)
    
 
# format for input data: { function_name1: { msize1 : { "nreps" : 10},
#                                             msize2 : { "nreps" : 20},
#                                          },
#                          function_name2 ......
#                           }
def format_benchmark_input(guidelines):
    tests = {}
    for guideline in guidelines:
        bench_funcs = []
        if "orig" in guideline:
            bench_funcs.append(guideline["orig"])
        if "mock" in guideline:
            bench_funcs.append(guideline["mock"])
        for bench_func in bench_funcs:
            for msize in guideline["msizes"]:   
                run = {}
                if "bench_func" in tests.keys():
                    run = tests[bench_func]
                    
                if not msize in run.keys():
                    run[msize] = {
                            "nreps": 0
                          }       
                tests[bench_func] = run
    
    print tests
    return tests



def create_input_file(glconfig_data, benchmark, pred_input_dir):

    assert os.path.isdir(pred_input_dir)
    
    print "Generating input files in %s..." % pred_input_dir
    
    input_data = format_benchmark_input(glconfig_data)
    benchmark.generate_input_files(pred_input_dir, 1, input_data)
    print "Done."


def create_job_file(exp_name, expconfig_data, benchmark, machine_configurator, pred_job_dir):
        
    print "Generating job files in %s..." % pred_job_dir
    
    exp_output_dir = machine_configurator.get_exp_output_dir()
        
    # input/output directories on the remote server to set inside the job files
    pred_dir_name = exp_name + "_" + PREDICTION_BASEDIR
    remote_input_dir = os.path.join(
                          os.path.join(exp_output_dir, pred_dir_name),
                                     PREDICTION_DIRS["input"]
                                     )
    remote_output_dir = os.path.join(
                                     os.path.join(exp_output_dir, pred_dir_name),
                                     PREDICTION_DIRS["raw_data"]
                                     )
        
    prediction_params = expconfig_data["prediction"]
    assert(prediction_params["max"] > 0), "Specify a maximum number of repetitions for the nrep prediction algorithm"
    for method in prediction_params["methods"]:
        assert(method in ["rse", "cov_mean", "cov_median"]), "Specify a defined prediction method (one of res, cov_mean, cov_median)"
    assert(len(prediction_params["thresholds"]) == len(prediction_params["methods"])), \
                    "The number of thresholds has to match the number of specified prediction methods"
    assert(len(prediction_params["windows"]) == len(prediction_params["methods"])),   \
                    "The number of prediction windows has to match the number of specified prediction methods"
        
        
    bench_args = benchmark.get_prediction_bench_args(remote_input_dir, expconfig_data)
    bench_prediction_binary = benchmark.get_prediction_bench_binary()
    machine_configurator.create_jobs(expconfig_data, bench_prediction_binary, bench_args, remote_output_dir, pred_job_dir)
    print "Done."   
    
    

if __name__ == "__main__":

    parser = OptionParser(usage="usage: %prog [options]")

    parser.add_option("-n", "--expname",
                       action="store",
                       dest="expname",
                       type="string",
                       help="unique experiment name")
    parser.add_option("-d", "--expdir",
                       action="store",
                       dest="base_expdir",
                       type="string",
                       help="path to local experiment directory")
    parser.add_option("-g", "--glconf",
                       action="store",
                       dest="glconf",
                       type="string",
                       help="path to guidelines config file")
    parser.add_option("-e", "--expconf",
                       action="store",
                       dest="expconf",
                       type="string",
                       help="path to exp config file")
    parser.add_option("-m", "--machconf",
                        action="store",
                        dest="machconf",
                        type="string",
                        help="path to machine/benchmark configuration file")

    (options, args) = parser.parse_args()


    if options.glconf == None or not os.path.exists(options.glconf):
        print >> sys.stderr, "Guidelines configuration file invalid"
        parser.print_help()
        sys.exit(1)

    if options.expconf == None or not os.path.exists(options.expconf):
        print >> sys.stderr, "Experiment configuration file invalid"
        parser.print_help()
        sys.exit(1)

    if options.machconf == None or not os.path.exists(options.machconf):
        print >> sys.stderr, "Machine configuration file invalid"
        parser.print_help()
        sys.exit(1)

    if options.expname == None:
        print >> sys.stderr, "Experiment name not specified"
        parser.print_help()
        sys.exit(1)
    expname = options.expname

    if options.base_expdir == None:
        print >> sys.stderr, "Experiment directory does not exist. Please create it using the ./bin/setupExp script"
        parser.print_help()
        sys.exit(1)
    else:
        exp_base_dir = os.path.abspath(options.base_expdir)
    
    initialize_config_files(options.glconf, options.expconf, expname, exp_base_dir)
    
    exec_dir_name = expname + "_" + PREDICTION_BASEDIR
    exp_dir = os.path.join(exp_base_dir, expname)
    assert os.path.isdir(exp_dir), "Cannot find experiment execution directory %s" % (exec_dir_name)
        
    exec_dir = os.path.join(exp_dir, exec_dir_name) 
    exec_input_dir = os.path.join(exec_dir, PREDICTION_DIRS["input"])
    exec_job_dir = os.path.join(exec_dir, PREDICTION_DIRS["jobs"])
        
    
    # load machine setup class from specified file    
    mach_conf_module = imp.load_source("machconf", options.machconf)   
    mach_class_list = []
    for name, cls in mach_conf_module.__dict__.items():
        if isclass(cls) and issubclass(cls, PGMPIMachineConfigurator) and not issubclass(PGMPIMachineConfigurator, cls):
            mach_class_list.append(cls)
    
    if len(mach_class_list) == 0:
        print >> sys.stderr, "Cannot load machine configuration class from: %s" % options.machconf 
        parser.print_help()
        sys.exit(1)
    
    if len(mach_class_list) > 1:
        print >> sys.stderr, "Multiple machine configuration classes found in: %s" % options.machconf 
        parser.print_help()
        sys.exit(1)    
    
    # instantiate class
    try:
        machine_configurator = mach_class_list[0]()
        print machine_configurator
    except Exception, err:
        print 'ERROR: Cannot instantiate class defined in %s: \n' % options.machconf, str(err)
        exit(1)
    
    glconfig_data = helpers.read_json_config_file(options.glconf)
    expconfig_data = helpers.read_json_config_file(options.expconf)
    
    bench_path  = machine_configurator.get_bench_path()
    bench_type  = machine_configurator.get_bench_type()
    benchmark = benchmarks.BENCHMARKS[bench_type](bench_path)
    
    
    create_input_file(glconfig_data, benchmark, exec_input_dir)
    create_job_file(expname, expconfig_data, benchmark, machine_configurator, exec_job_dir)

    
    

