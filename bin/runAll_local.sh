#!/bin/bash


expdir=$1
expname=$2

if [ $# -lt 2 ]
then
echo "Usage: $0 experiment_dir experiment_name"
exit 1
fi

./bin/setupExp.py -e test_cases/alex2/exp_config.json -m test_cases/alex2/local_mvapich2-2.1.json -g test_cases/alex2/exp_guidelines.json -d $expdir -n $expname --local_exec

./bin/configurePredictionExp.py -d $expdir -n $expname

#echo "Running prediction jobs"
./bin/runJobs.py -d $expdir/$expname/${expname}_nrep_prediction_exp
./bin/processPredictionResults.py -d $expdir/$expname/${expname}_nrep_prediction_exp


./bin/configureExp.py -n $expname -d $expdir -p $expdir/$expname/${expname}_nrep_prediction_exp/results/summary/nrep_prediction_results.json

./bin/runJobs.py -d $expdir/$expname/${expname}_experiment_exec/


./bin/collectAllData.py -d $expdir -n $expname
./bin/summarizeData.py -d $expdir -n $expname