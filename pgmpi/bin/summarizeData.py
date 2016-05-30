#! /usr/bin/env python

import sys
import os
import subprocess

# in bin
base_path = os.path.dirname( os.path.realpath( sys.argv[0] ) )
#cd ..
base_path = os.path.dirname( base_path )
lib_path = os.path.join( base_path, "lib" )
sys.path.append(lib_path)

from optparse import OptionParser
from mpiguidelines.helpers import file_helpers as helpers
from mpiguidelines.common_exp_infos import *

def get_guidelines(exp_data):
    all_guidelines = {}
       
    guidelines = exp_data["guidelines"]
    for guideline in guidelines:  
        if "orig" in guideline:
            if "mock" in guideline:   # check whether it is a pattern guideline  
                guideline_name = guideline["orig"] + "<" + guideline["mock"] 
                all_guidelines[guideline_name] = guideline["bench_mpicalls"]
            else:                     # monotony/split-robustness guideline (need to add an empty second function)
                guideline_name = guideline["orig"] 
                all_guidelines[guideline_name] = guideline["bench_mpicalls"]
                all_guidelines[guideline_name].append("NA")

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
    
    (options, args) = parser.parse_args()
    
    if options.expname == None:
        print >> sys.stderr, "Experiment name not specified"
        parser.print_help()
        sys.exit(1)

    if options.base_expdir == None:
        base_expdir = os.path.abspath(base_path)
        print  "Warning: Experiment directory not specified. Using current directory %s\n" %  base_path
    else:
        base_expdir = os.path.abspath(options.base_expdir)


    rscripts_dir = os.path.join(lib_path, SCRIPT_DIRS["rscripts"])
    exp_dir = os.path.abspath(os.path.join(base_expdir, options.expname))
    
    if not (os.path.exists(exp_dir) and os.path.isdir(exp_dir)):
        print  "Experiment directory does not exist: %s\n" %  exp_dir
        sys.exit(1)
    
    
    #read experiment configuration    
    conf_dir = os.path.join(exp_dir, CONFIG_BASEDIR)
    generated_exp_config = os.path.join(conf_dir, options.expname+".json")
    exp_data = helpers.read_json_config_file(generated_exp_config)
    
    # find output dir
    output_dir = os.path.join(exp_dir, EXEC_RESULTS_DIRS["summary"])
    helpers.create_local_dir(output_dir)
    
    # find the data file
    data_dir = os.path.join(exp_dir, EXEC_RESULTS_DIRS["alldata"])
    data_file = os.path.join(data_dir, "data.txt")
    
    if not (os.path.exists(data_file)):
        print  "\nGenerated data file does not exist: %s\n" %  data_file
        print "Run ./collectAllData.py script first."
        sys.exit(1)
    
    # get guidelines
    all_guidelines = get_guidelines(exp_data)
    guidelines_file = os.path.join(output_dir, "guidelines_catalog.txt")

    print("Guideline list for %s:" % options.expname)
    print("\n".join(all_guidelines))
    helpers.write_to_dataframe(guidelines_file, all_guidelines)
    
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
