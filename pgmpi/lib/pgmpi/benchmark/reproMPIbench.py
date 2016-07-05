import os
from __builtin__ import len

PREDICTION_BENCH_REL_PATH = "src/pred_bench/mpibenchmarkPredNreps"
REPROMPI_BENCH_REL_PATH = "mpibenchmark"

from pgmpi.benchmark import abs_benchmark

class GLReproMPIBench (abs_benchmark.BenchmarkGenerator):
    
    __mockup_functions = {"MPI_Allgather_with_MPI_Alltoall" : "GL_Allgather_as_Alltoall",
                  "MPI_Allgather_with_MPI_Allreduce" : "GL_Allgather_as_Allreduce",
                  "MPI_Allgather_with_MPI_Gather_MPI_Bcast" :  "GL_Allgather_as_GatherBcast",
                  "MPI_Allreduce_with_MPI_Reduce_MPI_Bcast" : "GL_Allreduce_as_ReduceBcast",
                  "MPI_Allreduce_with_MPI_Reduce_scatter_MPI_Allgather" : "GL_Allreduce_as_ReducescatterAllgather",
                  "MPI_Allreduce_with_MPI_Reduce_scatter_block_MPI_Allgather" :  "GL_Allreduce_as_ReducescatterblockAllgather",
                  "MPI_Bcast_with_MPI_Scatter_MPI_Allgather" : "GL_Bcast_as_ScatterAllgather",
                  "MPI_Gather_with_MPI_Allgather" : "GL_Gather_as_Allgather",
                  "MPI_Gather_with_MPI_Reduce" :  "GL_Gather_as_Reduce",
                  "MPI_Reduce_with_MPI_Allreduce" : "GL_Reduce_as_Allreduce",
                  "MPI_Reduce_with_MPI_Reduce_scatter_MPI_Gather" :"GL_Reduce_as_ReducescatterGather",
                  "MPI_Reduce_with_MPI_Reduce_scatter_block_MPI_Gather" :  "GL_Reduce_as_ReducescatterblockGather",
                  "MPI_Reduce_scatter_block_with_MPI_Reduce_MPI_Scatter" :  "GL_Reduce_scatter_block_as_ReduceScatter",
                  "MPI_Reduce_scatter_with_MPI_Allreduce" :  "GL_Reduce_scatter_as_Allreduce",
                  "MPI_Reduce_scatter_with_MPI_Reduce_MPI_Scatterv" :  "GL_Reduce_scatter_as_ReduceScatterv",
                  "MPI_Scan_with_MPI_Exscan_MPI_Reduce_local" : "GL_Scan_as_ExscanReducelocal",
                  "MPI_Scatter_with_MPI_Bcast" :"GL_Scatter_as_Bcast"
                  }
    

    def __init__(self, bench_path):
        self.__bench_path = bench_path

    def translate_name(self, call):
        if call in self.__mockup_functions:
            return self.__mockup_functions[call]   
        return call


    # intial format for input data: { function_name1: { msize1 : { "nreps" : 10},
    #                                             msize2 : { "nreps" : 20},
    #                                          },
    #                          function_name2 ......
    #                           }
    # translate input file data into the correct format for the benchmark
    def generate_input_file_data(self, input_data):
        file_contents = []
        for call in input_data.keys():
            test = input_data[call]
            for msize in test.keys():
                e = test[msize]
                translated_name = self.translate_name(call)
                file_contents.append( "%s %d %d" % (translated_name, msize, e["nreps"]))
        return "\n".join(file_contents)
                

    def get_verification_bench_binary(self):
        return os.path.join(self.__bench_path, REPROMPI_BENCH_REL_PATH)

    def get_prediction_bench_binary(self):
        return os.path.join(self.__bench_path, PREDICTION_BENCH_REL_PATH)

    def get_prediction_bench_args(self, bench_inputfile_dir, expconfig_data):
        prediction_params = expconfig_data["prediction"]
        
        inputfile_path = os.path.join(bench_inputfile_dir, self.__input_file_name)
        
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
        inputfile_path = os.path.join(bench_inputfile_dir, self.__input_file_name)
        
        bench_params = "-f %s" % (inputfile_path)
        return bench_params

