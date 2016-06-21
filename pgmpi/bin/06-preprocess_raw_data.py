#! /usr/bin/env python

import sys
import os
import subprocess
import imp
from inspect import isclass

# in bin
base_path = os.path.dirname( os.path.realpath( sys.argv[0] ) )
#cd ..
base_path = os.path.dirname( base_path )
lib_path = os.path.join( base_path, "lib" )
sys.path.append(lib_path)

from optparse import OptionParser
from mpiguidelines.helpers import file_helpers
from mpiguidelines.common_exp_infos import *
from mpiguidelines.machine_setup import * 
from mpiguidelines.benchmark import benchmarks

def get_guidelines(exp_data, benchmark):
    all_guidelines = {}
       
    for guideline in exp_data:  
        if "orig" in guideline.keys():
            if "mock" in guideline.keys():   # check whether it is a pattern guideline  
                translated_mockup_name = benchmark.translate_name(guideline["mock"])
                
                
                guideline_name = guideline["orig"] + "_lt_" + guideline["mock"] 
                all_guidelines[guideline_name] = [ guideline["orig"],
                                                   guideline["mock"],
                                                  translated_mockup_name
                                                  ]
            else:                     # monotony/split-robustness guideline (need to add an empty second function)
                guideline_name = guideline["orig"] 
                all_guidelines[guideline_name] = [ guideline["orig"],
                                                  "NA", 
                                                  "NA"
                                                  ]

    return all_guidelines


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
    parser.add_option("-m", "--machcode",
                        action="store",
                        dest="machcode",
                        type="string",
                        help="path to machine-specific class file")
        
    (options, args) = parser.parse_args()
    
    if options.expname == None:
        print >> sys.stderr, "ERROR: Experiment name not specified"
        parser.print_help()
        sys.exit(1)
    if options.glconf == None or not os.path.exists(options.glconf):
        print >> sys.stderr, "ERROR: Guidelines configuration file invalid"
        parser.print_help()
        sys.exit(1)
    if options.machcode == None or not os.path.exists(options.machcode):
        print >> sys.stderr, "ERROR: Machine class file invalid"
        parser.print_help()
        sys.exit(1)

    if options.base_expdir == None:
        base_expdir = os.path.abspath(base_path)
        print  "Warning: Experiment directory not specified. Using current directory %s\n" %  base_path
    else:
        base_expdir = os.path.abspath(options.base_expdir)


    # load machine setup class from specified file    
    mach_conf_module = imp.load_source("machconf", options.machcode)   
    mach_class_list = []
    for name, cls in mach_conf_module.__dict__.items():
        if isclass(cls) and issubclass(cls, PGMPIMachineConfigurator) and not issubclass(PGMPIMachineConfigurator, cls):
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


    rscripts_dir = os.path.join(lib_path, SCRIPT_DIRS["rscripts"])
    exp_dir = os.path.abspath(os.path.join(base_expdir, options.expname))
    
    if not (os.path.exists(exp_dir) and os.path.isdir(exp_dir)):
        print  "Experiment directory does not exist: %s\n" %  exp_dir
        sys.exit(1)
    
    
    #read guidelines configuration    
    gl_data = file_helpers.read_json_config_file(options.glconf)
    
    # find output dir
    output_dir = os.path.join(exp_dir, EXEC_RESULTS_DIRS["summary"])
    file_helpers.create_local_dir(output_dir)
    
    # find the data file
    data_dir = os.path.join(exp_dir, EXEC_RESULTS_DIRS["alldata"])
    data_file = os.path.join(data_dir, "data.txt")
    
    if not (os.path.exists(data_file)):
        print  "\nGenerated data file does not exist: %s\n" %  data_file
        print "Run ./collectAllData.py script first."
        sys.exit(1)
   

    # instantiate benchmark   
    bench_path  = machine_configurator.get_bench_path()
    bench_type  = machine_configurator.get_bench_type()
    benchmark = benchmarks.BENCHMARKS[bench_type](bench_path)

    
    # get guidelines
    all_guidelines = get_guidelines(gl_data, benchmark)
    guidelines_file = os.path.join(output_dir, "guidelines_catalog.txt")

    print("Guideline list for %s:" % options.expname)
    print("\n".join(all_guidelines))
    header = "guideline orig mock translated_mock"
    file_helpers.write_guidelines_to_dataframe(guidelines_file, all_guidelines, header)
    
    print("\nSummarizing data...\n")
    script = "%s/summarizeGuidelines.R" % (rscripts_dir)
    try:
        routput = subprocess.check_output(["Rscript", script, rscripts_dir, 
                                           #guidelines_file, 
                                           data_file, output_dir],
                                           stderr=subprocess.STDOUT
                                        )
        print routput
    except subprocess.CalledProcessError, e:
        print e.output
        exit(1)
        
    print ("Done.")
