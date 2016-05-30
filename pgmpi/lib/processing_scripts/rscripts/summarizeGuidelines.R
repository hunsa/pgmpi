library(plyr)
library(ggplot2)
library(Rmisc)
library(grid)
library(stringr)

# Get command line arguments
args <- commandArgs(trailingOnly = TRUE)

setwd(args[1])

source("process_bench_output.R")

#guidelines_file <- args[2]
data_file <- args[2]
output_dir <- args[3]


#guidelines <- read.table(guidelines_file, header=TRUE)
df <- read.table(data_file, header=TRUE, stringsAsFactors = FALSE)

df1 <- ddply(df, .(test, msize, nprocs, nnp, nexp), function(df) {  
  df1 <- compute_stats(df, "runtime_sec")
  df1
})  


# create summarized output for each mpi_collective 
all_tests <- unique(df1$test)

for(test in all_tests) {
  df2 <- df1[df1$test == test,]
  write_data(df2, paste(output_dir, "/data", test, ".txt", sep = ''))
}


# for(i in 1:nrow(guidelines)) {
#   g <- guidelines[i,]
# 
#   df2 <- df1[df1$test == g$f1 | df1$test == g$f2,]
#   write_data(df2, paste(output_dir, "/data", gsub("<", "_lte_", g$guideline), ".txt", sep = ''))
# }



