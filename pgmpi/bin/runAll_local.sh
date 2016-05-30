#!/bin/bash


expdir=$1
expname=$2

expfile=$3
machinefile=$4
glfile=$5

if [ $# -lt 5 ]
then
echo "Usage: $0 experiment_dir experiment_name exp_config machine_config guidelines_config"
exit 1
fi

./bin/setupExp.py -e $expfile -m $machinefile -g $glfile -d $expdir -n $expname --local_exec

./bin/configurePredictionExp.py -d $expdir -n $expname

#echo "Running prediction jobs"
./bin/runJobs.py -d $expdir/$expname/${expname}_nrep_prediction_exp
./bin/processPredictionResults.py -d $expdir/$expname/${expname}_nrep_prediction_exp


./bin/configureExp.py -n $expname -d $expdir -p $expdir/$expname/${expname}_nrep_prediction_exp/results/summary/nrep_prediction_results.json

./bin/runJobs.py -d $expdir/$expname/${expname}_experiment_exec/


./bin/collectAllData.py -d $expdir -n $expname
./bin/summarizeData.py -d $expdir -n $expname
