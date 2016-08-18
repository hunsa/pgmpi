
import os

from pgmpi.machsetup import abs_machine_setup

class PGMPIMachineConfiguratorLocal(abs_machine_setup.PGMPIAbstractMachineConfigurator):

    mpirun_path = "mpirun"
    mpi_common_args = "-bind-to core"
        
    
    def generate_prediction_job_contents(self, expconf, bench_binary_path, bench_args, remote_output_dir):
        nmpiruns = expconf.get_prediction_nmpiruns()
        
        job_contents = self.__gen_job_contents(expconf, bench_binary_path, bench_args, nmpiruns, remote_output_dir)
        return "\n".join(job_contents)
           
           
    def generate_verification_job_contents(self, expconf, bench_binary_path, bench_args, remote_output_dir):
        nmpiruns = expconf.get_verif_nmpiruns()
        
        job_contents = self.__gen_job_contents(expconf, bench_binary_path, bench_args, nmpiruns, remote_output_dir)
        return "\n".join(job_contents)



    def __gen_job_contents(self, expconf, bench_binary_path, bench_args, nmpiruns, remote_output_dir):
        
        nnp = expconf.get_num_nnp()
        nodes = expconf.get_num_nodes()
        
        assert(self.mpirun_path != ""), "No mpirun path specified. Please check the informations provided in the machine configuration script."
        
        check_bench = ["BENCH_BINARY_PATH=\"%s\"" % (bench_binary_path),
                       "if [ ! -x \"$BENCH_BINARY_PATH\" ]; then" , 
                        "echo \"Benchmark path incorrect: $BENCH_BINARY_PATH \"" ,
                        "exit 1",
                        "fi",
                        "\n"
                        ]  
 
        create_output_dir = ["OUTPUT_DIR=\"%s\"" % (remote_output_dir),
                             "mkdir -p \"$OUTPUT_DIR\"" ,
                             "mkdir -p \"$OUTPUT_DIR/logs\"",
                             "\n"
                             ]
        
        bench_call = "$BENCH_BINARY_PATH %s" % (bench_args) 
        mpirun_calls = []
        mpirun_args = self.__get_mpi_args(nodes, nnp)
        
        for i in range(0, nmpiruns):    
            # output files specified on the remote server
            outname = "$OUTPUT_DIR/mpi_bench_r%d.dat" % (i)
            outlogname = "$OUTPUT_DIR/logs/mpi_bench_r%d.log" % (i)
                
            mpirun_calls += [ "echo \"Starting mpirun %d...\"" %(i),
                              "%s %s %s > %s 2> %s" % ( self.mpirun_path, mpirun_args, 
                                                               bench_call,
                                                               outname, outlogname),
                            "echo \"Done.\"",
                            "\n"
                            ]
        return check_bench + create_output_dir + mpirun_calls



    def __get_mpi_args(self, nodes, nnp):
        return "-np %s -ppn %s %s" % (nodes * nnp, nnp, self.mpi_common_args)   



