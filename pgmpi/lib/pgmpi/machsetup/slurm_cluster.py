#    PGMPI - Performance Guideline Verification Tool for MPI Collectives
#
#    Copyright 2016 Alexandra Carpen-Amarie, Sascha Hunold
#    Research Group for Parallel Computing
#    Faculty of Informatics
#    Vienna University of Technology, Austria
# 
# 
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 2 of the License, or
#    (at your option) any later version.
# 
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
# 
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


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
        job_header.append("\n")
        
        check_bench = ["BENCH_BINARY_PATH=\"%s\"" % (bench_binary_path),
                       "if [ ! -f \"$BENCH_BINARY_PATH\" ]; then" , 
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
        
        for i in range(0, nmpiruns):    
            # output files specified on the remote server
            outname = "$OUTPUT_DIR/mpi_bench_r%d.dat" % (i)
            outlogname = "$OUTPUT_DIR/logs/mpi_bench_r%d.log" % (i)

            mpirun_calls += [ "echo \"Starting mpirun %d...\" " %(i),
                             "%s %s >> %s 2>> %s" % ( self.mpirun_call, 
                                                               bench_call,
                                                               outname, outlogname),
                            "echo \"Done.\" ",
                            "\n"
                            ]
        return job_header + check_bench + create_output_dir + mpirun_calls
            






