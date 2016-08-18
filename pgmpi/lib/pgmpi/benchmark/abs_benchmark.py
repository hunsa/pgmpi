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