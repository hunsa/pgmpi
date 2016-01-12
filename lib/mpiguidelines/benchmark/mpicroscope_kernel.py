import os
import random

class mpicroscope_kernel:
    
    guidelines = {"MPI_Gather<MPI_Allgather" : ["Gather", "Allgather"],
                  "MPI_Gather<MPI_Reduce" : ["Gather", "Reduce"],
                  "MPI_Allgather<MPI_Alltoall" : ["Allgather", "Alltoall"],
                  "MPI_Allgather<MPI_Allreduce" : ["Allgather", "Allreduce"],
                  "MPI_Scatter<MPI_Bcast" : ["Scatter", "Bcast"],
                  "MPI_Reduce<MPI_Allreduce" : ["Reduce", "Allreduce"],
                  #"MPI_Bcast<MPI_Scatter+MPI_Allgather" : ["MPI_Bcast", "GL_ScatterAllgather"],
                  #"MPI_Allgather<MPI_Gather+MPI_Bcast" : ["MPI_Allgather", "GL_GatherBcast"],
                  #"MPI_Allreduce<MPI_Reduce+MPI_Bcast" : ["MPI_Allreduce", "GL_ReduceBcast"]
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

        run_shuffled = list(run)
        random.shuffle(run_shuffled)
        with open(inputfile, "w") as f:
            for e in run_shuffled:                
                f.write( "%s %s %s %d\n" % (e["mpicall"], "MPI_BYTE", e["msize"], e["nreps"]))
        return


    def generate_job_files(self, jobs_dir, remote_input_dir, remote_output_dir, mpirun_call, 
                           runindex, nodes, nnp, scratch_dir):
        
        jobname = "%s_%d.sh" %  (self.input_job_name, runindex)
        jobfile = os.path.join(jobs_dir, jobname)
        
        # path to input/output files specified on the remote server 
        inputname = "%s_%d.txt" %  (self.input_file_name, runindex)
        inputfile = os.path.join(remote_input_dir, inputname)
        
        outname = "%s/mpi_bench_r%d.dat" % ( remote_output_dir, runindex)
        outlogname = "%s/logs/mpi_bench_r%d" % ( remote_output_dir, runindex)
            
        with open(jobfile, "w") as f:
            f.write( "mkdir -p %s \n" % (remote_output_dir) )
            f.write( "mkdir -p %s/logs \n" % (remote_output_dir) )        
            f.write( "mkdir -p %s \n" % (outlogname) )        
            call = "%s %s -i %s -r %s -l %s --experiment_block_len=1 \n" \
                           % ( mpirun_call, self.bench_info["bench_path"],
                               inputfile, outname, outlogname)
            f.write(call)
            tempfile = "%s/mpicroscope_kernel_output_temp" % scratch_dir
            f.write( "echo \"#@mpiargs=%s\" | cat - %s >%s && mv %s %s\n"
                %(mpirun_call, outname, tempfile, tempfile, outname))
            f.write( "echo \"#@nodes=%s\" | cat - %s >%s && mv %s %s\n"
                %(nodes, outname, tempfile, tempfile, outname))
            f.write( "echo \"#@nnp=%s\" | cat - %s >%s && mv %s %s\n" %(nnp,
              outname, tempfile, tempfile, outname))
            # Delete empty log files:
            f.write( "find %s -empty | xargs -r rm\n" % outlogname)
            f.write( "[ ! \"$(ls -A %s)\" ] && echo %s >> %s/../empty_logs_list "
                "&& rm -r %s\n" % (outlogname, outlogname, outlogname, outlogname))
