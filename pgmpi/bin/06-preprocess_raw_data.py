#! /usr/bin/env python

import sys
import os
import subprocess
from optparse import OptionParser

# in bin
base_path = os.path.dirname( os.path.realpath( sys.argv[0] ) )
#cd ..
base_path = os.path.dirname( base_path )
lib_path = os.path.join( base_path, "lib" )
sys.path.append(lib_path)


from pgmpi.helpers import file_helpers
from pgmpi.glexp_desc.abs_exp_desc import AbstractExpDescription  
from pgmpi.helpers import common_exp_infos


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
#===============================================================================
# 
#     parser.add_option("-n", "--expname",
#                        action="store",
#                        dest="expname",
#                        type="string",
#                        help="unique experiment name")
#     parser.add_option("-d", "--expdir",
#                        action="store",
#                        dest="base_expdir",
#                        type="string",
#                        help="path to local experiment directory")
#     parser.add_option("-g", "--glconf",
#                        action="store",
#                        dest="glconf",
#                        type="string",
#                        help="path to guidelines config file")
#     parser.add_option("-m", "--machcode",
#                         action="store",
#                         dest="machcode",
#                         type="string",
#                         help="path to machine-specific class file")
#         
#     (options, args) = parser.parse_args()
#     
#     if options.expname == None:
#         print >> sys.stderr, "ERROR: Experiment name not specified"
#         parser.print_help()
#         sys.exit(1)
#     if options.glconf == None or not os.path.exists(options.glconf):
#         print >> sys.stderr, "ERROR: Guidelines configuration file invalid"
#         parser.print_help()
#         sys.exit(1)
#     if options.machcode == None or not os.path.exists(options.machcode):
#         print >> sys.stderr, "ERROR: Machine class file invalid"
#         parser.print_help()
#         sys.exit(1)
# 
#     if options.base_expdir == None:
#         base_expdir = os.path.abspath(base_path)
#         print  "Warning: Experiment directory not specified. Using current directory %s\n" %  base_path
#     else:
#         base_expdir = os.path.abspath(options.base_expdir)
#===============================================================================

    #instantiate experiment configuration class from user file
    exp_configurator_class = file_helpers.get_class_from_file(options.expfile, AbstractExpDescription)
    exp_configurator = exp_configurator_class() 
    
    experiment = exp_configurator.setup_exp()


    rscripts_dir = os.path.join(lib_path, common_exp_infos.SCRIPT_DIRS["rscripts"])
    data_dir = experiment.get_local_verif_alldata_dir()
    output_dir = experiment.get_local_verif_processed_dir()
        
    data_file = os.path.join(data_dir, common_exp_infos.FINAL_FILENAMES["alldata"])
        
    if not (os.path.exists(data_file)):
        print  "\nGenerated data file does not exist: %s\n" %  data_file
        print "Run ./pgmpi/bin/05-collect_raw_data.py script first."
        sys.exit(1)
   
    
    # get guidelines
    guidelines_file = os.path.join(output_dir, common_exp_infos.FINAL_FILENAMES["guidelines_list"])
    experiment.create_guidelines_catalog(guidelines_file)

    print("\nSummarizing data...\n")
    script = "%s/summarizeGuidelines.R" % (rscripts_dir)
    try:
        routput = subprocess.check_output(["Rscript", script, rscripts_dir, 
                                           os.path.abspath(data_file), 
                                           os.path.abspath(output_dir),
                                           common_exp_infos.SUMMARIZED_DATA_FILENAME_EXTENSION],
                                           stderr=subprocess.STDOUT
                                        )
        print routput
    except subprocess.CalledProcessError, e:
        print e.output
        exit(1)
        
    print ("Done.")
