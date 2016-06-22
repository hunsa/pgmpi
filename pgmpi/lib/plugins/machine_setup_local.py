
import os

from mpiguidelines.machine_setup import PGMPIMachineConfigurator

class PGMPIMachineConfiguratorLocal(PGMPIMachineConfigurator):

    __mpirun_path = "mpirun"
    __mpi_common_args = "-bind-to core"

    __exp_output_basedir = "test_cases/output"

    __bench_path = "/Users/carpenamarie/Work/tuwien2014/code/mpibenchmark"

    __input_job_name = "job"
    
     
    def get_exp_output_dir (self):
        assert(self.__exp_output_basedir != ""), "No output directory path specified. Please check the informations provided in the machine configuration script."
        return self.__exp_output_basedir

    
         
    def setup_benchmark(self, benchmark_generator):
        self.__benchmark = benchmark_generator.create_benchmark_instance("reproMPI")
    
    
    def get_benchmark(self):
        return self.__benchmark
    
    
    def create_prediction_jobs(self, expconfig_data, remote_input_dir, remote_output_dir, job_output_dir):
        
        jobname = "%s.sh" %  (self.__input_job_name)
        jobfile = os.path.join(job_output_dir, jobname)
        
        bench_binary_path = self.__benchmark.get_prediction_bench_binary(self.__bench_path)
        bench_args = self.__benchmark.get_prediction_bench_args(remote_input_dir, expconfig_data) 
        bench_call = "%s %s" % (bench_binary_path, bench_args) 
                
        check_bench = ["if [ ! -f %s ]; then " % (bench_binary_path), 
                        "echo \"Benchmark path incorrect: %s \" " % (bench_binary_path),
                        "exit 1",
                        "fi"
                        ]  
        
        job_contents = self.__gen_job_contents(expconfig_data, remote_output_dir, bench_call)
        
        with open(jobfile, "w") as f:
            f.write("\n".join(check_bench) + "\n")
            f.write("\n".join(job_contents) + "\n")
           



    def create_verification_jobs(self, expconfig_data, remote_input_dir, remote_output_dir, job_output_dir):
        
        jobname = "%s.sh" %  (self.__input_job_name)
        jobfile = os.path.join(job_output_dir, jobname)
        
        bench_binary_path = self.__benchmark.get_verification_bench_binary(self.__bench_path)
        bench_args = self.__benchmark.get_verification_bench_args(remote_input_dir, expconfig_data) 
        bench_call = "%s %s" % (bench_binary_path, bench_args) 
        
        check_bench = ["if [ ! -f %s ]; then " % (bench_binary_path), 
                        "echo \"Benchmark path incorrect: %s \" " % (bench_binary_path),
                        "exit 1",
                        "fi"
                        ]  
        job_contents = self.__gen_job_contents(expconfig_data, remote_output_dir, bench_call)
                             
        with open(jobfile, "w") as f:
            f.write("\n".join(check_bench) + "\n")
            f.write("\n".join(job_contents) + "\n")





    def __gen_job_contents(self, expconfig_data, remote_output_dir, bench_call):
        create_output_dir = ["mkdir -p %s " % (remote_output_dir),
                             "mkdir -p %s/logs " % (remote_output_dir)
                             ]
        
        nnp = expconfig_data["nnp"]
        nodes = expconfig_data["nodes"]
        mpirun_calls = []
        mpirun_args = self.__get_mpi_args(expconfig_data)
        
        assert(self.__mpirun_path != ""), "No mpirun path specified. Please check the informations provided in the machine configuration script."
        
        for i in range(0, expconfig_data["nmpiruns"]):    
            # output files specified on the remote server
            outname = "%s/mpi_bench_r%d.dat" % ( remote_output_dir, i)
            outlogname = "%s/logs/mpi_bench_r%d.log" % ( remote_output_dir, i)
                
            mpirun_calls += [ "echo \"Starting mpirun %d...\" " %(i),
                             "echo \"#@nodes=%s\" > %s " % (nodes, outname),
                             "echo \"#@nnp=%s\" >> %s " % (nnp, outname),
                             "%s %s %s >> %s 2>> %s" % ( self.__mpirun_path, mpirun_args, 
                                                               bench_call,
                                                               outname, outlogname),
                            "echo \"Done.\" ",
                            "\n"
                            ]
        return create_output_dir + mpirun_calls
            


    def __get_mpi_args(self, expconfig_data):
        nodes = expconfig_data["nodes"]
        nnp = expconfig_data["nnp"]
        
        return "-np %s -ppn %s %s" % (nodes * nnp, nnp, self.__mpi_common_args)   
