



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
