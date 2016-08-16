#!/bin/bash

function check_result {
    res_code=$1
    if [ $res_code -ne 0 ]; then
        exit 1
    fi
}


if [ $# -lt 1 ]
then
echo "Usage: $0 experiment_def_class [start_from_step]"
echo "       Experiment steps: - 1 create local directories"
echo "                         - 2 configure prediction experiment"
echo "                         - 3 process prediction results"
echo "                         - 4 configure guideline validation experiment"
echo "                         - 5 collect raw data"
echo "                         - 6 process raw data"
echo "                         - 7 verify guidelines"
exit 1
fi


expdef_file=$1

step=1
if [ $# -eq 2 ]; then
    step=$2
fi


if [ $step -eq 1 ]; then
    ./bin/01-create_local_file_structure.py -i ${expdef_file}
    check_result $?

    ./bin/02-configure_prediction_run.py -i ${expdef_file}
    check_result $?

    echo "Execute generated prediction jobs before resuming from step 3."
fi


if [ $step -eq 3 ]; then
    ./bin/03-process_prediction_results.py -i ${expdef_file}
    check_result $?

    ./bin/04-configure_verification_run.py -i ${expdef_file}
    check_result $?

    echo "Execute generated jobs before resuming from step 5."
fi


if [ $step -eq 5 ]; then
    ./bin/05-collect_raw_data.py -i ${expdef_file}
    check_result $?

    ./bin/06-preprocess_raw_data.py -i ${expdef_file}
    check_result $?

    ./bin/07-verify_guidelines.py -i ${expdef_file}
    check_result $?
fi


