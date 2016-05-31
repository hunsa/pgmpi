
library(Rmisc)
library(stringr)


############################################################

read_properties <- function(filename) 
{
  df <-data.frame(1:1)
  con  <- file(filename, open = "r")
  while (length(line <- readLines(con, n = 1)) > 0 )
  {
    result <- str_match(line, "#@(.*)=(.*)")
    if (!is.na(result[1,2])) 
    {
      df[result[1,2]] <- result[1,3]
    }
    else
    {
      comment <- str_match(line, "#.*")
      if (is.na(comment[1,1])) {
        break
      } 
    }
  }
  close(con)
  df[,1] <- NULL
  df
}


# set properties in vector "properties" to each column of data frame df
set_properties <- function(df, properties, filename)
{ 
  prop_df <- read_properties(filename)
  for (prop in properties)
  {
    df[prop] <- prop_df[prop]
  }
  
  df
}


# set all properties from filename to each column of data frame df
set_all_properties <- function(df, filename)
{
  prop_df <- read_properties(filename)
  for (col in colnames(prop_df))
  {
    df[col] <- prop_df[col]
  }
  
  df
}

