
import os

from pgmpi.machsetup import abs_machine_setup

class PGMPIMachineConfiguratorSlurm(abs_machine_setup.PGMPIAbstractMachineConfigurator):
    
    mpirun_call = "srun"
    slurm_job_name = "jobPGMPI"
    
    
    def __init__(self, account = None, partition = None, qos = None, walltime = None):
        self.__slurm_account = account
        self.__slurm_qos = qos
        self.__slurm_partition = partition
        self.__slurm_walltime = walltime
            
    
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
        
        assert(self.mpirun_call != ""), "No mpirun path specified. Please check the informations provided in the machine configuration script."
        
        job_header = [
              "#!/usr/bin/env bash",
              "#SBATCH --nodes=%d" % nodes,
              "#SBATCH --ntasks-per-core=%d" % nnp,
              "#SBATCH --job-name=%s" % (self.slurm_job_name)
                    ]
        
        if self.__slurm_partition:
            job_header.append("#SBATCH --partition=%s" % (self.__slurm_partition))   
        if self.__slurm_account:
            job_header.append("#SBATCH --account=%s" % (self.__slurm_account))        
        if self.__slurm_qos:
            job_header.append("#SBATCH --qos=%s" % (self.__slurm_qos))
        if self.__slurm_walltime:
            job_header.append("#SBATCH --time=%s" % (self.__slurm_walltime))
        
        check_bench = ["if [ ! -f %s ]; then " % (bench_binary_path), 
                        "echo \"Benchmark path incorrect: %s \" " % (bench_binary_path),
                        "exit 1",
                        "fi"
                        ]  
 
        create_output_dir = ["mkdir -p %s " % (remote_output_dir),
                             "mkdir -p %s/logs " % (remote_output_dir)
                             ]
        
        bench_call = "%s %s" % (bench_binary_path, bench_args) 
        mpirun_calls = []
        
        for i in range(0, nmpiruns):    
            # output files specified on the remote server
            outname = "%s/mpi_bench_r%d.dat" % ( remote_output_dir, i)
            outlogname = "%s/logs/mpi_bench_r%d.log" % ( remote_output_dir, i)
                
            mpirun_calls += [ "echo \"Starting mpirun %d...\" " %(i),
                             "echo \"#@nodes=%s\" > %s " % (nodes, outname),
                             "echo \"#@nnp=%s\" >> %s " % (nnp, outname),
                             "%s %s >> %s 2>> %s" % ( self.mpirun_call, 
                                                               bench_call,
                                                               outname, outlogname),
                            "echo \"Done.\" ",
                            "\n"
                            ]
        return job_header + check_bench + create_output_dir + mpirun_calls
            






