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

from mpiguidelines.common_exp_infos import *
import mpiguidelines.helpers.file_helpers as helpers
from mpiguidelines.machine_setup import *   
from mpiguidelines.benchmark import benchmarks

def create_input_file(glconfig_data, pred_info, benchmark, exec_input_dir, max_nrep = 0):
    
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
                if "bench_func" in tests.keys():
                    run = tests[bench_func]
                    
                if not msize in run.keys():
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
    
    benchmark.generate_input_files(exec_input_dir, 1, tests)    
    print "Done."


def create_job_file(exp_name, expconfig_data, benchmark, machine_configurator, exp_job_dir):
        
    print "Generating job files in %s..." % exp_job_dir
    
    exp_output_dir = machine_configurator.get_exp_output_dir()
        
    # input/output directories on the remote server to set inside the job files
    exp_dirname = os.path.basename(os.path.dirname(exp_job_dir))
    remote_input_dir = os.path.join(
                          os.path.join(exp_output_dir, exp_dirname),
                                     EXEC_DIRS["input"]
                                     )
    remote_output_dir = os.path.join(
                                     os.path.join(exp_output_dir, exp_dirname),
                                     EXEC_DIRS["raw_data"]
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
    parser.add_option("-m", "--machconf",
                        action="store",
                        dest="machconf",
                        type="string",
                        help="path to machine/benchmark configuration file")
    parser.add_option("-p", "--predfile",
                       action="store",
                       dest="predfile",
                       type="string",
                       help="summarized prediction data")

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
    
    if options.predfile == None:
        print >> sys.stderr, "Prediction output data file not specified"
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
  

#    expgen.initialize_config_files(expname, exp_base_dir)
    
    
    exec_dir_name = expname + "_" + EXEC_BASEDIR
    exp_dir = os.path.join(exp_base_dir, expname)
    assert os.path.isdir(exp_dir), "Cannot find experiment execution directory %s" % (exec_dir_name)
        
    exec_dir = os.path.join(exp_dir, exec_dir_name) 
    exec_input_dir = os.path.join(exec_dir, EXEC_DIRS["input"])
    exec_job_dir = os.path.join(exec_dir, EXEC_DIRS["jobs"])
    execconfig_dir = os.path.join(exec_dir, EXEC_DIRS["config"])
    
    if options.predfile != None and os.path.exists(options.predfile):
        shutil.copy(options.predfile, execconfig_dir)
        prediction_data = helpers.read_json_config_file(options.predfile)
        
    max_nrep = 0
    if options.predfile == None or len(prediction_data) == 0:
        try:
            prediction_cfg = config_data["exp_info"]["prediction"]
            try:
                max_nrep = prediction_cfg["max"]
            except KeyError:
                print >> sys.stderr, "No maximum nrep value specified in the configuration file %s." % (config_file_name)
                max_nrep = 1000
        except KeyError:
            print >> sys.stderr, "No prediction data specified in configuration file %s." % (config_file_name)
            max_nrep = 1000

        print >> sys.stderr, "Warning: no prediction data found or incorrectly formatted. Using the predefined maximum runs %d" % (max_nrep)   

     
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
    except Exception, err:
        print 'ERROR: Cannot instantiate class defined in %s: \n' % options.machconf, str(err)
        exit(1)
    
    
    
    glconfig_data = helpers.read_json_config_file(options.glconf)
    expconfig_data = helpers.read_json_config_file(options.expconf)
    
    bench_path  = machine_configurator.get_bench_path()
    bench_type  = machine_configurator.get_bench_type()
    benchmark = benchmarks.BENCHMARKS[bench_type](bench_path)
    
    
    create_input_file(glconfig_data, prediction_data, benchmark, exec_input_dir, max_nrep)
    create_job_file(expname, expconfig_data, benchmark, machine_configurator, exec_job_dir)

    
    