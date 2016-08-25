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


from pgmpi.expconfig import abs_expconfig
from pgmpi.helpers import file_helpers 

class GLExperimentalConfig (abs_expconfig.AbstractExperimentalConfig):

    
    def __init__(self, exp_conf_file):
        self.__exp_conf_data = file_helpers.read_json_config_file(exp_conf_file)
        self.__exp_conf_filepath = exp_conf_file
    
    def get_conf_filepath(self):
        return self.__exp_conf_filepath
   
    def get_num_nodes(self):
        return self.__exp_conf_data["nodes"]

    def get_num_nnp(self):
        return self.__exp_conf_data["nnp"]
    
    def get_verif_nmpiruns(self):
        return self.__exp_conf_data["nmpiruns"]
    
    def get_prediction_nmpiruns(self):
        return self.__exp_conf_data["prediction"]["nmpiruns"]    
        
    def get_prediction_min_nrep(self):
        return self.__exp_conf_data["prediction"]["min"]

    def get_prediction_max_nrep(self):
        return self.__exp_conf_data["prediction"]["max"]
    
    def get_prediction_step_nrep(self):
        return self.__exp_conf_data["prediction"]["step"]
    
    def get_prediction_methods(self):
        return self.__exp_conf_data["prediction"]["methods"]
    
    def get_prediction_threshold(self, method):
        for i in range(len(self.__exp_conf_data["prediction"]["methods"])):
            if self.__exp_conf_data["prediction"]["methods"][i] == method:
                return self.__exp_conf_data["prediction"]["thresholds"][i]
        return None
        
        
    def get_prediction_window(self, method):
        for i in range(len(self.__exp_conf_data["prediction"]["methods"])):
            if self.__exp_conf_data["prediction"]["methods"][i] == method:
                return self.__exp_conf_data["prediction"]["windows"][i]
        return None
    
    