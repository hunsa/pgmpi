


from pgmpi.machsetup import slurm_cluster



class MySlurmConfigurator(slurm_cluster.PGMPIMachineConfiguratorSlurm):
    mpirun_call = "mpirun"
    slurm_job_name = "jobPGMPImpirun"
