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

from pgmpi.glexp_desc import abs_exp_desc
from pgmpi.experiment import glexp
from pgmpi.benchmark import reproMPIbench
from pgmpi.machsetup import slurm_cluster


class ExpDescription(abs_exp_desc.AbstractExpDescription):
    # Path to the ReproMPI benchmark binaries on the target machine 
    # (more info on how to install ReproMPI can be found here: 
    # https://github.com/hunsa/reprompi)
    benchmark_path_remote = "/home/carpenamarie/reprompi-1.0.0/bin"

 
    def setup_exp(self):

        bench    = reproMPIbench.GLReproMPIBench(self.benchmark_path_remote)
        machinfo = slurm_cluster.PGMPIMachineConfiguratorSlurm(qos="normal_0064", 
                                                               partition="mem_0064", 
                                                               account = None, 
                                                               walltime = None)
   
        exp = glexp.GLExperimentWriter(bench, machinfo)

        return exp
    
    
    
    