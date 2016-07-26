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
                        properties = c("nnp", "nprocs", "sync"),
                        exclude = "logs")

write_data(df, output_file)



