#    PGMPI - Performance Guideline Verification Tool for MPI Collectives
#
#    Copyright 2016 Alexandra Carpen-Amarie, Sascha Hunold
#    Research Group for Parallel Computing
#    Faculty of Informatics
#    Vienna University of Technology, Austria
# 
# 
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 2 of the License, or
#    (at your option) any later version.
# 
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
# 
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


import sys
import os
import shutil
from pgmpi.helpers import file_helpers
from pgmpi.helpers import common_exp_infos
from pgmpi.expconfig import glexpconfig
from pgmpi.glconfig import glconfig

class DirStructure(object):

    def __init__(self, basedir, input_rel_dir, job_rel_dir, raw_data_rel_dir, 
                 proc_data_rel_dir = None, alldata_rel_dir = None):
        self.basedir = basedir
        self.input_dir = os.path.join(basedir, input_rel_dir)
        self.job_dir = os.path.join(basedir, job_rel_dir)
        self.raw_data_dir = os.path.join(basedir, raw_data_rel_dir)
        
        if proc_data_rel_dir:
            self.processed_data_dir = os.path.join(basedir, proc_data_rel_dir)
        
        if alldata_rel_dir:
            self.alldata_dir = os.path.join(basedir, alldata_rel_dir)
        

class GLExperimentWriter(object):
    '''
    classdocs
    '''
    DEFAULT_NREPS = 0
    
    __input_file_name = "input.txt"
    __input_job_name = "job.sh"

    def __init__(self, benchmark, machine_configurator):

        # initialize guideline config and guideline_catalog from the predefined directory
        exp_config_dir = os.path.join(os.getcwd(), common_exp_infos.CONFIG_BASEDIR)
        gl_config_file = os.path.join(exp_config_dir, common_exp_infos.GUIDELINE_CONFIG_FILE)
        gl_catalog_file = os.path.join(exp_config_dir, common_exp_infos.GUIDELINE_CATALOG_FILE)

        self.__gl_config = glconfig.Guidelines(gl_catalog_file) 
        self.__exp_config = glexpconfig.GLExperimentalConfig(gl_config_file)
        
        self.__benchmark = benchmark
        self.__machine_configurator = machine_configurator
        
        self.__local_basedir = ""
    
        # use absolute path for if the remote directory is the same as the local one
        self.__remote_basedir = ""
        #if self.__remote_basedir == self.__local_basedir:
        #    self.__remote_basedir = os.path.abspath(self.__remote_basedir)
        
    
        local_pred_dir = os.path.join(self.__local_basedir, common_exp_infos.PREDICTION_BASEDIR)
        self.__local_pred = DirStructure(basedir = local_pred_dir, 
                                         input_rel_dir = common_exp_infos.PREDICTION_DIRS["input"],
                                         job_rel_dir = common_exp_infos.PREDICTION_DIRS["jobs"],
                                         raw_data_rel_dir = common_exp_infos.PREDICTION_DIRS["raw_data"],
                                         proc_data_rel_dir = common_exp_infos.PREDICTION_RESULTS_DIRS["summary"])
    
    
        local_verif_dir = os.path.join(self.__local_basedir, common_exp_infos.EXEC_BASEDIR)
        self.__local_verif = DirStructure(basedir = local_verif_dir, 
                                         input_rel_dir = common_exp_infos.EXEC_DIRS["input"],
                                         job_rel_dir = common_exp_infos.EXEC_DIRS["jobs"],
                                         raw_data_rel_dir = common_exp_infos.EXEC_DIRS["raw_data"],
                                         proc_data_rel_dir = common_exp_infos.EXEC_RESULTS_DIRS["summary"],
                                         alldata_rel_dir = common_exp_infos.EXEC_RESULTS_DIRS["alldata"])
        
        
        #remote_pred_dir = os.path.join(self.__remote_basedir, common_exp_infos.PREDICTION_BASEDIR)
        remote_pred_dir = ""
        self.__remote_pred = DirStructure(basedir = remote_pred_dir, 
                                         input_rel_dir = common_exp_infos.PREDICTION_DIRS["input"],
                                         job_rel_dir = common_exp_infos.PREDICTION_DIRS["jobs"],
                                         raw_data_rel_dir = common_exp_infos.PREDICTION_DIRS["raw_data"]
                                         )

        
        #remote_verif_dir = os.path.join(self.__remote_basedir, common_exp_infos.EXEC_BASEDIR)
        remote_verif_dir = ""
        self.__remote_verif = DirStructure(basedir = remote_verif_dir, 
                                         input_rel_dir = common_exp_infos.EXEC_DIRS["input"],
                                         job_rel_dir = common_exp_infos.EXEC_DIRS["jobs"],
                                         raw_data_rel_dir = common_exp_infos.EXEC_DIRS["raw_data"]
                                         )
        
        
    
#    def get_exp_dir(self):
#        return self.__local_basedir
    
    
#    def get_remote_exp_dir(self):
#        return self.__remote_basedir

    def get_local_pred_input_dir(self):
        return self.__local_pred.input_dir

    def get_local_verif_input_dir(self):
        return self.__local_verif.input_dir

    def get_local_pred_job_dir(self):
        return self.__local_pred.job_dir

    def get_local_verif_job_dir(self):
        return self.__local_verif.job_dir
    
    
    def get_remote_pred_job_dir(self):
        return self.__remote_pred.job_dir

    def get_remote_verif_job_dir(self):
        return self.__remote_verif.job_dir


    def get_local_pred_output_dir(self):
        return self.__local_pred.raw_data_dir
    
    def get_local_verif_output_dir(self):
        return self.__local_verif.raw_data_dir

    def get_remote_pred_output_dir(self):
        return self.__remote_pred.raw_data_dir
    
    def get_remote_verif_output_dir(self):
        return self.__remote_verif.raw_data_dir
    
    def get_local_pred_processed_dir(self):
        return self.__local_pred.processed_data_dir
    
    def get_local_verif_processed_dir(self):
        return self.__local_verif.processed_data_dir
    
    
    def get_local_verif_alldata_dir(self):
        return self.__local_verif.alldata_dir
    
    def generate_pred_input_files(self):
        
        assert os.path.isdir(self.__local_pred.input_dir)
        inputfile = os.path.join(self.__local_pred.input_dir, self.__input_file_name)
        print "Generating (local) input data in %s..." % inputfile
        
        # set nreps to 0 for prediction jobs
        tests = self.__gl_config.format_guideline_data_for_input_files(nreps = 0)        
        file_contents = self.__benchmark.generate_input_file_data(tests)
                
        with open(inputfile, "w") as f:
                f.write( "%s\n" % (file_contents))
        print "Done."
        
   
    def generate_verification_input_files(self, pred_data):
        
        assert os.path.isdir(self.__local_verif.input_dir)
        inputfile = os.path.join(self.__local_verif.input_dir, self.__input_file_name)
        print "Generating (local) input data in %s..." % inputfile
        
        # initially set nreps to the maximum possible value
        tests = self.__gl_config.format_guideline_data_for_input_files(nreps = self.DEFAULT_NREPS)
        
        # set nreps according to the predicted values (if they were measured)
        if pred_data:
            for res in pred_data:
                # prediction data contains benchmark-specific function names
                # thus, the input function names need to be translated
                bench_func_names = [self.__benchmark.translate_name(t) for t in tests.keys()]
                
                if res["test"] in bench_func_names:
                    msize = int(res["msize"])
                    
                    index =  bench_func_names.index(res["test"])
                    current_test = tests.keys()[index] 
                    if msize in tests[current_test].keys():
                        nreps = tests[current_test][msize]["nreps"]
                        
                        if nreps == self.DEFAULT_NREPS or res["max_nrep"] > nreps:
                            tests[current_test][msize]["nreps"] = res["max_nrep"]   
        
        file_contents = self.__benchmark.generate_input_file_data(tests)
                
        with open(inputfile, "w") as f:
                f.write( "%s\n" % (file_contents))
        print "Done."
   
        
    
    def create_prediction_jobs(self):
        assert os.path.isdir(self.__local_pred.job_dir)
        print "Generating job files in %s..." % self.__local_pred.job_dir       
         
        #input_file_path = os.path.join(self.__remote_pred.input_dir, self.__input_file_name)
        input_file_dir = os.path.relpath(self.__remote_pred.input_dir, self.__remote_pred.job_dir)
        input_file_path = os.path.join(input_file_dir, self.__input_file_name)
        
        bench_binary_path = self.__benchmark.get_prediction_bench_binary()
        bench_args = self.__benchmark.get_prediction_bench_args(input_file_path, self.__exp_config) 
        
        output_dir = os.path.relpath(self.__remote_pred.raw_data_dir, self.__remote_pred.job_dir)
        job_contents = self.__machine_configurator.generate_prediction_job_contents(self.__exp_config, bench_binary_path, bench_args, output_dir)
        jobfile = os.path.join(self.__local_pred.job_dir, self.__input_job_name)
        with open(jobfile, "w") as f:
                f.write( "%s\n" % (job_contents))
        print "Done." 

  
    def create_verification_jobs(self):
        assert os.path.isdir(self.__local_verif.job_dir)
        print "Generating job files in %s..." % self.__local_verif.job_dir     
         
        #input_file_path = os.path.join(self.__remote_verif.input_dir, self.__input_file_name)
        input_file_dir = os.path.relpath(self.__remote_verif.input_dir, self.__remote_verif.job_dir)
        input_file_path = os.path.join(input_file_dir, self.__input_file_name)
        
        
        bench_binary_path = self.__benchmark.get_verification_bench_binary()
        bench_args = self.__benchmark.get_verification_bench_args(input_file_path, self.__exp_config) 
        
        output_dir = os.path.relpath(self.__remote_verif.raw_data_dir, self.__remote_verif.job_dir)
        job_contents = self.__machine_configurator.generate_verification_job_contents(self.__exp_config, bench_binary_path, bench_args, output_dir)
        jobfile = os.path.join(self.__local_verif.job_dir, self.__input_job_name)
        with open(jobfile, "w") as f:
                f.write( "%s\n" % (job_contents))
        print "Done."   
  
    
    
    def create_exp_dir_structure(self):
    
        # create prediction directory tree
        file_helpers.create_local_dir(self.__local_pred.basedir)
        for d in common_exp_infos.PREDICTION_DIRS.values():
            file_helpers.create_local_dir(os.path.join(self.__local_pred.basedir, d))
        for d in common_exp_infos.PREDICTION_RESULTS_DIRS.values():
            file_helpers.create_local_dir(os.path.join(self.__local_pred.basedir, d))
    
        # create experiment execution directory tree
        file_helpers.create_local_dir(self.__local_verif.basedir)
        for d in common_exp_infos.EXEC_DIRS.values():
            file_helpers.create_local_dir(os.path.join(self.__local_verif.basedir, d))

        # create experiment results directory tree
        for d in common_exp_infos.EXEC_RESULTS_DIRS.values():
            file_helpers.create_local_dir(os.path.join(self.__local_verif.basedir, d))




    def create_guidelines_catalog(self, guidelines_file):
        
        all_guidelines = self.__gl_config.format_guideline_data_for_catalog()
        
        print("Guideline list:")
        print("\n".join(all_guidelines))
        
        for guideline in all_guidelines.keys():
            info = all_guidelines[guideline]
            if len(info) == 2:  # pattern guideline
                info.append(self.__benchmark.translate_name(info[1]))
            if len(info) == 1:  # monotony/split-robustness guideline
                info.append("NA")
                info.append("NA")
        
        header = "guideline orig mock translated_mock"
        file_helpers.write_guidelines_to_dataframe(guidelines_file, all_guidelines, header)

    
    
    
            

