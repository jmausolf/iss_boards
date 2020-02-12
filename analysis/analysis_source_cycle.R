####################################
## CORE LIBRARIES
####################################


setwd("~/Box Sync/Dissertation_v2/CH3_BoardEx/iss_boards/analysis/")


##Load Libraries
library(tidyverse)
library(stargazer)
library(knitr)
library(pastecs)
library(forcats)
library(stringr)
library(lubridate)
library(scales)
library(DBI)
library(ggsci)
library(rbokeh)
library(bbplot)
library(magrittr)
library(qwraps2)
library(RColorBrewer)
library(ggthemes)
library(fastDummies)

#Overwrite bbplot finalise_plot() function
source("bb_finalise_plot_academic.R")




####################################
## CORE FOLDERS
####################################

system("mkdir -p output")
system("mkdir -p output/plots")
system("mkdir -p output/tables")


####################################
## CORE UTIL FUNCTIONS
####################################

#Function for Fixing Odds Ratios Pvals (from glm)
stargazer2 <- function(model, odd.ratio = F, ...) {
if(!("list" %in% class(model))) model <- list(model)

if (odd.ratio) {
  coefOR2 <- lapply(model, function(x) exp(coef(x)))
  seOR2 <- lapply(model, function(x) exp(coef(x)) * summary(x)$coef[, 2])
  p2 <- lapply(model, function(x) summary(x)$coefficients[, 4])
  stargazer(model, coef = coefOR2, se = seOR2, p = p2, ...)
  
} else {
  stargazer(model, ...)
}
}

#Function for Fixing Odds Ratios Pvals (from glmer)
stargazer3 <- function(model, odd.ratio = F, ...) {
  if(!("list" %in% class(model))) model <- list(model)
  
  if (odd.ratio) {
    coefOR2 <- lapply(model, function(x) exp(fixef(x)))
    seOR2 <- lapply(model, function(x) exp(fixef(x)) * summary(x)$coef[, 2])
    p2 <- lapply(model, function(x) summary(x)$coefficients[, 4])
    stargazer(model, coef = coefOR2, se = seOR2, p = p2, ...)
    
  } else {
    stargazer(model, ...)
  }
}

#Change Append = TRUE to Not Overwrite Files
save_stargazer <- function(output.file, ...) {
  output <- capture.output(stargazer(...))
  cat(paste(output, collapse = "\n"), "\n", file=output.file, append = FALSE)
}


#Change Append = TRUE to Not Overwrite Files
save_stargazer2 <- function(output.file, ...) {
  output <- capture.output(stargazer2(...))
  cat(paste(output, collapse = "\n"), "\n", file=output.file, append = FALSE)
}

#Change Append = TRUE to Not Overwrite Files
save_stargazer3 <- function(output.file, ...) {
  output <- capture.output(stargazer3(...))
  cat(paste(output, collapse = "\n"), "\n", file=output.file, append = FALSE)
}


wout <- function(plt_type, cid){
  outfile <- paste0("output/plots/", plt_type, "_", str_replace_all(tolower(cid), " ", "_"), ".png")
  return(outfile)
}


####################################
## CORE DATA SOURCE - All 
####################################



dfb <- read_csv("../data/ISS/ISS_ANALYSIS_cycle.csv")
print(df)


# dfx <- read_csv("../data/ISS/ISS_Boards.csv")
# print(df)
# 
# df <- dfx %>% 
#   select(company_id, name, First_name, Last_name, year) %>% 
#   distinct()
# 
# df <- dfb %>% 
#   select(ticker, cid_master) %>% 
#   distinct()
# 
# table(dfx$Country_of_Empl)
# table(dfx$Interlocking)
# table(dfx$Ethnicity)
# table(dfx$female)
# table(dfx$Age)
# table(dfx$Outside_Public_Boards)
