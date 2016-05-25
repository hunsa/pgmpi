import os
from __builtin__ import len

class ReproMPI:

    guidelines = {"MPI_Allgather<MPI_Allgather_with_MPI_Alltoall" : ["MPI_Allgather", "GL_Allgather_as_Alltoall"],
                  "MPI_Allgather<MPI_Allgather_with_MPI_Allreduce" : ["MPI_Allgather", "GL_Allgather_as_Allreduce"],
                  "MPI_Allgather<MPI_Allgather_with_MPI_Gather_MPI_Bcast" : ["MPI_Allgather", "GL_Allgather_as_GatherBcast"],
                  "MPI_Allreduce<MPI_Allreduce_with_MPI_Reduce_MPI_Bcast" : ["MPI_Allreduce", "GL_Allreduce_as_ReduceBcast"],
                  "MPI_Allreduce<MPI_Allreduce_with_MPI_Reduce_scatter_MPI_Allgather" : ["MPI_Allreduce", "GL_Allreduce_as_ReducescatterAllgather"],
                  "MPI_Allreduce<MPI_Allreduce_with_MPI_Reduce_scatter_block_MPI_Allgather" : ["MPI_Allreduce", "GL_Allreduce_as_ReducescatterblockAllgather"],
                  "MPI_Bcast<MPI_Bcast_with_MPI_Scatter_MPI_Allgather" : ["MPI_Bcast", "GL_Bcast_as_ScatterAllgather"],
                  "MPI_Gather<MPI_Gather_with_MPI_Allgather" : ["MPI_Gather", "GL_Gather_as_Allgather"],
                  "MPI_Gather<MPI_Gather_with_MPI_Reduce" : ["MPI_Gather", "GL_Gather_as_Reduce"],
                  "MPI_Reduce<MPI_Reduce_with_MPI_Allreduce" : ["MPI_Reduce", "GL_Reduce_as_Allreduce"],
                  "MPI_Reduce<MPI_Reduce_with_MPI_Reduce_scatter_MPI_Gather" : ["MPI_Reduce", "GL_Reduce_as_ReducescatterGather"],
                  "MPI_Reduce<MPI_Reduce_with_MPI_Reduce_scatter_block_MPI_Gather" : ["MPI_Reduce", "GL_Reduce_as_ReducescatterblockGather"],
                  "MPI_Reduce_scatter_block<MPI_Reduce_scatter_block_with_MPI_Reduce_MPI_Scatter" : ["MPI_Reduce_scatter_block", "GL_Reduce_scatter_block_as_ReduceScatter"],
                  "MPI_Reduce_scatter<MPI_Reduce_scatter_with_MPI_Allreduce" : ["MPI_Reduce_scatter", "GL_Reduce_scatter_as_Allreduce"],
                  "MPI_Reduce_scatter<MPI_Reduce_scatter_with_MPI_Reduce_MPI_Scatterv" : ["MPI_Reduce_scatter", "GL_Reduce_scatter_as_ReduceScatterv"],
                  "MPI_Scan<MPI_Scan_with_MPI_Exscan_MPI_Reduce_local" : ["MPI_Scan", "GL_Scan_as_ExscanReducelocal"],
                  "MPI_Scatter<MPI_Scatter_with_MPI_Bcast" : ["MPI_Scatter", "GL_Scatter_as_Bcast"]
                  }
    input_file_name = "input"
    input_job_name = "job"

    def __init__(self, bench_info):
        self.bench_info = bench_info


    def translate_guideline(self, calls):
        for i in xrange(0,len(calls)):
            calls[i] = calls[i].strip()
        str_gl = "<".join(calls)
        try:
            translated = self.guidelines[str_gl]
        except KeyError:
            translated = None
        return translated


    def generate_input_files(self, inputfiles_dir, runindex, run):
        # create input files on the local machine
        inputname = "%s_%d.txt" %  (self.input_file_name, runindex)
        inputfile = os.path.join(inputfiles_dir, inputname)

        with open(inputfile, "w") as f:
            for call in run.keys():
                test = run[call]
                for msize in test.keys():
                    e = test[msize]
                    f.write( "%s %d %d\n" % (call, msize, e["nreps"]))
        return


    def generate_and_write_job_files(self, jobs_dir, remote_input_dir, remote_output_dir, mpirun_call,
                           nmpiruns, nodes, nnp, job_header, additional_bench_params = "", scratch_dir = ""):

        jobname = "%s.sh" %  (self.input_job_name)
        jobfile = os.path.join(jobs_dir, jobname)

        n_input_files = 1
        with open(jobfile, "w") as f:
            f.write(job_header)
            f.write( "mkdir -p %s \n" % (remote_output_dir) )
            f.write( "mkdir -p %s/logs \n" % (remote_output_dir) )
            
            for i in range(0, nmpiruns):
                
                # path to input/output files specified on the remote server
                inputname = "%s_%d.txt" %  (self.input_file_name, n_input_files)
                inputfile = os.path.join(remote_input_dir, inputname)

                outname = "%s/mpi_bench_r%d.dat" % ( remote_output_dir, i)
                outlogname = "%s/logs/mpi_bench_r%d.log" % ( remote_output_dir, i)
                
                f.write( "echo \"#@mpiargs=%s\" >> %s \n" %(mpirun_call, outname))
                f.write( "echo \"#@nodes=%s\" >> %s \n" %(nodes, outname))
                f.write( "echo \"#@nnp=%s\" >> %s \n" %(nnp, outname))
                call = "%s %s/mpibenchmark -f %s %s >> %s 2>> %s \n" \
                           % ( mpirun_call, self.bench_info["bench_path"], inputfile,
                               additional_bench_params, outname, outlogname)

                f.write(call)
                f.write("\n\n")



    def generate_and_write_prediction_job_files(self, jobs_dir, remote_input_dir, remote_output_dir, mpirun_call,
                           nodes, nnp, prediction_params, job_header, scratch_dir = ""):

        jobname = "%s.sh" %  (self.input_job_name)
        jobfile = os.path.join(jobs_dir, jobname)
        
        assert(prediction_params["max"] > 0), "Specify a maximum number of repetitions for the nrep prediction algorithm"
        for method in prediction_params["methods"]:
            assert(method in ["rse", "cov_mean", "cov_median"]), "Specify a defined prediction method (one of res, cov_mean, cov_median)"
        assert(len(prediction_params["thresholds"]) == len(prediction_params["methods"])), \
                    "The number of thresholds has to match the number of specified prediction methods"
        assert(len(prediction_params["windows"]) == len(prediction_params["methods"])),   \
                    "The number of prediction windows has to match the number of specified prediction methods"
        
        prediction_bench_params = "--rep-prediction min=%d,max=%d,step=%d --pred-method=%s --var-thres=%s --var-win=%s" % ( 
                                    prediction_params["min"],
                                    prediction_params["max"], prediction_params["step"], 
                                    ",".join(prediction_params["methods"]),
                                    ",".join(map(str, prediction_params["thresholds"])),
                                    ",".join(map(str, prediction_params["windows"]))
                                    )


        n_input_files = 1
        with open(jobfile, "w") as f:
            f.write(job_header)
            f.write( "mkdir -p %s \n" % (remote_output_dir) )
            f.write( "mkdir -p %s/logs \n" % (remote_output_dir) )
            
            for i in range(0, prediction_params["nmpiruns"]):
                
                # path to input/output files specified on the remote server
                inputname = "%s_%d.txt" %  (self.input_file_name, n_input_files)
                inputfile = os.path.join(remote_input_dir, inputname)

                outname = "%s/mpi_bench_r%d.dat" % ( remote_output_dir, i)
                outlogname = "%s/logs/mpi_bench_r%d.log" % ( remote_output_dir, i)
                
                f.write( "echo \"Starting mpirun %d...\" \n" %(i))
                f.write( "echo \"#@mpiargs=%s\" > %s \n" %(mpirun_call, outname))
                f.write( "echo \"#@nodes=%s\" >> %s \n" %(nodes, outname))
                f.write( "echo \"#@nnp=%s\" >> %s \n" %(nnp, outname))
                call = "%s %s/src/pred_bench/mpibenchmarkPredNreps -f %s %s >> %s 2>> %s \n" \
                           % ( mpirun_call, self.bench_info["bench_path"], inputfile,
                               prediction_bench_params, outname, outlogname)

                f.write(call)
                f.write( "echo \"Done.\" ")
                f.write("\n\n")




