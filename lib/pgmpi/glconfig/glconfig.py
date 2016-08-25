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


from pgmpi.glconfig import abs_glconfig
from pgmpi.helpers import file_helpers 

class Guidelines(abs_glconfig.AbstractGLConfig):


    def __init__(self, gl_config_file):
        self.__gl_conf_data = file_helpers.read_json_config_file(gl_config_file)
        self.__gl_conf_filepath = gl_config_file
                
        
    
    def get_gl_filepath(self):
        return self.__gl_conf_filepath 
    
    
    # Format guideline data into the following structure (for each function/msize pair):
    #                         { function_name1: { msize1 : { "nreps" : value},
    #                                             msize2 : { "nreps" : value},
    #                                          },
    #                          function_name2 ......
    #                           }
    def format_guideline_data_for_input_files(self, nreps = 0):  
        tests = {}
        for guideline in self.__gl_conf_data:
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
                                      "nreps": nreps
                                      }       
                    tests[bench_func] = run
        return tests



    # Extract guidelines (and comprised function names) into a catalog
    # format of the returned data: 
    #    { function_orig_lt_function_mock: [ function_orig,
    #                                        function_mock
    #                                       ],
    #      function_orig                : [ function_orig
    #                                       ],
    def format_guideline_data_for_catalog(self):
        all_guidelines = {}
       
        for guideline in self.__gl_conf_data:  
            if "orig" in guideline.keys():
                if "mock" in guideline.keys():   # check whether it is a pattern guideline  
                    guideline_name = guideline["orig"] + "_lt_" + guideline["mock"] 
                    all_guidelines[guideline_name] = [ guideline["orig"],
                                                      guideline["mock"]
                                                      ]
                else:                     # monotony/split-robustness guideline (need to add an empty second function)
                    guideline_name = guideline["orig"] 
                    all_guidelines[guideline_name] = [ guideline["orig"]
                                                      ]
        return all_guidelines



