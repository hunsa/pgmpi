
import mpiguidelines.benchmark.reproMPIbench as reproMPI
import mpiguidelines.benchmark.mpicroscope_kernel as mpicroscope_kernel 


class BenchmarkGenerator:
    
    __benchmark_list = { "reproMPI": reproMPI.ReproMPI,
                        "mpicroscope_kernel": mpicroscope_kernel.mpicroscope_kernel
                        } 
    
        
    def create_benchmark_instance(self, bench_type):
        return self.__benchmark_list[bench_type]()