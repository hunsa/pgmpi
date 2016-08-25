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
library(Rmisc)
library(logging)

source("common/readExpProperties.R")

############################################################

read_data_from_dir <- function(base_dir, pattern = "*.dat", properties = "", exclude = NA) {
  data_files <- list.files(base_dir, pattern = pattern)
  
  dflist <- list()
  
  if( length(data_files) <= 0 ) {
    warning(paste("no files found in", base_dir))
    dfres <- data.frame
  } else {
    for(i in 1:length(data_files)) {
      if (!is.na(exclude)) {
        if (grepl(exclude, data_files[i])) {
          next      
        }
      }

      fname = paste(base_dir,"/",data_files[i],sep="")
      loginfo(paste0("reading file: ", fname))
      df <- read.table(fname, header=TRUE, stringsAsFactors = FALSE)
      df <- set_properties(df, properties, fname)    
      
      df$nexp  <- i
      dflist[[i]] <- df
    }    
    dfres <- do.call(rbind, dflist)
  }
  
  dfres
}



write_data <- function(df_all, output_file) {
  dir.create(dirname(output_file), recursive = TRUE, showWarnings = FALSE)
  
  write.table(df_all,
              file = paste(output_file, sep = ''),
              col.names = TRUE,
              row.names = FALSE,
              quote = FALSE
  )
  print(paste("Data file created: ", basename(output_file), sep = ''))
}



remove_outlier <- function(df, column) {
  a <- quantile(df[, column], probs=c(.25,.75))
  limit <- a[2] + 1.5 * (a[2]-a[1])
  dfres <- df[df[, column]<=limit,]
  
  limit2 <- a[1] - 1.5 * (a[2]-a[1])
  dfres <- dfres[dfres[, column] >=limit2,]
  
  dfres
}


compute_stats <- function(df, column, remove_outliers = TRUE) {
  
  if (remove_outliers == FALSE) {
    df1 <- df
  }
  else {
    df1 <- remove_outlier(df, column)
  }
  
  time.ci=CI(df1[, column])
  ssize=length(df1[, column])
  quartiles <- quantile(df1[, column], probs=c(.25,.75))
  
  res <- data.frame(ci_lower=time.ci[[3]], ci_upper=time.ci[[1]], tmean=time.ci[[2]], ssize, 
                    sd=sd(df1[, column]), 
                    tmedian=median(df1[, column]), 
                    q1 = quartiles[1],
                    q3 = quartiles[2]
  )
  res
}



