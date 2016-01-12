
import os
import sys
import config_helpers as helpers
import machine_config as machine
from mpiguidelines.benchmark import benchmarks as bench
from mpiguidelines.common_exp_infos import *
            
def generate_mpiruns_list(config_data):
    exp = config_data["exp_info"]
    
    mpiruns = {}
       
    guidelines = exp["guidelines"]
    for guideline in guidelines.values():
        for (gindex, g) in enumerate(guideline):
            for msize in g["msizes"].keys():
                config = g["msizes"][msize]
                for i in xrange(int(config[1])):    
                    try: 
                        run = mpiruns[i]
                    except KeyError:
                        run = []
                    run.append({"mpicall": g["bench_mpicall"],  
                                "msize": msize,
                                                "nreps": config[0]
                                               } 
                                )
                    mpiruns[i] = run
    #i=0
    #for exp in mpiruns.values():      
    #    print(" mpirun %d " % i)
    #    print(exp)
    #    i = i+1
    return mpiruns
   



 
def generate_job_file(config_data, mpiruns):
    bench_info = config_data["mach_info"]["benchmark"]
    benchmark = bench.BENCHMARKS[bench_info["type"]](bench_info)

    exp_info = config_data["exp_info"]
    jobs_dir = os.path.join(
                          os.path.join(exp_info["exp_base_dir"], config_data["exp_name"]),
                                     EXP_DIRS["jobs"]
                                     )
    helpers.create_local_dir(jobs_dir)

    input_dir = os.path.join(
                          os.path.join(exp_info["exp_base_dir"], config_data["exp_name"]),
                                     EXP_DIRS["input"]
                                     )
    helpers.create_local_dir(input_dir)
    
    # input/output directories on the remote server
    remote_input_dir = os.path.join(
                          os.path.join(config_data["mach_info"]["remote_base_dir"], config_data["exp_name"]),
                                     EXP_DIRS["input"]
                                     )
    remote_output_dir = os.path.join(
                                     os.path.join(config_data["mach_info"]["remote_base_dir"], config_data["exp_name"]),
                                     EXP_DIRS["rawdata"]
                                     )
    

    mpirun_call = machine.get_mpi_call(exp_info["nodes"], exp_info["nnp"], config_data["mach_info"])

    # create job file in the jobs_dir, with the output path pointing to the remote output directory of the experiment     
    for runindex in mpiruns.keys():      
        run_info = mpiruns[runindex]
        
        if benchmark:
            benchmark.generate_input_files(input_dir, runindex, run_info)
            benchmark.generate_job_files(jobs_dir, remote_input_dir,
                remote_output_dir, mpirun_call, runindex, exp_info["nodes"],
                exp_info["nnp"], config_data["mach_info"]["scratch_dir"])
    
    
    
