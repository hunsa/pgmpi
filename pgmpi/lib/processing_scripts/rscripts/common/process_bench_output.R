
library(plyr)
library(Rmisc)

source("common/readExpProperties.R")

############################################################

read_data <- function(base_dir, pattern = "*.dat") {
  data_files <- list.files(base_dir, pattern = pattern)
  
  dflist <- list()
  
  if( length(data_files) <= 0 ) {
    warning(paste("no files found in", base_dir))
    dfres <- data.frame
  } else {
    for(i in 1:length(data_files)) {
      print(data_files[i])
      if (grepl("nodesfile", data_files[i])) {
        next      
      }
      
      df <- read.table(paste(base_dir,"/",data_files[i],sep=""), header=TRUE, stringsAsFactors = FALSE)
      df <- set_properties(df, c("nnp", "nprocs", "sync"),
                           paste(base_dir,"/",data_files[i],sep=""))    
      #print(df[1,])
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



