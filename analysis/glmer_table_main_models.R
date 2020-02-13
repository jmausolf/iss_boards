##########################################
## Fixed Party Models
##########################################

#Set Options
# models <- list(m1lr, m2lr, m3lr, m4lr)
# ttitle = "Cross-Classified Random Effects Logit Models of the Likelihood that the New Board Member is a Republican, 1 Year Lag, Odds Ratios Displayed"
# dvar = "Pr\\{New Board Member: Republican\\}"
# outfile = "output/tables/glmer_models_republican_lag1.tex"
# note_content <- "Cross-classified random effects (CCRE) logistic regression model with fixed 1-year lag. Cross-classifed andom intercepts include firm and year. Measure of board-member partisanship: \\textit{party}, which is fixed across election cycles."


#Set Options
# models <- list(m1lr2, m2lr2, m3lr2, m4lr2)
# ttitle = "Cross-Classified Random Effects Logit Models of the Likelihood that the New Board Member is a Republican, 2 Year Lag, Odds Ratios Displayed"
# dvar = "Pr\\{New Board Member: Republican\\}"
# outfile = "output/tables/glmer_models_republican_lag2.tex"
# note_content <- "Cross-classified random effects (CCRE) logistic regression model with fixed 2-year lag. Cross-classifed andom intercepts include firm and year. Measure of board-member partisanship: \\textit{party}, which is fixed across election cycles."


#Set Options
# models <- list(m1lr_all, m2lr_all, m3lr_all, m4lr_all)
# ttitle = "Cross-Classified Random Effects Logit Models of the Likelihood that the New Board Member is a Republican, 1-11 Year Lags, Odds Ratios Displayed"
# dvar = "Pr\\{New Board Member: Republican\\}"
# outfile = "output/tables/glmer_models_republican_lag_all.tex"
# note_content <- "Cross-classified random effects (CCRE) logistic regression model, all lags (1-year, 11-year) included. Cross-classifed andom intercepts include firm, year, and lag-year. Measure of board-member partisanship: \\textit{party}, which is fixed across election cycles."
# all_lags = TRUE


#Set Options
# models <- list(m1ld, m2ld, m3ld, m4ld)
# ttitle = "Cross-Classified Random Effects Logit Models of the Likelihood that the New Board Member is a Democrat, 1 Year Lag, Odds Ratios Displayed"
# dvar = "Pr\\{New Board Member: Democrat\\}"
# outfile = "output/tables/glmer_models_democrat_lag1.tex"
# note_content <- "Cross-classified random effects (CCRE) logistic regression model with fixed 1-year lag. Cross-classifed andom intercepts include firm and year. Measure of board-member partisanship: \\textit{party}, which is fixed across election cycles."


#Set Options
# models <- list(m1ld2, m2ld2, m3ld2, m4ld2)
# ttitle = "Cross-Classified Random Effects Logit Models of the Likelihood that the New Board Member is a Democrat, 2 Year Lag, Odds Ratios Displayed"
# dvar = "Pr\\{New Board Member: Democrat\\}"
# outfile = "output/tables/glmer_models_democrat_lag2.tex"
# note_content <- "Cross-classified random effects (CCRE) logistic regression model with fixed 2-year lag. Cross-classifed andom intercepts include firm and year. Measure of board-member partisanship: \\textit{party}, which is fixed across election cycles."


#Set Options
# models <- list(m1ld_all, m2ld_all, m3ld_all, m4ld_all)
# ttitle = "Cross-Classified Random Effects Logit Models of the Likelihood that the New Board Member is a Democrat, 1-11 Year Lags, Odds Ratios Displayed"
# dvar = "Pr\\{New Board Member: Democrat\\}"
# outfile = "output/tables/glmer_models_democrat_lag_all.tex"
# note_content <- "Cross-classified random effects (CCRE) logistic regression model, all lags (1-year, 11-year) included. Cross-classifed andom intercepts include firm, year, and lag-year. Measure of board-member partisanship: \\textit{party}, which is fixed across election cycles."
# all_lags = TRUE



##########################################
## Varying Party Cycle Models
##########################################

#Set Options
# models <- list(mc1lr, mc2lr, mc3lr, mc4lr)
# ttitle = "Cross-Classified Random Effects Logit Models of the Likelihood that the New Board Member is a Republican, 1 Year Lag, Odds Ratios Displayed"
# dvar = "Pr\\{New Board Member: Republican\\}"
# outfile = "output/tables/glmer_models_republican_lag1_cycle.tex"
# note_content <- "Cross-classified random effects (CCRE) logistic regression model with fixed 1-year lag. Cross-classifed andom intercepts include firm and year. Measure of board-member partisanship: \\textit{party-cycle}, which may vary across election cycles."


#Set Options
# models <- list(mc1lr2, mc2lr2, mc3lr2, mc4lr2)
# ttitle = "Cross-Classified Random Effects Logit Models of the Likelihood that the New Board Member is a Republican, 2 Year Lag, Odds Ratios Displayed"
# dvar = "Pr\\{New Board Member: Republican\\}"
# outfile = "output/tables/glmer_models_republican_lag2_cycle.tex"
# note_content <- "Cross-classified random effects (CCRE) logistic regression model with fixed 2-year lag. Cross-classifed andom intercepts include firm and year. Measure of board-member partisanship: \\textit{party-cycle}, which may vary across election cycles."


#Set Options
# models <- list(mc1lr_all, mc2lr_all, mc3lr_all, mc4lr_all)
# ttitle = "Cross-Classified Random Effects Logit Models of the Likelihood that the New Board Member is a Republican, 1-11 Year Lags, Odds Ratios Displayed"
# dvar = "Pr\\{New Board Member: Republican\\}"
# outfile = "output/tables/glmer_models_republican_lag_all_cycle.tex"
# note_content <- "Cross-classified random effects (CCRE) logistic regression model, all lags (1-year, 11-year) included. Cross-classifed andom intercepts include firm, year, and lag-year. Measure of board-member partisanship: \\textit{party-cycle}, which may vary across election cycles."
# all_lags = TRUE


#Set Options
# models <- list(mc1ld, mc2ld, mc3ld, mc4ld)
# ttitle = "Cross-Classified Random Effects Logit Models of the Likelihood that the New Board Member is a Democrat, 1 Year Lag, Odds Ratios Displayed"
# dvar = "Pr\\{New Board Member: Democrat\\}"
# outfile = "output/tables/glmer_models_democrat_lag1_cycle.tex"
# note_content <- "Cross-classified random effects (CCRE) logistic regression model with fixed 1-year lag. Cross-classifed andom intercepts include firm and year. Measure of board-member partisanship: \\textit{party-cycle}, which may vary across election cycles."


#Set Options
# models <- list(mc1ld2, mc2ld2, mc3ld2, mc4ld2)
# ttitle = "Cross-Classified Random Effects Logit Models of the Likelihood that the New Board Member is a Democrat, 2 Year Lag, Odds Ratios Displayed"
# dvar = "Pr\\{New Board Member: Democrat\\}"
# outfile = "output/tables/glmer_models_democrat_lag2_cycle.tex"
# note_content <- "Cross-classified random effects (CCRE) logistic regression model with fixed 2-year lag. Cross-classifed andom intercepts include firm and year. Measure of board-member partisanship: \\textit{party-cycle}, which may vary across election cycles."


#Set Options
# models <- list(mc1ld_all, mc2ld_all, mc3ld_all, mc4ld_all)
# ttitle = "Cross-Classified Random Effects Logit Models of the Likelihood that the New Board Member is a Democrat, 1-11 Year Lags, Odds Ratios Displayed"
# dvar = "Pr\\{New Board Member: Democrat\\}"
# outfile = "output/tables/glmer_models_democrat_lag_all_cycle.tex"
# note_content <- "Cross-classified random effects (CCRE) logistic regression model, all lags (1-year, 11-year) included. Cross-classifed andom intercepts include firm, year, and lag-year. Measure of board-member partisanship: \\textit{party-cycle}, which may vary across election cycles."
# all_lags = TRUE





#asr
r = 37
r2 = 42
d = 3


re1l = "Firm"
re2l = "Year"
re3l = "Lag-Year"

#Add Insert Row Function
insertrow <- function(existingDF, newrow, r) {
  existingDF[seq(r+1,nrow(existingDF)+1),] <- existingDF[seq(r,nrow(existingDF)),]
  existingDF[r,] <- newrow
  existingDF
}

# Create some standard rows to add.
randomeffect <- "{\\textit{Level-2 Random Intercepts}} & & & &\\\\"
hline <- "\\hline"
hline2 <- "\\hline \\\\[-1.8ex]"
newline <- "\\\\"
blankline <- " & & & & \\\\"

# Make Note
note_form <- "\\multicolumn{5}{l}{\\parbox[t]{\\textwidth}{{\\textit{Notes:}}"
tnote <- paste(note_form, note_content, "}}", "\\\\", sep=" ")
tnote



m1 = models[[1]]
m2 = models[[2]]
m3 = models[[3]]
m4 = models[[4]]


#make base tables
tables <- stargazer3(models,
                     odd.ratio = T,
                     star.cutoffs = c(0.05, 0.01, 0.001),
                     align = TRUE,
                     initial.zero = TRUE,
                     # no.space = TRUE,
                     column.sep.width = "0pt",
                     header = FALSE,
                     font.size = "scriptsize",
                     style = "asr",
                     title = ttitle,
                     dep.var.labels   = dvar,
                     covariate.labels = c("\\textit{Boards and Firm Politics} \\\\Board Member Added",
                                          "Board Member Equal Swap",
                                          "Republican Board",
                                          "Democratic Firm",
                                          "Republican Firm",
                                          
                                          "\\\\ \\textit{Board Features} \\\\ Board Size (Log)",
                                          "Median Age (Log)",
                                          "Proportion Female",
                                          "Proportion Black or Hispanic",
                                          "Proportion Minority",
                                          "Proportion Non-US",
                                          "Median Outside Board Ties",
                                          
                                          "\\\\ \\textit{Firm Sectors} \\\\ Capital Goods",
                                          "Conglomerates",
                                          "Consumer Cyclical",
                                          "Consumer Goods",
                                          "Consumer/Non-Cyclical",
                                          "Energy",
                                          "Financial",
                                          "Healthcare",
                                          "Services",
                                          "Technology",
                                          "Transportation",
                                          "Utilities",

                                          "\\\\ \\textit{Other Features} \\\\ U.S. President (Democrat)",
                                          "Constant"),
                     notes.append = TRUE, notes.align = "l"
                     )

tables <- as.data.frame(tables)
tables$tables <- as.character(tables$tables)
tables

#Add Table Note
tables <- insertrow(tables, tnote, r2)

#Start Random Effects
tables <- insertrow(tables, blankline, r)
tables <- insertrow(tables,randomeffect,r+1)

#Get number of RE's
num.re1.m1 <- sapply(ranef(m1),nrow)[1]
num.re2.m1 <- sapply(ranef(m1),nrow)[2]

num.re1.m2 <- sapply(ranef(m2),nrow)[1]
num.re2.m2 <- sapply(ranef(m2),nrow)[2]

num.re1.m3 <- sapply(ranef(m3),nrow)[1]
num.re2.m3 <- sapply(ranef(m3),nrow)[2]

num.re1.m4 <- sapply(ranef(m4),nrow)[1]
num.re2.m4 <- sapply(ranef(m4),nrow)[2]

if(all_lags == TRUE) {
   num.re3.m1 <- sapply(ranef(m1),nrow)[3]
   num.re3.m2 <- sapply(ranef(m2),nrow)[3]
   num.re3.m3 <- sapply(ranef(m3),nrow)[3]
   num.re3.m4 <- sapply(ranef(m4),nrow)[3]
}


#Get Variance
var.re1.m1 <- as.data.frame(VarCorr(m1))$vcov[1]
var.re2.m1 <- as.data.frame(VarCorr(m1))$vcov[2]

var.re1.m2 <- as.data.frame(VarCorr(m2))$vcov[1]
var.re2.m2 <- as.data.frame(VarCorr(m2))$vcov[2]

var.re1.m3 <- as.data.frame(VarCorr(m3))$vcov[1]
var.re2.m3 <- as.data.frame(VarCorr(m3))$vcov[2]

var.re1.m4 <- as.data.frame(VarCorr(m4))$vcov[1]
var.re2.m4 <- as.data.frame(VarCorr(m4))$vcov[2]

if(all_lags == TRUE) {
   var.re3.m1 <- as.data.frame(VarCorr(m1))$vcov[3]
   var.re3.m2 <- as.data.frame(VarCorr(m2))$vcov[3]
   var.re3.m3 <- as.data.frame(VarCorr(m3))$vcov[3]
   var.re3.m4 <- as.data.frame(VarCorr(m4))$vcov[3]
}


#make RE row entries
num.re1 <- paste0(re1l, "s &", num.re1.m1, "&", num.re1.m2, "&", num.re1.m3, "&", num.re1.m4, "\\\\")
var.re1 <- paste0(re1l, " Variance &", round(var.re1.m1, d), "&", round(var.re1.m2, d), "&", round(var.re1.m3, d), "&", round(var.re1.m4, d), "\\\\")

num.re2 <- paste0(re2l, "s &", num.re2.m1, "& ", num.re2.m2, "& ", num.re2.m3, "& ", num.re2.m4, "\\\\")
var.re2 <- paste0(re2l, " Variance &", round(var.re2.m1, d), "&", round(var.re2.m2, d), "&", round(var.re2.m3, d), "&", round(var.re2.m4, d), "\\\\")

if(all_lags == TRUE) {
   num.re3 <- paste0(re3l, "s &", num.re3.m1, "& ", num.re3.m2, "& ", num.re3.m3, "& ", num.re3.m4, "\\\\")
   var.re3 <- paste0(re3l, " Variance &", round(var.re3.m1, d), "&", round(var.re3.m2, d), "&", round(var.re3.m3, d), "&", round(var.re3.m4, d), "\\\\")
}



#add rows
if(all_lags == TRUE) {
   tables <- insertrow(tables,var.re1, r+2)
   tables <- insertrow(tables,var.re2, r+3)
   tables <- insertrow(tables,var.re3, r+4)
   tables <- insertrow(tables, hline2, r+5)
   tables <- insertrow(tables,newline, r+6)
   tables <- insertrow(tables,num.re1, r+8)
   tables <- insertrow(tables,num.re2, r+9)
   tables <- insertrow(tables,num.re3, r+10)
} else {
   tables <- insertrow(tables,var.re1, r+2)
   tables <- insertrow(tables,var.re2, r+3)
   tables <- insertrow(tables, hline2, r+4)
   tables <- insertrow(tables,newline, r+5)
   tables <- insertrow(tables,num.re1, r+7)
   tables <- insertrow(tables,num.re2, r+8)
}




write.table(tables,file=outfile,sep="",row.names= FALSE,na="", quote = FALSE, col.names = FALSE)
