import abc


class PGMPIAbstractMachineConfigurator:
    __metaclass__ = abc.ABCMeta


    @abc.abstractmethod
    def generate_prediction_job_contents(self, expconf, bench_binary_path, bench_args):
        pass

    @abc.abstractmethod
    def generate_verification_job_contents(self, expconf, bench_binary_path, bench_args):
        pass    
