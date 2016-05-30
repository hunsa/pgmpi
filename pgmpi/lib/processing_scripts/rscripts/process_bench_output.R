
library(plyr)
library(ggplot2)
library(Rmisc)
library(grid)
library(scales)
#library(tikzDevice)

source("readExpProperties.R")
my_colors <- c("#1C355B",  "#F28D69")#, "#9063cd", "#3E9651", "#CC2529" )
my_fillcolors <- c("#2e5796", "#f8c3af")#, "#9063cd", "#3E9651", "#CC2529" )

#my_colors <- c("#004265", "#C85200", "#0000FF")
#my_fillcolors <- c("#A2C8EC", "#FFF1E3", "#000099" )


############################################################

read_data <- function(base_dir, pattern = "*.dat") {
  data_files <- list.files(base_dir, pattern = pattern)
  
  dflist <- list()
  
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
  
  dfres
}




read_data_mpicroscope_kernel <- function(base_dir, fileprefix="experiment_results") {
  data_files <- list.files(base_dir)
  
  dflist <- list()
  
  for(i in 1:length(data_files)) {
    
    if( grepl(fileprefix, data_files[i]) == FALSE ) {
      next
    }
    
    print(data_files[i])
    
    pstr <- str_replace(data_files[i], fileprefix, "")
    
    splitted <- strsplit(pstr, "-")
    
    #print(paste(">", length(splitted[[1]]) ) )
    
    df <- read.table(paste(base_dir,"/",data_files[i],sep=""), header=TRUE)
    
    for( k in 1:length(splitted[[1]]) ) {
      
      #print(splitted[[1]][i])
      
      mat <- str_match(splitted[[1]][k], "([a-zA-Z]+)(\\d+)")
      
      if( ! is.na( mat[1] ) ) {
        #print(mat[2])  
        #print(mat[3])  
        
        df[, mat[2]] <- as.integer(mat[3])
      }
      
    }
    
    print(df[1,])
    
    
    dflist[[i]] <- df
  }
  
  dfres <- do.call(rbind, dflist)
  
  # Adapt to Alexandra's interface
  colnames(dfres) <- c("test", "Datatype_name", "Count", "msize", "runtime_sec", "nnp", "nnodes", "nexp")
  dfres$nprocs <- dfres$nnp * dfres$nnodes
  dfres$sync <- "BBarrier"
  dfres$nrep <- -1
  dfres <- dfres[,!(names(dfres) %in% c("Datatype_name", "Count", "nnodes"))]
  
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


generate_frame <- function(df, guideline, nprocs, nnp) {
  
  df1 <- df[df$nprocs == nprocs & df$nnp == nnp,]
  df2 <- df1[df1$test %in% guideline,]
  
  df2
}



process_data <- function(results_dir, output_dir) {
  dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)
  df_all <- read_data( results_dir)
  
  
  print("DONE: data read.")
  df2 <- ddply(df_all, .(test, msize, nprocs, nnp, nexp), function(df) {  
    df1 <- compute_stats(df, "runtime_sec")
    df1
  })  
  
  test_list <-  unique(df2$test)
  for (test in test_list) {
    write.table(df2[df2$test == test,],
                file = paste(output_dir,"/", test,".txt", sep = ''),
                col.names = TRUE,
                row.names = FALSE,
                quote = FALSE
                )
    
  }
}

