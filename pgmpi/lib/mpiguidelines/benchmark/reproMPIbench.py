import os
from __builtin__ import len

PREDICTION_BENCH_REL_PATH = "src/pred_bench/mpibenchmarkPredNreps"
REPROMPI_BENCH_REL_PATH = "mpibenchmark"

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
    input_file_name = "input.txt"

    def __init__(self, bench_path):
        self.bench_path = bench_path


    def translate_guideline(self, calls):
        for i in xrange(0,len(calls)):
            calls[i] = calls[i].strip()
        str_gl = "<".join(calls)
        try:
            translated = self.guidelines[str_gl]
        except KeyError:
            translated = None
        return translated


    # format for input data: { function_name1: { msize1 : { "nreps" : 10},
    #                                             msize2 : { "nreps" : 20},
    #                                          },
    #                          function_name2 ......
    #                           }
    def generate_input_files(self, inputfiles_dir, runindex, input_data):
        # create input files on the local machine
        inputfile = os.path.join(inputfiles_dir, self.input_file_name)

        with open(inputfile, "w") as f:
            for call in input_data.keys():
                test = input_data[call]
                for msize in test.keys():
                    e = test[msize]
                    f.write( "%s %d %d\n" % (call, msize, e["nreps"]))
        return


    def get_verification_bench_binary(self):
        return os.path.join(self.bench_path, REPROMPI_BENCH_REL_PATH)

    def get_prediction_bench_binary(self):
        return os.path.join(self.bench_path, PREDICTION_BENCH_REL_PATH)

    def get_prediction_bench_args(self, bench_inputfile_dir, expconfig_data):
        prediction_params = expconfig_data["prediction"]
        
        inputfile_path = os.path.join(bench_inputfile_dir, self.input_file_name)
        
        prediction_bench_params = "-f %s --rep-prediction min=%d,max=%d,step=%d --pred-method=%s --var-thres=%s --var-win=%s" % ( 
                                    inputfile_path,
                                    prediction_params["min"],
                                    prediction_params["max"], prediction_params["step"], 
                                    ",".join(prediction_params["methods"]),
                                    ",".join(map(str, prediction_params["thresholds"])),
                                    ",".join(map(str, prediction_params["windows"]))
                                    )
        return prediction_bench_params
    

    def get_verification_bench_args(self, bench_inputfile_dir, expconfig_data):
        inputfile_path = os.path.join(bench_inputfile_dir, self.input_file_name)
        
        bench_params = "-f %s" % (inputfile_path)
        return bench_params

