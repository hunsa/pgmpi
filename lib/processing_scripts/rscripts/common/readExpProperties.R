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
  if (!is.na(properties)[1]) {
    prop_df <- read_properties(filename)
    for (prop in properties)
    {
      df[prop] <- prop_df[prop]
    }
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

