'''
Created on Jun 24, 2016

@author: carpenamarie
'''
import sys
import os
import shutil
from pgmpi.helpers import file_helpers
from pgmpi.helpers import common_exp_infos

class GLExperimentWriter(object):
    '''
    classdocs
    '''
    __input_file_name = "input.txt"
    __input_job_name = "job.sh"

    def __init__(self, gl_config, exp_config, benchmark, machine_configurator, local_basedir):

        self.__gl_config = gl_config
        self.__exp_config = exp_config
        self.__benchmark = benchmark
        self.__machine_configurator = machine_configurator
        self.__local_basedir = local_basedir
    
        self.__pred_input_files_dir = os.path.join(self.__local_basedir, common_exp_infos.PREDICTION_DIRS["input"])
        self.__pred_job_files_dir = os.path.join(self.__local_basedir, common_exp_infos.PREDICTION_DIRS["jobs"])
    
        self.__verif_input_files_dir = os.path.join(self.__local_basedir, common_exp_infos.EXEC_DIRS["input"])
        self.__verif_job_files_dir = os.path.join(self.__local_basedir, common_exp_infos.EXEC_DIRS["jobs"])
    
    
    
    def generate_pred_input_files(self):
        
        assert os.path.isdir(self.__pred_input_files_dir)
        inputfile = os.path.join(self.__pred_input_files_dir, self.__input_file_name)
        print "Generating (local) input data in %s..." % inputfile
        
        
        tests = self.__format_guideline_data(self.__gl_config)
        
        file_contents = self.__benchmark.generate_input_file_data(tests)
                
        with open(inputfile, "w") as f:
                f.write( "%s\n" % (file_contents))
        print "Done."
        
    
    def create_prediction_jobs(self):
        assert os.path.isdir(self.__pred_job_files_dir)
        print "Generating job files in %s..." % self.__pred_job_files_dir        
         
        bench_binary_path = self.__benchmark.get_prediction_bench_binary()
        bench_args = self.__benchmark.get_prediction_bench_args(self.__exp_config) 
        
        job_contents = self.__machine_configurator.generate_job_contents(self.__exp_config, bench_binary_path, bench_args)
        jobfile = os.path.join(self.__pred_job_files_dir, self.__input_job_name)
        with open(jobfile, "w") as f:
                f.write( "%s\n" % (job_contents))
        print "Done." 

    
    
    
    def create_exp_dir_structure(self):
    
        exp_dir = self.__local_basedir
        ret = file_helpers.create_local_dir(exp_dir)
        if not ret:
            print ("Specify another experiment name or path to create a new experiment.\n")
            sys.exit(1) 
    
        # create prediction directory tree
        pred_dir = os.path.join(exp_dir, common_exp_infos.PREDICTION_BASEDIR)
        file_helpers.create_local_dir(pred_dir)
        for d in common_exp_infos.PREDICTION_DIRS.values():
            file_helpers.create_local_dir(os.path.join(pred_dir, d))
        for d in common_exp_infos.PREDICTION_RESULTS_DIRS.values():
            file_helpers.create_local_dir(os.path.join(pred_dir, d))
    
        # create experiment execution directory tree
        exec_dir = os.path.join(exp_dir, common_exp_infos.EXEC_BASEDIR)
        file_helpers.create_local_dir(exec_dir)
        for d in common_exp_infos.EXEC_DIRS.values():
            file_helpers.create_local_dir(os.path.join(exec_dir, d))

        # create experiment results directory tree
        for d in common_exp_infos.EXEC_RESULTS_DIRS.values():
            file_helpers.create_local_dir(os.path.join(exp_dir, d))

        #create initial configuration directory
        conf_dir = os.path.join(exp_dir, common_exp_infos.CONFIG_BASEDIR)
        file_helpers.create_local_dir(conf_dir)
    
 
    def create_init_config_files(self):
        config_dir = os.path.join(self.__local_basedir, common_exp_infos.CONFIG_BASEDIR) 
        assert os.path.isdir(config_dir)
    
        gl_file = self.__gl_config.get_filename()
        shutil.copy(gl_file, config_dir)

        exp_conf_file = self.__exp_config.get_filename()
        shutil.copy(exp_conf_file, config_dir)



    
    
    def __format_guideline_data(self, glconfig_data):  
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
    