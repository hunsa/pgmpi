
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
        
        check_bench = ["if [ ! -f %s ]; then" % (bench_binary_path), 
                        "echo \"Benchmark path incorrect: %s \"" % (bench_binary_path),
                        "exit 1",
                        "fi"
                        ]  
 
        create_output_dir = ["mkdir -p %s" % (remote_output_dir),
                             "mkdir -p %s/logs" % (remote_output_dir)
                             ]
        
        bench_call = "%s %s" % (bench_binary_path, bench_args) 
        mpirun_calls = []
        mpirun_args = self.__get_mpi_args(nodes, nnp)
        
        for i in range(0, nmpiruns):    
            # output files specified on the remote server
            outname = "%s/mpi_bench_r%d.dat" % ( remote_output_dir, i)
            outlogname = "%s/logs/mpi_bench_r%d.log" % ( remote_output_dir, i)
                
            mpirun_calls += [ "echo \"Starting mpirun %d...\"" %(i),
                             "echo \"#@nodes=%s\" > %s" % (nodes, outname),
                             "echo \"#@nnp=%s\" >> %s" % (nnp, outname),
                             "%s %s %s >> %s 2>> %s" % ( self.mpirun_path, mpirun_args, 
                                                               bench_call,
                                                               outname, outlogname),
                            "echo \"Done.\"",
                            "\n"
                            ]
        return check_bench + create_output_dir + mpirun_calls
            



    def __get_mpi_args(self, nodes, nnp):
        return "-np %s -ppn %s %s" % (nodes * nnp, nnp, self.mpi_common_args)   



