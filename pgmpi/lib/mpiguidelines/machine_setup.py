import abc


class PGMPIMachineConfigurator:
    __metaclass__ = abc.ABCMeta

    #def create_prediction_jobs(self, expconfig_data, output_dir):
    #    pass
    
    @abc.abstractmethod
    def get_exp_output_dir (self):
        return ""

    @abc.abstractmethod
    def setup_benchmark(self, benchmark_generator):
        pass

    @abc.abstractmethod
    def get_benchmark(self):
        pass
    
    @abc.abstractmethod
    def create_prediction_jobs(self, expconfig_data, remote_input_dir, remote_output_dir, job_output_dir):
        pass

    @abc.abstractmethod
    def create_verification_jobs(self, expconfig_data, remote_input_dir, remote_output_dir, job_output_dir):
        pass

     