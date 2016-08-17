library(plyr)
library(ggplot2)
library(Rmisc)
library(grid)
library(stringr)

################################################
# Summarize experimental data into individual files for each measured MPI collective 
################################################

# Get command line arguments
args <- commandArgs(trailingOnly = TRUE)

setwd(args[1])

source("common/processBenchOutput.R")

data_file <- args[2]
output_dir <- args[3]

file_extension <- ""
if (length(args) == 4) {
  file_extension <- args[4]
}




df <- read.table(data_file, header=TRUE, stringsAsFactors = FALSE)

df1 <- ddply(df, .(test, msize, nexp), function(df) {  
  df1 <- compute_stats(df, "runtime_sec", remove_outliers = TRUE)
  df1
})  


# create summarized output for each mpi_collective 
all_tests <- unique(df1$test)

for(test in all_tests) {
  df2 <- df1[df1$test == test,]
  write_data(df2, paste(output_dir, "/data", test, file_extension, sep = ''))
}


