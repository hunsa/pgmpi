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


    exp_configurator = file_helpers.instantiate_class_from_file(options.expfile, abs_exp_desc.AbstractExpDescription)

    experiment = exp_configurator.setup_exp()
    experiment.generate_input_files()
    
    exec_dir_name = expname + "_" + common_exp_infos.PREDICTION_BASEDIR
    exp_dir = os.path.join(exp_base_dir, expname)
    assert os.path.isdir(exp_dir), "Cannot find experiment execution directory %s" % (exec_dir_name)
        
    exec_dir = os.path.join(exp_dir, exec_dir_name) 
    exec_input_files_dir = os.path.join(exec_dir, common_exp_infos.EXEC_DIRS["input"])
    exec_job_files_dir = os.path.join(exec_dir, common_exp_infos.EXEC_DIRS["jobs"])
        
    
    
    glconfig_data = file_helpers.read_json_config_file(options.glconf)
    expconfig_data = file_helpers.read_json_config_file(options.expconf)
    
     
    machine_configurator = file_helpers.instantiate_class_from_file(options.machcode)
    machine_configurator.setup_benchmark(benchmarks.BenchmarkGenerator())
    benchmark = machine_configurator.get_benchmark()
    
    

    
       
    print "--------------------"
    print "To run the generated jobs, copy the entire experiment from %s to the target machine (in %s) and execute the jobs from %s. " % (exp_dir, remote_output_basedir, remote_job_dir)
