



PREDICTION_BASEDIR = "01-nrep_prediction_exp"
PREDICTION_DIRS = {
#        "config" : "config",
        "input" : "jobs/input_files",
        "jobs": "jobs",
        "raw_data": "jobs/raw_data"       
                   }

PREDICTION_RESULTS_DIRS = {
       "summary": "results/summary",
       }
PREDICTION_PROCESSED_OUTPUT_FILENAME = "nrep_prediction_results.json"



EXEC_BASEDIR = "02-experiment_exec"
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



DEFAULT_CONFIG_DIR = "default_config"
GUIDELINE_CATALOG_FILE = "guideline_catalog.json"
GUIDELINE_CONFIG_FILE = "guideline_conf.json"
EXP_CONF_FILE = "experiment_conf.py"





