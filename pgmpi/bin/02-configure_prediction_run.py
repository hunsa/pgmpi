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

from mpiguidelines import file_helpers
from mpiguidelines.benchmark import benchmarks
from mpiguidelines import common_exp_infos 


def format_input_data(glconfig_data):  
    tests = {}
    # format input data: { function_name1: { msize1 : { "nreps" : 10},
    #                                             msize2 : { "nreps" : 20},
    #                                          },
    #                          function_name2 ......
    #                           }
    for guideline in glconfig_data:
        bench_funcs = []
        if "orig" in guideline:
            bench_funcs.append(guideline["orig"])
        if "mock" in guideline:
            bench_funcs.append(guideline["mock"])
        for bench_func in bench_funcs:
            for msize in guideline["msizes"]:   
                run = {}
                if bench_func in tests.keys():
                    run = tests[bench_func]
                    
                if not msize in run.keys():
                    run[msize] = {
                            "nreps": 0
                          }       
                tests[bench_func] = run
    return tests
    
    

def generate_remote_exp_dirs(expname, remote_output_basedir):    
    exp_output_dir = os.path.join(remote_output_basedir, expname)
        
    # input/output directories on the remote server to set inside the job files
    pred_dir_name = expname + "_" + common_exp_infos.PREDICTION_BASEDIR
    remote_input_dir = os.path.join(
                                     os.path.join(exp_output_dir, pred_dir_name),
                                     common_exp_infos.PREDICTION_DIRS["input"]
                                     )
    remote_output_dir = os.path.join(
                                     os.path.join(exp_output_dir, pred_dir_name),
                                     common_exp_infos.PREDICTION_DIRS["raw_data"]
                                     )
    remote_job_dir = os.path.join(
                                     os.path.join(exp_output_dir, pred_dir_name),
                                     common_exp_infos.PREDICTION_DIRS["jobs"]
                                     )    
    return (remote_input_dir, remote_output_dir, remote_job_dir)
 
  
    
    

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
    
    
    exec_dir_name = expname + "_" + common_exp_infos.PREDICTION_BASEDIR
    exp_dir = os.path.join(exp_base_dir, expname)
    assert os.path.isdir(exp_dir), "Cannot find experiment execution directory %s" % (exec_dir_name)
        
    exec_dir = os.path.join(exp_dir, exec_dir_name) 
    exec_input_files_dir = os.path.join(exec_dir, common_exp_infos.PREDICTION_DIRS["input"])
    exec_job_files_dir = os.path.join(exec_dir, common_exp_infos.PREDICTION_DIRS["jobs"])
        
    
    
    glconfig_data = file_helpers.read_json_config_file(options.glconf)
    expconfig_data = file_helpers.read_json_config_file(options.expconf)
    
     
    machine_configurator = file_helpers.instantiate_class_from_file(options.machcode)
    machine_configurator.setup_benchmark(benchmarks.BenchmarkGenerator())
    benchmark = machine_configurator.get_benchmark()
    
    
    assert os.path.isdir(exec_input_files_dir)
    print "Generating (local) input data in %s..." % exec_input_files_dir
    tests = format_input_data(glconfig_data)
    benchmark.generate_input_files(tests, exec_input_files_dir)
    print "Done."
    
    
    
    print "Generating job files in %s..." % exec_job_files_dir
    remote_output_basedir = machine_configurator.get_exp_output_dir()
    (remote_input_dir, remote_output_dir, remote_job_dir) = generate_remote_exp_dirs(expname, remote_output_basedir)
    
    machine_configurator.create_prediction_jobs(expconfig_data, remote_input_dir, remote_output_dir, exec_job_files_dir)
    print "Done." 
    
    print "--------------------"
    print "To run the generated jobs, copy the entire experiment from %s to the target machine (in %s) and execute the jobs from %s. " % (exp_dir, remote_output_basedir, remote_job_dir)
