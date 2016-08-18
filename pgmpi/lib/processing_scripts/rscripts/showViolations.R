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


library(logging)

basicConfig()
options(width=200)
setLevel('WARNING', getHandler('basic.stdout'))


# Get command line arguments
args <- commandArgs(trailingOnly = TRUE)

setwd(args[1])

source("common/processBenchOutput.R")
source("pgmpir.R")

partial_res_dir <- args[2]
guidelines_list_file <- args[3]

partial_res_pattern <- ""
if (length(args) == 4) {
  partial_res_pattern <- args[4]
}


df <- read_data_from_dir(partial_res_dir, properties = NA,
                         pattern = partial_res_pattern)

dfgl <- read_gl_file(guidelines_list_file)

dfvio <- check_all_violations(df, dfgl)
    
print(dfvio)


