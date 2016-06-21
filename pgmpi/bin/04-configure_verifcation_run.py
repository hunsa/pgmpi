#! /usr/bin/env python

import sys
import os
import shutil
import imp
from optparse import OptionParser
from inspect import isclass

# in bin
base_path = os.path.dirname( os.path.realpath( sys.argv[0] ) )
#cd ..
base_path = os.path.dirname( base_path )
lib_path = os.path.join( base_path, "lib" )
sys.path.append(lib_path)

from mpiguidelines import file_helpers
from mpiguidelines.benchmark import benchmarks
from mpiguidelines import common_exp_infos
from mpiguidelines import machine_setup  

MAX_NREPS = 1000


def create_input_file(glconfig_data, pred_data, benchmark, exec_input_dir, max_nrep = 0):
    
    assert os.path.isdir(exec_input_dir)
    print "Generating input data in %s..." % exec_input_dir

    tests = {}
    for guideline in glconfig_data:
        bench_funcs = []
        if "orig" in guideline:
            bench_funcs.append(guideline["orig"])
        if "mock" in guideline:
            bench_funcs.append(guideline["mock"])
            
        for bench_func in bench_funcs:
            for msize in guideline["msizes"]:   
                run = {}
                translated_func_name = benchmark.translate_name(bench_func)
                
                if translated_func_name in tests.keys():
                    run = tests[translated_func_name]
                    
                if not msize in run.keys():
                    # default value for nreps
                    run[msize] = {  
                                "nreps": max_nrep
                                 }   
                    
                    if pred_data:
                        pred_values = [] 
                        for res in pred_data:
                            if res["test"] == translated_func_name and int(res["msize"]) == msize:
                                pred_values.append(res)
                                
                        # replace nreps with predicted value if it exists for the current msize
                        if len(pred_values) > 0:
                            run[msize] = {
                                          "nreps": pred_values[0]["max_nrep"]
                                          }                      
                tests[translated_func_name] = run
                
    benchmark.generate_input_files(exec_input_dir, 1, tests)    
    print "Done."


def create_job_file(expname, expconfig_data, benchmark, machine_configurator, exp_job_dir):
        
    print "Generating job files in %s..." % exp_job_dir
    
    exp_output_basedir = machine_configurator.get_exp_output_dir()
    exp_output_dir = os.path.join(exp_output_basedir, expname)
        
    # input/output directories on the remote server to set inside the job files
    exp_dirname = os.path.basename(os.path.dirname(exp_job_dir))
    remote_input_dir = os.path.join(
                          os.path.join(exp_output_dir, exp_dirname),
                                     common_exp_infos.EXEC_DIRS["input"]
                                     )
    remote_output_dir = os.path.join(
                                     os.path.join(exp_output_dir, exp_dirname),
                                     common_exp_infos.EXEC_DIRS["raw_data"]
                                     )
     
    bench_args = benchmark.get_verification_bench_args(remote_input_dir, expconfig_data)
    bench_binary = benchmark.get_verification_bench_binary()
    
    machine_configurator.create_jobs(expconfig_data, bench_binary, bench_args, remote_output_dir, exp_job_dir)
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
    parser.add_option("-m", "--machcode",
                        action="store",
                        dest="machcode",
                        type="string",
                        help="path to machine-specific class file")
    parser.add_option("-p", "--predfile",
                       action="store",
                       dest="predfile",
                       type="string",
                       help="summarized prediction data")

    (options, args) = parser.parse_args()


    if options.glconf == None or not os.path.exists(options.glconf):
        print >> sys.stderr, "ERROR: Guidelines configuration file invalid"
        parser.print_help()
        sys.exit(1)

    if options.expconf == None or not os.path.exists(options.expconf):
        print >> sys.stderr, "ERROR: Experiment configuration file invalid"
        parser.print_help()
        sys.exit(1)

    if options.machcode == None or not os.path.exists(options.machcode):
        print >> sys.stderr, "ERROR: Machine class file invalid"
        parser.print_help()
        sys.exit(1)
    
    if options.predfile == None:
        print >> sys.stderr, "ERROR: Prediction output data file not specified"
        parser.print_help()
        sys.exit(1)
    
    if options.expname == None:
        print >> sys.stderr, "ERROR: Experiment name not specified"
        parser.print_help()
        sys.exit(1)
    expname = options.expname

    if options.base_expdir == None:
        print >> sys.stderr, "ERROR: Experiment directory does not exist. Please create it using the ./bin/setupExp script"
        parser.print_help()
        sys.exit(1)
    else:
        exp_base_dir = os.path.abspath(options.base_expdir)
  
    
    exec_dir_name = expname + "_" + common_exp_infos.EXEC_BASEDIR
    exp_dir = os.path.join(exp_base_dir, expname)
    assert os.path.isdir(exp_dir), "Cannot find experiment execution directory %s" % (exec_dir_name)
        
    exec_dir = os.path.join(exp_dir, exec_dir_name) 
    exec_input_dir = os.path.join(exec_dir, common_exp_infos.EXEC_DIRS["input"])
    exec_job_dir = os.path.join(exec_dir, common_exp_infos.EXEC_DIRS["jobs"])
    
    # load configuration files
    glconfig_data = file_helpers.read_json_config_file(options.glconf)
    expconfig_data = file_helpers.read_json_config_file(options.expconf)
    
    # load prediction results
    prediction_data = None
    if options.predfile != None and os.path.exists(options.predfile):
    #    shutil.copy(options.predfile, execconfig_dir)
        prediction_data = file_helpers.read_json_config_file(options.predfile)
    
    max_nrep = MAX_NREPS
    if options.predfile == None or prediction_data == None or len(prediction_data) == 0:
        # retrieve max nrep from the initial experiment configuration
        if "prediction" in expconfig_data:
            prediction_cfg = expconfig_data["prediction"]
            if "max" in prediction_cfg:
                max_nrep = prediction_cfg["max"]
            else:
                print >> sys.stderr, "No maximum nrep value specified in the configuration file %s." % (options.expconf)
                max_nrep = MAX_NREPS
        else:
            print >> sys.stderr, "No prediction data specified in configuration file %s." % (options.expconf)
            max_nrep = MAX_NREPS
        print >> sys.stderr, "Warning: no prediction data found or incorrectly formatted. Using the predefined maximum runs %d" % (max_nrep)   

     
    # load machine setup class from specified file    
    mach_conf_module = imp.load_source("machconf", options.machcode)   
    mach_class_list = []
    for name, cls in mach_conf_module.__dict__.items():
        if isclass(cls) and issubclass(cls, machine_setup.PGMPIMachineConfigurator) and not issubclass(machine_setup.PGMPIMachineConfigurator, cls):
            mach_class_list.append(cls)
    
    if len(mach_class_list) == 0:
        print >> sys.stderr, "ERROR: Cannot load machine configuration class from: %s" % options.machcode 
        parser.print_help()
        sys.exit(1)
    
    if len(mach_class_list) > 1:
        print >> sys.stderr, "ERROR: Multiple machine configuration classes found in: %s" % options.machcode 
        parser.print_help()
        sys.exit(1)    
   
    # instantiate class
    try:
        machine_configurator = mach_class_list[0]()
    except Exception, err:
        print 'ERROR: Cannot instantiate class defined in %s: \n' % options.machcode, str(err)
        exit(1)
    
    
    bench_path  = machine_configurator.get_bench_path()
    bench_type  = machine_configurator.get_bench_type()
    benchmark = benchmarks.BENCHMARKS[bench_type](bench_path)
    
    
    create_input_file(glconfig_data, prediction_data, benchmark, exec_input_dir, max_nrep)
    create_job_file(expname, expconfig_data, benchmark, machine_configurator, exec_job_dir)

    
    