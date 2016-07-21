'''
Created on Jun 24, 2016

@author: carpenamarie
'''
from pgmpi.glconfig.abs_glconfig import AbstractGLConfig
from pgmpi.helpers import file_helpers 

class Guidelines(AbstractGLConfig):


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


#===============================================================================
# 
# 
#    def format_guideline_data_for_input_files(self, nreps = 0):  
#         tests = {}
#         # format input data: { function_name1: { msize1 : { "nreps" : 10},
#         #                                             msize2 : { "nreps" : 20},
#         #                                          },
#         #                          function_name2 ......
#         #                           }
#         for guideline in self.__gl_conf_data:
#             bench_funcs = []
#             if "orig" in guideline:
#                 bench_funcs.append(guideline["orig"])
#             if "mock" in guideline:
#                 bench_funcs.append(guideline["mock"])
#             for bench_func in bench_funcs:
#                 for msize in guideline["msizes"]:   
#                     run = {}
#                     translated_name = self.__benchmark.translate_name(bench_func)
#                     if translated_name in tests.keys():
#                         run = tests[translated_name]
#                     
#                     if not msize in run.keys():
#                         run[msize] = {
#                                       "nreps": nreps
#                                       }       
#                     tests[translated_name] = run
#         return tests
# 
# 
#     def get_guidelines(self, benchmark):
#         all_guidelines = {}
#        
#         for guideline in self.__gl_conf_data:  
#             if "orig" in guideline.keys():
#                 if "mock" in guideline.keys():   # check whether it is a pattern guideline  
#                     translated_mockup_name = benchmark.translate_name(guideline["mock"])
#                 
#                 
#                     guideline_name = guideline["orig"] + "_lt_" + guideline["mock"] 
#                     all_guidelines[guideline_name] = [ guideline["orig"],
#                                                       guideline["mock"],
#                                                       translated_mockup_name
#                                                       ]
#                 else:                     # monotony/split-robustness guideline (need to add an empty second function)
#                     guideline_name = guideline["orig"] 
#                     all_guidelines[guideline_name] = [ guideline["orig"],
#                                                       "NA", 
#                                                       "NA"  
#                                                       ]
# 
#         return all_guidelines
#===============================================================================
