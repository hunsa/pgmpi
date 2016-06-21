
import os

from mpiguidelines.machine_setup import PGMPIMachineConfigurator

class PGMPIMachineConfiguratorJupiterNEC(PGMPIMachineConfigurator):

    mpirun_path = " /opt/NECmpi/gcc/inst/bin64/mpirun"
    mpi_common_args = "-pin_mode consec"

    exp_output_basedir = "/home/carpenamarie/code/test_pgmpi"

    bench_info = {     
                  "bench_path" : "/home/carpenamarie/code/mpibenchmark",
                  "type" : "reproMPI"
                  }

    input_file_name = "input"
    input_job_name = "job"


    def get_mpi_args(self, expconfig_data):
        nodes = expconfig_data["nodes"]
        nnp = expconfig_data["nnp"]
        
        return "-node 1-%s -nnp %s %s" % (nodes, nnp, self.mpi_common_args)   
    
    def get_exp_output_dir (self):
        return self.exp_output_basedir

    def get_bench_path (self):
        return self.bench_info["bench_path"]

    def get_bench_type (self):
        return self.bench_info["type"]
    
    def create_jobs(self, expconfig_data, bench_binary_path, bench_args, results_output_dir, job_output_dir):
        
        jobname = "%s.sh" %  (self.input_job_name)
        jobfile = os.path.join(job_output_dir, jobname)

        nnp = expconfig_data["nnp"]
        nodes = expconfig_data["nodes"]
        
        
        # mpi call info
        assert(self.mpirun_path != ""), "No mpirun path specified. Please check the informations provided in the machine configuration script."
        mpirun_args = self.get_mpi_args(expconfig_data)     
        
        check_bench = ["if [ ! -f %s ]; then " % (bench_binary_path), 
                        "echo \"Benchmark path incorrect: %s \" " % (bench_binary_path),
                        "exit 1",
                        "fi"
                        ]  

        create_output_dir = ["mkdir -p %s " % (results_output_dir),
                             "mkdir -p %s/logs " % (results_output_dir)
                             ]
        
        
        mpirun_calls = []
        for i in range(0, expconfig_data["nmpiruns"]):    
            # output files specified on the remote server
            outname = "%s/mpi_bench_r%d.dat" % ( results_output_dir, i)
            outlogname = "%s/logs/mpi_bench_r%d.log" % ( results_output_dir, i)
                
            mpirun_calls += [ "echo \"Starting mpirun %d...\" " %(i),
                             "echo \"#@nodes=%s\" > %s " % (nodes, outname),
                             "echo \"#@nnp=%s\" >> %s " % (nnp, outname),
                             "%s %s %s %s >> %s 2>> %s" % ( self.mpirun_path, mpirun_args, 
                                                               bench_binary_path, bench_args,
                                                               outname, outlogname),
                            "echo \"Done.\" ",
                            "\n"
                            ]
                             
        with open(jobfile, "w") as f:
            f.write("\n".join(check_bench) + "\n")
            f.write("\n".join(create_output_dir) + "\n")
            f.write("\n".join(mpirun_calls) + "\n")
           


