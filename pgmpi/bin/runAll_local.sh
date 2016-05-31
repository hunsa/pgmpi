#!/bin/bash

function check_result {
    res_code=$1
    if [ $res_code -ne 0 ]; then
        exit 1
    fi
}

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
check_result $?

./bin/configurePredictionExp.py -d $expdir -n $expname
check_result $?

#echo "Running prediction jobs"
./bin/runJobs.py -d $expdir/$expname/${expname}_nrep_prediction_exp
check_result $?

./bin/processPredictionResults.py -d $expdir/$expname/${expname}_nrep_predction_exp
check_result $?

./bin/configureExp.py -n $expname -d $expdir -p $expdir/$expname/${expname}_nrep_prediction_exp/results/summary/nrep_prediction_results.json
check_result $?

./bin/runJobs.py -d $expdir/$expname/${expname}_experiment_exec/
check_result $?

./bin/collectAllData.py -d $expdir -n $expname
check_result $?

./bin/summarizeData.py -d $expdir -n $expname
check_result $?

./bin/checkViolations.py -d $expdir -n $expname
check_result $?