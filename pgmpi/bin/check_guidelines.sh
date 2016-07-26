#!/bin/bash

function check_result {
    res_code=$1
    if [ $res_code -ne 0 ]; then
        exit 1
    fi
}


if [ $# -lt 5 ]
then
echo "Usage: $0 experiment_dir experiment_name exp_config guidelines_config machine_class [start_from_step]"
exit 1
fi


expdir=$1
expname=$2

expfile=$3
glfile=$4
machinefile=$5

step=1
if [ $# -eq 6 ]; then
    step=$6
fi


if [ $step -eq 1 ]; then
    ./bin/01-create_local_file_structure.py -i test_cases/local_test/experiment_def.py
    check_result $?

    ./bin/02-configure_prediction_run.py -d $expdir -n $expname -e $expfile -m $machinefile -g $glfile
    check_result $?

    echo "Execute generated prediction jobs before resuming from step 3."
fi


if [ $step -eq 3 ]; then
    ./bin/03-process_prediction_results.py -r $expdir/$expname/${expname}_nrep_prediction_exp/raw_data -o $expdir/$expname/${expname}_nrep_prediction_exp/results/summary
    check_result $?

    ./bin/04-configure_verifcation_run.py -n $expname -d $expdir -e $expfile -m $machinefile -g $glfile -p $expdir/$expname/${expname}_nrep_prediction_exp/results/summary/nrep_prediction_results.json
    check_result $?

    echo "Execute generated jobs before resuming from step 5."
fi


if [ $step -eq 5 ]; then
    ./bin/05-collect_raw_data.py -d $expdir -n $expname
    check_result $?

    ./bin/06-preprocess_raw_data.py -d $expdir -n $expname -m $machinefile -g $glfile
    check_result $?

    ./bin/07-verify_guidelines.py -d $expdir -n $expname
    check_result $?
fi


