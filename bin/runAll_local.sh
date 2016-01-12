#!/bin/bash


expdir=$1
expname=$2

if [ $# -lt 2 ]
then
echo "Usage: $0 experiment_dir experiment_name"
exit 1
fi

./bin/setupExp.py -e data/exp_config.json -m data/local_mvapich2-2.1.json -d $expdir -n $expname --local_exec
./bin/runJobs.py -d $expdir -n $expname
./bin/collectAllData.py -d $expdir -n $expname
./bin/summarizeData.py -d $expdir -n $expname