import abc


class PGMPIMachineConfigurator:
    __metaclass__ = abc.ABCMeta

    #def create_prediction_jobs(self, expconfig_data, output_dir):
    #    pass
    
    @abc.abstractmethod
    def get_exp_output_dir (self):
        return ""

    @abc.abstractmethod
    def get_bench_path (self):
        pass

    @abc.abstractmethod
    def get_bench_type (self):
        pass
    
    @abc.abstractmethod
    def create_jobs(self, expconfig_data, bench_binary_path, bench_args, results_output_dir, job_output_dir):
        pass

