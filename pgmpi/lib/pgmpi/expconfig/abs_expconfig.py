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



class AbstractExperimentalConfig():
    __metaclass__ = abc.ABCMeta

    
    @abc.abstractmethod 
    def get_conf_filepath(self):
        pass
   
    @abc.abstractmethod 
    def get_num_nodes(self):
        pass

    @abc.abstractmethod 
    def get_num_nnp(self):
        pass
    
    @abc.abstractmethod 
    def get_verif_nmpiruns(self):
        pass
    
    @abc.abstractmethod 
    def get_prediction_nmpiruns(self):
        pass
        
    @abc.abstractmethod 
    def get_prediction_min_nrep(self):
        pass

    @abc.abstractmethod 
    def get_prediction_max_nrep(self):
        pass
    
    @abc.abstractmethod 
    def get_prediction_step_nrep(self):
        pass
    
    @abc.abstractmethod 
    def get_prediction_methods(self):
        pass
    
    @abc.abstractmethod 
    def get_prediction_threshold(self, method):
        pass
        
    @abc.abstractmethod 
    def get_prediction_window(self, method):
        pass