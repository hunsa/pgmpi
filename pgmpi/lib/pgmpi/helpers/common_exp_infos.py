



PREDICTION_BASEDIR = "nrep_prediction_exp"
PREDICTION_DIRS = {
#        "config" : "config",
        "input" : "input_files",
        "jobs": "jobs",
        "raw_data": "raw_data"       
                   }

PREDICTION_RESULTS_DIRS = {
       "summary": "results/summary",
       }
PREDICTION_PROCESSED_OUTPUT_FILENAME = "nrep_prediction_results.json"



EXEC_BASEDIR = "experiment_exec"
EXEC_DIRS = PREDICTION_DIRS

EXEC_RESULTS_DIRS = {
       "alldata": "results/alldata",
       "summary": "results/summary",
       "plots": "results/plots"
       }

CONFIG_BASEDIR = "config"


SCRIPT_DIRS = {
       "rscripts": "processing_scripts/rscripts"
       }


FINAL_FILENAMES = {
             "alldata": "data.txt",
             "guidelines_list": "guidelines_catalog.txt"
             }
BENCH_OUTPUT_FILENAME_PATTERN = ""
SUMMARIZED_DATA_FILENAME_EXTENSION = ".txt"
SUMMARIZED_DATA_FILENAME_PATTERN = "data.*\\.txt$"