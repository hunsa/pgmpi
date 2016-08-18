#! /usr/bin/env python

import sys
import os
import shutil
import argparse 
import subprocess

# in bin
base_path = os.path.dirname( os.path.realpath( sys.argv[0] ) )
#cd ..
base_path = os.path.dirname( base_path )
lib_path = os.path.join( base_path, "lib" )
sys.path.append(lib_path)


from pgmpi.helpers import file_helpers
from pgmpi.helpers import common_exp_infos
from pgmpi.glexp_desc.abs_exp_desc import AbstractExpDescription  
    
OUTPUT_SEPARATOR = "-" * 30 
    
    
def initialize_experiment_handle():
    # need to check if experiment file exists
    # TODO: do not assume default name
    exp_config_dir = os.path.join(os.getcwd(), common_exp_infos.CONFIG_BASEDIR)
    exp_file = os.path.join(exp_config_dir, common_exp_infos.EXP_CONF_FILE)
    
    #include experiment file directory in the path
    sys.path.append(os.path.dirname(exp_file))

    #instantiate experiment configuration class from user file
    exp_configurator_class = file_helpers.get_class_from_file(exp_file, AbstractExpDescription)
    exp_configurator = exp_configurator_class() 
        
    experiment = exp_configurator.setup_exp()
    return experiment

    
def get_nrep_predictions(pred_rawdata_dir):
    assert os.path.isdir(pred_rawdata_dir), "Cannot find prediction results directory %s. Please execute the prediction jobs first with ./bin/runPredictionJobs.py " % (pred_rawdata_dir)

    fieldnames=["test", "nrep", "msize", "last_runtime_sec", "pred_method", "pred_value"]
    nrep_prediction_data = {}
    
    for f in os.listdir(pred_rawdata_dir):
        if f.endswith(".dat"):      
            data = file_helpers.read_cvs_file(os.path.join(pred_rawdata_dir, f), fieldnames)
            current_test = None
            
            for data_row in data:
                print(data_row)
                if current_test == (data_row["test"], data_row["msize"]):
                    continue    # skip this line, already read data for this (test,msize) tuple
                else:
                    current_test = (data_row["test"], data_row["msize"])
                    
                    if len(nrep_prediction_data) > 0 and current_test in nrep_prediction_data.keys():
                        # already have the results for this (test,msize) tuple from a different file
                        # add current nrep value
                        test_data = nrep_prediction_data[current_test]
                        test_data.append(int(data_row["nrep"]))
                    else:
                        # create nrep record for the current test
                        nrep_prediction_data[current_test] = [int(data_row["nrep"])] 
                        
    # reformat data into a json-compatible structure
    # replace list of nreps with the maximum value for each (test, msize) tuple
    nrep_prediction_list = []
    for test in nrep_prediction_data.keys():
        maxnreps = max(nrep_prediction_data[test])
        print("[%s][msize=%s] Setting max_nrep=%d " % (test[0], test[1], maxnreps))
        
        nrep_prediction_list.append({
                                     "test" : test[0],
                                     "msize": test[1],
                                     "max_nrep": maxnreps
                                    })
        
    return nrep_prediction_list

    
def exec_init(args):
    print "Initializing experiment in %s..." % (args.dir)    

    if args.dir == None or not os.path.isdir(args.dir):
        print >> sys.stderr, "ERROR: Invalid directory specified. Please create directory before running the script."
        parser.print_help()
        sys.exit(1)        

    #create initial configuration directory
    conf_dir = os.path.join(args.dir, common_exp_infos.CONFIG_BASEDIR)
    file_helpers.create_local_dir(conf_dir)
    
    
    default_conf_dir = os.path.join(lib_path, common_exp_infos.DEFAULT_CONFIG_DIR)
    exp_cf_file = os.path.join(default_conf_dir, common_exp_infos.EXP_CONF_FILE)
    assert os.path.exists(exp_cf_file)
    shutil.copy(exp_cf_file, conf_dir)
    
    exp_gl_file = os.path.join(default_conf_dir, common_exp_infos.GUIDELINE_CATALOG_FILE)
    assert os.path.exists(exp_gl_file)    
    shutil.copy(exp_gl_file, conf_dir)
 
    exp_file = os.path.join(default_conf_dir, common_exp_infos.GUIDELINE_CONFIG_FILE)
    assert os.path.exists(exp_file)    
    shutil.copy(exp_file, conf_dir)    
        
    experiment = initialize_experiment_handle()
    experiment.create_exp_dir_structure()
    
    print "Done."


    
def exec_setup(args):
    print "Setting up experiment... "  
    
    experiment = initialize_experiment_handle()

    if args.step == "pred":
        
        experiment.generate_pred_input_files()
        experiment.create_prediction_jobs()
        
        print OUTPUT_SEPARATOR
        print OUTPUT_SEPARATOR
        #    if not experiment.get_exp_dir() == experiment.get_remote_exp_dir():
        print "To proceed with the experiment: "
        print "1. Copy: \n\t%s \nto the target machine in:\n\t$REMOTE_DIR\n" % (experiment.get_local_pred_job_dir()) 
        print OUTPUT_SEPARATOR
        print "2. On the target machine: \n\tcd $REMOTE_DIR/%s" % (os.path.basename(experiment.get_remote_pred_job_dir()))
        print OUTPUT_SEPARATOR
        print "3. Execute the job in: \n\tjob.sh\n"
        print OUTPUT_SEPARATOR
        print "4. Copy results from the target machine directory: \n\t$REMOTE_DIR/%s \nto the local machine in: \n\t%s" % (experiment.get_remote_pred_output_dir(), experiment.get_local_pred_job_dir())
        print OUTPUT_SEPARATOR
    
    elif args.step == "verif":
        processed_dir = experiment.get_local_pred_processed_dir()
        pred_file = os.path.join(processed_dir, common_exp_infos.PREDICTION_PROCESSED_OUTPUT_FILENAME)
    
        prediction_data = file_helpers.read_json_config_file(pred_file) 
        assert len(prediction_data) > 0, "No prediction data found or incorrectly formatted. Generate prediction data first"  
    
    
        experiment.generate_verification_input_files(prediction_data)
        experiment.create_verification_jobs()

        print OUTPUT_SEPARATOR
        print OUTPUT_SEPARATOR
        #    if not experiment.get_exp_dir() == experiment.get_remote_exp_dir():
        print "To proceed with the experiment: "
        print "1. Copy: \n\t%s \nto the target machine in:\n\t$REMOTE_DIR\n" % (experiment.get_local_verif_job_dir()) 
        print OUTPUT_SEPARATOR
        print "2. On the target machine: \n\tcd $REMOTE_DIR/%s" % (os.path.basename(experiment.get_remote_verif_job_dir()))
        print OUTPUT_SEPARATOR
        print "3. Execute the job in: \n\tjob.sh\n"
        print OUTPUT_SEPARATOR
        print "4. Copy results from the target machine directory: \n\t$REMOTE_DIR/%s \nto the local machine in: \n\t%s" % (experiment.get_remote_verif_output_dir(), experiment.get_local_verif_job_dir())
        print OUTPUT_SEPARATOR

        
    else:
        print >> sys.stderr, "ERROR: Unknown option."
        exit(1)
    
        
    

def exec_process(args):
    print "Processing experiment... "    
    experiment = initialize_experiment_handle()

    if args.step == "pred":
        pred_rawdata_dir = experiment.get_local_pred_output_dir()
        processed_dir = experiment.get_local_pred_processed_dir()

        print "Processing prediction data from %s..." % pred_rawdata_dir
        prediction_data = get_nrep_predictions(pred_rawdata_dir)
    
        assert len(prediction_data) > 0, "No prediction data found or incorrectly formatted. Generate prediction data first"  
        output_file = os.path.join(processed_dir, common_exp_infos.PREDICTION_PROCESSED_OUTPUT_FILENAME)
        file_helpers.write_json_config_file(output_file, prediction_data)

        print("Prediction data summarized into the %s file" % output_file)

    
    elif args.step == "verif":
        rscripts_dir = os.path.join(lib_path, common_exp_infos.SCRIPT_DIRS["rscripts"])
        
        rawdata_dir = experiment.get_local_verif_output_dir()
        output_dir = experiment.get_local_verif_alldata_dir()
    
        if (not os.path.exists(rawdata_dir)) or len(os.listdir(rawdata_dir)) == 0:
            print  "\nRaw benchmark output files do not exist in %s" %  rawdata_dir
            print "To generate them, execute the benchmark jobs in %s" % experiment.get_remote_verif_job_dir()
            sys.exit(1)
    
        # collect all data
        file_helpers.create_local_dir(output_dir)
        alldata_file = os.path.join(output_dir, common_exp_infos.FINAL_FILENAMES["alldata"])
        rawdata_pattern = common_exp_infos.BENCH_OUTPUT_FILENAME_PATTERN
        print(rawdata_dir)
        print (rscripts_dir)
    
        print("\nReading raw data...")
        script = "%s/collectAll.R" % (rscripts_dir)
        try:
            routput = subprocess.check_output(["Rscript", script, rscripts_dir, 
                                           os.path.abspath(rawdata_dir), 
                                           os.path.abspath(alldata_file),
                                           rawdata_pattern],
                                stderr=subprocess.STDOUT
                                )
            print routput
        except subprocess.CalledProcessError, e:
            print e.output
            exit(1)


        # summarize data
        output_dir = experiment.get_local_verif_processed_dir()
            
        if not (os.path.exists(alldata_file)):
            print  "\nGenerated data file could not be created in %s\n" %  alldata_file
            sys.exit(1)
   
        # get guidelines
        guidelines_file = os.path.join(output_dir, common_exp_infos.FINAL_FILENAMES["guidelines_list"])
        experiment.create_guidelines_catalog(guidelines_file)

        print("\nSummarizing data...\n")
        script = "%s/summarizeGuidelines.R" % (rscripts_dir)
        try:
            routput = subprocess.check_output(["Rscript", script, rscripts_dir, 
                                           os.path.abspath(alldata_file), 
                                           os.path.abspath(output_dir),
                                           common_exp_infos.SUMMARIZED_DATA_FILENAME_EXTENSION],
                                           stderr=subprocess.STDOUT
                                        )
            print routput
        except subprocess.CalledProcessError, e:
            print e.output
            exit(1)




        
    else:
        print >> sys.stderr, "ERROR: Unknown option."
        exit(1)
    
    #print OUTPUT_SEPARATOR
    #print OUTPUT_SEPARATOR
    #if not os.path.abspath(experiment.get_exp_dir()) == experiment.get_remote_exp_dir():
    #    print "To execute the experiment: \nCopy: \n\t%s \nTo the target machine in: \n\t%s\n" % (experiment.get_exp_dir(),  os.path.dirname(experiment.get_remote_exp_dir())) 
    #    print OUTPUT_SEPARATOR
    #print "Execute the jobs from: \n\t%s\n" % (current_job_dir)
    #print OUTPUT_SEPARATOR


def exec_check(args):
    experiment = initialize_experiment_handle()

    rscripts_dir = os.path.join(lib_path, common_exp_infos.SCRIPT_DIRS["rscripts"])
    summary_dir = experiment.get_local_verif_processed_dir()
    guidelines_list_file = os.path.join(summary_dir, common_exp_infos.FINAL_FILENAMES["guidelines_list"])
        
    if not (os.path.exists(summary_dir)):
        print  "\nSummarized results do not exist: %s\n" %  summary_dir
        print "Run the ./pgmpi/bin/06-preprocess_raw_data.py script first."
        sys.exit(1)

    if not (os.path.exists(guidelines_list_file)):
        print  "\nGuidelines catalog file does not exist: %s\n" %  guidelines_list_file
        print "Run the ./pgmpi/bin/06-preprocess_raw_data.py script first."
        sys.exit(1)

    

    print("\n------------------------------------------------------------")
    print("\nThe following performance guideline violations have been found:\n" )
    
    script = "%s/showViolations.R" % (rscripts_dir)
    try:
        routput = subprocess.check_output(["Rscript", script, rscripts_dir, 
                                           os.path.abspath(summary_dir),
                                           os.path.abspath(guidelines_list_file),
                                           common_exp_infos.SUMMARIZED_DATA_FILENAME_PATTERN
                                           ],
                                           stderr=subprocess.STDOUT
                                        )
        print routput
    except subprocess.CalledProcessError, e:
        print e.output
        exit(1)
        
    print ("Done.")



if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title='valid sub-commands',
                                       dest='subparser_name')
                                       #description='execute one of the following commands')
                                       #help='additional help')
    init_parser = subparsers.add_parser('init', help='initialize experiment in the specified directory')
    init_parser.add_argument('dir', type=str, 
                             action='store',
                             metavar = "exp_dir",
                             help='experiment directory')
    init_parser.set_defaults(process_func=exec_init)
    
    setup_parser = subparsers.add_parser('setup', help='setup experiment (create input files/jobs)')
    setup_parser.add_argument('step', type=str, 
                              choices=['pred', 'verif'],
                              action='store',
                              help='select experimental step')
    setup_parser.set_defaults(process_func=exec_setup)
    
    process_parser = subparsers.add_parser('process', help='process experimental results')
    process_parser.add_argument('step', type=str, 
                              choices=['pred', 'verif'],
                              action='store',
                              help='select experimental step')    
    process_parser.set_defaults(process_func=exec_process)
    
    
    check_parser = subparsers.add_parser('check', help='verify guideline violations') 
    check_parser.set_defaults(process_func=exec_check)
    
    args = parser.parse_args()
    args.process_func(args)




