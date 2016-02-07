library(plyr)
library(ggplot2)
library(Rmisc)
library(grid)
library(stringr)

# Get command line arguments
args <- commandArgs(trailingOnly = TRUE)

setwd(args[1])

source("process_bench_output.R")

guidelines_file <- args[2]
data_file <- args[3]
output_dir <- args[4]


guidelines <- read.table(guidelines_file, header=TRUE)
df <- read.table(data_file, header=TRUE, stringsAsFactors = FALSE)

df1 <- ddply(df, .(test, msize, nprocs, nnp, nexp), function(df) {  
  df1 <- compute_stats(df, "runtime_sec")
  df1
})  

for(i in 1:nrow(guidelines)) {
  g <- guidelines[i,]

  df2 <- df1[df1$test == g$f1 | df1$test == g$f2,]
  write_data(df2, paste(output_dir, "/data", gsub("<", "_", g$guideline), ".txt", sep = ''))
}



