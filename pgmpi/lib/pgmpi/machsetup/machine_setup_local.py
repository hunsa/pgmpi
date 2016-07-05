
import os

from pgmpi.machsetup.machine_setup import PGMPIMachineConfigurator

class PGMPIMachineConfiguratorLocal(PGMPIMachineConfigurator):

    __mpirun_path = "mpirun"
    __mpi_common_args = "-bind-to core"
    

    def __init__(self, remote_basedir):
        self.__remote_basedir = remote_basedir

    def get_exp_output_dir (self):
        return self.__remote_basedir
    
    def generate_job_contents(self, expconf, bench_binary_path, bench_args):
                       
        check_bench = ["if [ ! -f %s ]; then " % (bench_binary_path), 
                        "echo \"Benchmark path incorrect: %s \" " % (bench_binary_path),
                        "exit 1",
                        "fi"
                        ]  
        
        expconfig_data = expconf.get_data()
        bench_call = "%s %s" % (bench_binary_path, bench_args) 
        job_contents = self.__gen_job_contents(expconfig_data, bench_call)
        
        job_contents = check_bench + job_contents
        return "\n".join(job_contents)
           




    def __gen_job_contents(self, expconfig_data, bench_call):
        create_output_dir = ["mkdir -p %s " % (self.__remote_basedir),
                             "mkdir -p %s/logs " % (self.__remote_basedir)
                             ]
        
        nnp = expconfig_data["nnp"]
        nodes = expconfig_data["nodes"]
        mpirun_calls = []
        mpirun_args = self.__get_mpi_args(expconfig_data)
        
        assert(self.__mpirun_path != ""), "No mpirun path specified. Please check the informations provided in the machine configuration script."
        
        for i in range(0, expconfig_data["nmpiruns"]):    
            # output files specified on the remote server
            outname = "%s/mpi_bench_r%d.dat" % ( self.__remote_basedir, i)
            outlogname = "%s/logs/mpi_bench_r%d.log" % ( self.__remote_basedir, i)
                
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
