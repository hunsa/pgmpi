library(plyr)
library(ggplot2)
library(Rmisc)
library(grid)

################################################
# Collect experiment output data into a single file
################################################

# Get command line arguments
args <- commandArgs(trailingOnly = TRUE)

setwd(args[1])

source("common/process_bench_output.R")

rawdata_dir <- args[2]
output_file <- args[3]


df <- read_data(rawdata_dir)

write_data(df, output_file)



