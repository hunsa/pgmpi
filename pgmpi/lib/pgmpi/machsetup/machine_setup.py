import abc


class PGMPIMachineConfigurator:
    __metaclass__ = abc.ABCMeta

    #def create_prediction_jobs(self, expconfig_data, output_dir):
    #    pass
    
    @abc.abstractmethod
    def get_exp_output_dir (self):
        return ""
    
    @abc.abstractmethod
    def generate_job_contents(self, expconf, bench_binary_path, bench_args):
        pass

    
