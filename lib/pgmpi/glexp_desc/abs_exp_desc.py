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

from pgmpi.experiment import glexp
from pgmpi.benchmark import reproMPIbench
from pgmpi.machsetup import machine_setup_local

class AbstractExpDescription(object):
    __metaclass__ = abc.ABCMeta

    
    def setup_exp(self):
        
        bench    = reproMPIbench.GLReproMPIBench(self.benchmark_path_remote)
        machinfo = machine_setup_local.PGMPIMachineConfiguratorLocal()
   
        exp = glexp.GLExperimentWriter(bench, machinfo)

        return exp
    
    
    