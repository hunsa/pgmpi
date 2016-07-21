import abc


class PGMPIMachineConfigurator:
    __metaclass__ = abc.ABCMeta

    #def create_prediction_jobs(self, expconfig_data, output_dir):
    #    pass
    

    @abc.abstractmethod
    def generate_prediction_job_contents(self, expconf, bench_binary_path, bench_args):
        pass

    @abc.abstractmethod
    def generate_verification_job_contents(self, expconf, bench_binary_path, bench_args):
        pass    
