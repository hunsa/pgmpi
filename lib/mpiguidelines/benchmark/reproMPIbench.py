import os

class ReproMPI:

    guidelines = {"MPI_Gather<MPI_Allgather" : ["MPI_Gather", "MPI_Allgather"],
                  "MPI_Gather<MPI_Reduce" : ["MPI_Gather", "GL_Reduce"],
                  "MPI_Allgather<MPI_Alltoall" : ["MPI_Allgather", "MPI_Alltoall"],
                  "MPI_Allgather<MPI_Allreduce" : ["MPI_Allgather", "GL_Allreduce"],
                  "MPI_Scatter<MPI_Bcast" : ["MPI_Scatter", "GL_Bcast"],
                  "MPI_Reduce<MPI_Allreduce" : ["MPI_Reduce", "MPI_Allreduce"],
                  #"MPI_Bcast<MPI_Scatter+MPI_Allgather" : ["MPI_Bcast", "GL_ScatterAllgather"],
                  "MPI_Allgather<MPI_Gather+MPI_Bcast" : ["MPI_Allgather", "GL_GatherBcast"],
                  "MPI_Allreduce<MPI_Reduce+MPI_Bcast" : ["MPI_Allreduce", "GL_ReduceBcast"]
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
            for (index, e) in enumerate(run):
                f.write( "%s %s %d\n" % (e["mpicall"], e["msize"], e["nreps"]))
        return


    def generate_job_files(self, jobs_dir, remote_input_dir, remote_output_dir, mpirun_call,
                           runindex, nodes, nnp, scratch_dir):

        jobname = "%s_%d.sh" %  (self.input_job_name, runindex)
        jobfile = os.path.join(jobs_dir, jobname)

        # path to input/output files specified on the remote server
        inputname = "%s_%d.txt" %  (self.input_file_name, runindex)
        inputfile = os.path.join(remote_input_dir, inputname)

        outname = "%s/mpi_bench_r%d.dat" % ( remote_output_dir, runindex)
        outlogname = "%s/logs/mpi_bench_r%d.log" % ( remote_output_dir, runindex)

        with open(jobfile, "w") as f:
            f.write( "mkdir -p %s \n" % (remote_output_dir) )
            f.write( "mkdir -p %s/logs \n" % (remote_output_dir) )
            f.write( "echo \"#@mpiargs=%s\" >> %s \n" %(mpirun_call, outname))
            f.write( "echo \"#@nodes=%s\" >> %s \n" %(nodes, outname))
            f.write( "echo \"#@nnp=%s\" >> %s \n" %(nnp, outname))
            call = "%s %s/mpibenchmark -f %s >> %s 2>> %s \n" \
                           % ( mpirun_call, self.bench_info["bench_path"], inputfile,
                               outname, outlogname)

            f.write(call)






