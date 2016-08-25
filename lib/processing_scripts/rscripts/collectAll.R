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

library(plyr)
library(ggplot2)
library(Rmisc)
library(grid)
library(logging)

basicConfig()

################################################
# Collect experiment output data into a single file
################################################

# Get command line arguments
args <- commandArgs(trailingOnly = TRUE)

setwd(args[1])

source("common/processBenchOutput.R")

rawdata_dir <- args[2]
output_file <- args[3]

rawdata_pattern <- ""
if (length(args) == 4) {
  rawdata_pattern <- args[4]
}

print(rawdata_pattern)

# read data from ReproMPIbench-generated output
df <- read_data_from_dir(rawdata_dir, 
                        pattern = rawdata_pattern,
                        properties = NA,
                        exclude = "logs")

write_data(df, output_file)



