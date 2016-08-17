
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


