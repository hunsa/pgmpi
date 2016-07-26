
library(logging)
library(reshape2)
library(plyr)


basicConfig()
options(width=200)
setLevel('WARNING', getHandler('basic.stdout'))

convert_significance <- function(sig_vector) {
  #  *   P <= 0.05
  #  **   P <= 0.01
  #  ***   P <= 0.001
  result_vec <- rep("", length(sig_vector))
  result_vec[ sig_vector>0.05 ] <- ""
  result_vec[ sig_vector<=0.05 ] <- "*"
  result_vec[ sig_vector<=0.01 ] <- "**"
  result_vec[ sig_vector<=0.001 ] <- "***"
  result_vec
}


read_gl_file <- function(fname="guidelines_catalog.txt") {
  dfres <- read.table(fname, header=TRUE)
  dfres
}


check_monotone_guideline <- function(df, func_name, conf.level=0.95) {
  
  dfres <- data.frame(
    "start" = numeric(0),
    "end"   = numeric(0),
    "func"  = character(0),
    "name"  = character(0),
    "significance" = character(0),
    "descr" = character(0),
     stringsAsFactors=FALSE
  )
  
  if( length(unique(df$test)) > 1 ) {
    warning("more than one MPI function found")
  }

  sig_level <- 1 - conf.level
  
  msizes <- sort(unique(df$msize))
  
  for(midx in 1:(length(msizes)-1)) {
    msize1 <- msizes[midx]
    msize2 <- msizes[midx+1]
    #print(paste(msize1, msize2))
    
    vals1 <- df[df$msize==msize1,]$tmedian
    vals2 <- df[df$msize==msize2,]$tmedian
    
    sres <- wilcox.test(vals1, vals2, alternative = "greater", conf.level = conf.level, exact = FALSE)
    
    #print(sres)
    
    #sres <- ks.test(vals1, vals2, alternative = "less", conf.level = conf.level, exact = FALSE)
    
    if(sres$p.value <= sig_level) {
      sig_level_str <- convert_significance(sres$p.value)
      dfres[nrow(dfres)+1, ] <- list(msize1, msize2, 
                                     func_name,
                                     "monotony", 
                                     sig_level_str, 
                                     sprintf("median(%d)=%g > median(%d)=%g", msize1, median(vals1), msize2, median(vals2)))
    }
    
    #print(summary(vals1))
    #print(summary(vals2))
  }

  
  dfres  
}



check_split_guideline <- function(df, func_name, runtime_thres=0.05) {
  
  dfres <- data.frame(
    "start" = numeric(0),
    "end"   = numeric(0),
    "func"  = character(0),
    "name"  = character(0),
    "significance" = character(0),
    "descr" = character(0),
    stringsAsFactors=FALSE
  )
  
  if( length(unique(df$test)) > 1 ) {
    warning("more than one MPI function found")
  }
  
  msizes <- sort(unique(df$msize))
  
  for(midx in 2:length(msizes)) {
    # larger
    msize1 <- msizes[midx]
    
    min_time   <- NA
    best_msize <- NA

    val1 <- median(df[df$msize==msize1,]$tmedian)
    
    for(midx2 in (midx-1):1) {
      # smaller
      msize2 <- msizes[midx2]
      
      fac <- ceiling(msize1/msize2)
      #print(paste("fac=", fac))
      #print(paste(msize1, msize2))

      val2 <- median(df[df$msize==msize2,]$tmedian)
      
      time_with_val2 <- val2 * fac
      
      if( (time_with_val2 + (1+runtime_thres) * time_with_val2)  < val1 ) {
        if( is.na(min_time) ) {
          min_time <- fac*val2
          best_msize <- msize2
        }
      }
    }
    
    if( ! is.na(min_time)) {
      fac <- ceiling(msize1/best_msize)
      dfres[nrow(dfres)+1, ] <- list(best_msize, msize1, 
                                     func_name,
                                     "split", "*", 
                                     sprintf("%d*t(%d)=%g < t(%d)=%g", 
                                             fac, best_msize, min_time, msize1, val1))
    }
    
  }
  
  
  dfres  
}



check_pattern_guideline <- function(df, df2, pattern_name, conf.level=0.95) {
  
  dfres <- data.frame(
    "start" = numeric(0),
    "end"   = numeric(0),
    "func"  = character(0),
    "name"  = character(0),
    "significance" = character(0),
    "descr" = character(0),
    stringsAsFactors=FALSE
  )
  
  sig_level <- 1 - conf.level
  
  #msizes <- sort(unique(df$msize))
  msizes <- sort(intersect(unique(df$msize), unique(df2$msize)))
  
  for(msize in msizes) {

    vals1 <- df [ df$msize==msize,]$tmedian
    vals2 <- df2[df2$msize==msize,]$tmedian
    
    sres <- wilcox.test(vals1, vals2, alternative = "greater", 
                        conf.level = conf.level, 
                        exact = FALSE)
  
#     print(paste0("median(vals1):", median(vals1)))
#     print(paste0("median(vals2):", median(vals2)))
#     print(sres)
    
    if(sres$p.value <= sig_level) {
      sig_level_str <- convert_significance(sres$p.value)
      dfres[nrow(dfres)+1, ] <- list("start"=msize, 
                                     "end"=msize, 
                                     "func"=pattern_name,
                                     "name"="pattern",
                                     "significance"=sig_level_str, 
                                     "descr"=sprintf("time(%d)=%g > time(%d)=%g", 
                                             msize, median(vals1), 
                                             msize, median(vals2)))
      
    }
    
  }
  
  dfres 
}  


append_guideline_violations <- function(dfres, dfcur) {
  if( nrow(dfres) <= 0 ) {
    dfres <- dfcur
  } else {
    dfres <- rbind(dfres, dfcur)
  }
  dfres
}

check_all_violations <- function(df, dfgl) {
  
  dfres <- data.frame()
  
  for(func in unique(dfgl$orig)) {
    
    df1 <- df[df$test==func,]
    
    if( nrow(df1) > 0 ) {
      
      loginfo(paste(func, nprocs, nnp))
      
      # get all pattern guidelines (the ones that have a second function mock and translated_mock defined)
      dfpat <- dfgl[dfgl$orig==func & (!is.na(dfgl$translated_mock)),]
      if( nrow(dfpat) <= 0 ) { # no pattern guideline defined for this function orig
        next
      }
      
      for(pat_idx in 1:nrow(dfpat)) {
        pattern_func <- dfpat[pat_idx,]$translated_mock
        pattern_str  <- as.character(dfpat[pat_idx,]$guideline)

        df2 <- df[df$test==pattern_func & df$nprocs==nprocs & df$nnp==nnp,]
        
        if( nrow(df2) <= 0 ) {
          warning(paste0("pattern ", pattern_func, " has no data"))
        } else {          
          loginfo(paste0("pattern ", pattern_func))
          dfpat_res <- check_pattern_guideline(df1, df2, pattern_str, conf.level = 0.95)
          dfres <- append_guideline_violations(dfres, dfpat_res)
#           if( nrow(dfpat_res) > 0 ) {
#             print(dfpat_res)
#           }
        }
      }
      
      
      df_mono <- check_monotone_guideline(df1, func)
      dfres <- append_guideline_violations(dfres, df_mono)
      
#       if( nrow(df_mono) > 0 ) {
#         print(df_mono)
#       }
      
      df_split <- check_split_guideline(df1, func)
      dfres <- append_guideline_violations(dfres, df_split)
      
#       if( nrow(df_split) > 0 ) {
#         print(df_split)
#       }
      
    }
  }  
  
  dfres
}




# Get command line arguments
args <- commandArgs(trailingOnly = TRUE)

setwd(args[1])

source("common/processBenchOutput.R")

partial_res_dir <- args[2]
guidelines_list_file <- args[3]

partial_res_pattern <- ""
if (length(args) == 4) {
  partial_res_pattern <- args[4]
}


df <- read_data_from_dir(partial_res_dir, properties = NA,
                         pattern = partial_res_pattern)

dfgl <- read_gl_file(guidelines_list_file)

for(nprocs in unique(df$nprocs)) {
  for(nnp in unique(df$nnp)) {
    
    dft <- df[df$nprocs==nprocs & df$nnp==nnp,]
    
    dfvio <- check_all_violations(dft, dfgl)
    
    print(paste0("Total number of processes: ", nprocs, " (", nprocs/nnp, "x", nnp, ")"))
    print(dfvio)
    
  }
}


