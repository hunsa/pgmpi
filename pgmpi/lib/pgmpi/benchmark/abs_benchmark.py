import abc

class BenchmarkGenerator:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod    
    def translate_name(self, call):
        pass

    @abc.abstractmethod
    def generate_input_file_data(self, input_data):
        pass

    @abc.abstractmethod
    def get_verification_bench_binary(self, bench_path):
        pass


    @abc.abstractmethod
    def get_prediction_bench_binary(self, bench_path):
        pass


    @abc.abstractmethod
    def get_prediction_bench_args(self, bench_inputfile_dir, expconfig_data):
        pass 

    @abc.abstractmethod
    def get_verification_bench_args(self, bench_inputfile_dir, expconfig_data):
        pass