##########################################
## Fixed Party Models
##########################################


#Set Options
# models <- list(mlr_2, mlr_4, mlr_6, mlr_8)
# ttitle = "Cross-Classified Random Effects Logit Models of the Likelihood that the New Board Member is a Republican, Odds Ratios Displayed"
# dvar = "Pr\\{New Board Member: Republican\\}"
# outfile = "output/tables/glmer_models_republican_multilag.tex"
# note_content <- "Cross-classified random effects (CCRE) logistic regression model with discrete multiyear lags. That is, each model uses a discrete set of year lags as follows: 1-2 year lags, 1-4 year lags, 1-6 year lags, and 1-8 year lags. Cross-classified random intercepts include firm, year, and lag years. Measure of board-member partisanship: \\textit{party}, which is fixed across election cycles."
# mlabel = "tab:rep_multilag"


#Set Options
# models <- list(mld_2, mld_4, mld_6, mld_8)
# ttitle = "Cross-Classified Random Effects Logit Models of the Likelihood that the New Board Member is a Democrat, Odds Ratios Displayed"
# dvar = "Pr\\{New Board Member: Democrat\\}"
# outfile = "output/tables/glmer_models_democrat_multilag.tex"
# note_content <- "Cross-classified random effects (CCRE) logistic regression model with discrete multiyear lags. That is, each model uses a discrete set of year lags as follows: 1-2 year lags, 1-4 year lags, 1-6 year lags, and 1-8 year lags. Cross-classified random intercepts include firm, year, and lag years. Measure of board-member partisanship: \\textit{party}, which is fixed across election cycles."
# mlabel = "tab:dem_multilag"


##########################################
## Varying Party Cycle Models
##########################################

#Set Options
# models <- list(mclr_2, mclr_4, mclr_6, mclr_8)
# ttitle = "Cross-Classified Random Effects Logit Models of the Likelihood that the New Board Member is a Republican, Odds Ratios Displayed"
# dvar = "Pr\\{New Board Member: Republican\\}"
# outfile = "output/tables/glmer_models_republican_multilag_cycle.tex"
# note_content <- "Cross-classified random effects (CCRE) logistic regression model with discrete multiyear lags. That is, each model uses a discrete set of year lags as follows: 1-2 year lags, 1-4 year lags, 1-6 year lags, and 1-8 year lags. Cross-classified random intercepts include firm, year, and lag years. Measure of board-member partisanship: \\textit{party-cycle}, which may vary across election cycles."
# mlabel = "tab:rep_multilag_cycle"


#Set Options
# models <- list(mcld_2, mcld_4, mcld_6, mcld_8)
# ttitle = "Cross-Classified Random Effects Logit Models of the Likelihood that the New Board Member is a Democrat, Odds Ratios Displayed"
# dvar = "Pr\\{New Board Member: Democrat\\}"
# outfile = "output/tables/glmer_models_democrat_multilag_cycle.tex"
# note_content <- "Cross-classified random effects (CCRE) logistic regression model with discrete multiyear lags. That is, each model uses a discrete set of year lags as follows: 1-2 year lags, 1-4 year lags, 1-6 year lags, and 1-8 year lags. Cross-classified random intercepts include firm, year, and lag years. Measure of board-member partisanship: \\textit{party-cycle}, which may vary across election cycles."
# mlabel = "tab:dem_multilag_cycle"




#asr
r = 19
r2 = 23
r3 = 9
d = 3



re1l = "Firm"
re2l = "Year"
re3l = "Lag Year"

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
newline_space <- "\\\\[-1em]"
blankline <- " & & & & \\\\"



# Make Note
note_form <- "\\multicolumn{5}{l}{\\parbox[t]{0.9\\textwidth}{{\\textit{Notes:}}"
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
                     #type = "text",
                     header = FALSE,
                     font.size = "scriptsize",
                     style = "asr",
                     title = ttitle,
                     dep.var.labels   = dvar,
                     label = mlabel,
                     column.labels = c("1-2 \\par Year Lags", "1-4 \\par Year Lags", "1-6 \\par Year Lags", "1-8 \\par Year Lags"),
                     covariate.labels = c("Board Member Added",
                                          "Board Member Equal Swap",
                                          "Republican Board",
                                          "Democratic Firm",
                                          "Republican Firm",
                                          "Constant"),
                      notes.append = TRUE, notes.align = "l"
                     )

tables <- as.data.frame(tables)
tables$tables <- as.character(tables$tables)
tables

#Add Table Note
tables <- insertrow(tables, tnote, r2)

#Add Space to DV Label
tables <- insertrow(tables, newline_space, r3)

#Start Random Effects
tables <- insertrow(tables, blankline, r)
tables <- insertrow(tables,randomeffect,r+1)


#Get number of RE's
num.re1.m1 <- sapply(ranef(m1),nrow)[1]
num.re2.m1 <- sapply(ranef(m1),nrow)[2]
num.re3.m1 <- sapply(ranef(m1),nrow)[3]

num.re1.m2 <- sapply(ranef(m2),nrow)[1]
num.re2.m2 <- sapply(ranef(m2),nrow)[2]
num.re3.m2 <- sapply(ranef(m2),nrow)[3]

num.re1.m3 <- sapply(ranef(m3),nrow)[1]
num.re2.m3 <- sapply(ranef(m3),nrow)[2]
num.re3.m3 <- sapply(ranef(m3),nrow)[3]

num.re1.m4 <- sapply(ranef(m4),nrow)[1]
num.re2.m4 <- sapply(ranef(m4),nrow)[2]
num.re3.m4 <- sapply(ranef(m4),nrow)[3]


#Get Variance
var.re1.m1 <- as.data.frame(VarCorr(m1))$vcov[1]
var.re2.m1 <- as.data.frame(VarCorr(m1))$vcov[2]
var.re3.m1 <- as.data.frame(VarCorr(m1))$vcov[3]

var.re1.m2 <- as.data.frame(VarCorr(m2))$vcov[1]
var.re2.m2 <- as.data.frame(VarCorr(m2))$vcov[2]
var.re3.m2 <- as.data.frame(VarCorr(m2))$vcov[3]

var.re1.m3 <- as.data.frame(VarCorr(m3))$vcov[1]
var.re2.m3 <- as.data.frame(VarCorr(m3))$vcov[2]
var.re3.m3 <- as.data.frame(VarCorr(m3))$vcov[3]

var.re1.m4 <- as.data.frame(VarCorr(m4))$vcov[1]
var.re2.m4 <- as.data.frame(VarCorr(m4))$vcov[2]
var.re3.m4 <- as.data.frame(VarCorr(m4))$vcov[3]


#make RE row entries
num.re1 <- paste0(re1l, "s &", num.re1.m1, "&", num.re1.m2, "&", num.re1.m3, "&", num.re1.m4, "\\\\")
num.re2 <- paste0(re2l, "s &", num.re2.m1, "& ", num.re2.m2, "& ", num.re2.m3, "& ", num.re2.m4, "\\\\")
num.re3 <- paste0(re3l, "s & [1,", num.re3.m1, "] & [1,", num.re3.m2, "] & [1,", num.re3.m3, "] & [1,", num.re3.m4, "] \\\\")


var.re1 <- paste0(re1l, " Variance &", round(var.re1.m1, d), "&", round(var.re1.m2, d), "&", round(var.re1.m3, d), "&", round(var.re1.m4, d), "\\\\")
var.re2 <- paste0(re2l, " Variance &", round(var.re2.m1, d), "&", round(var.re2.m2, d), "&", round(var.re2.m3, d), "&", round(var.re2.m4, d), "\\\\")
var.re3 <- paste0(re3l, " Variance &", round(var.re3.m1, d), "&", round(var.re3.m2, d), "&", round(var.re3.m3, d), "&", round(var.re3.m4, d), "\\\\")

#add rows
#tables <- insertrow(tables,num.re1, r+3)
tables <- insertrow(tables,var.re1, r+2)
tables <- insertrow(tables,var.re2, r+3)
tables <- insertrow(tables,var.re3, r+4)
tables <- insertrow(tables, hline2, r+5)
tables <- insertrow(tables,newline_space, r+6)

tables <- insertrow(tables,num.re1, r+8)
tables <- insertrow(tables,num.re2, r+9)
tables <- insertrow(tables,num.re3, r+10)

write.table(tables,file=outfile,sep="",row.names= FALSE,na="", quote = FALSE, col.names = FALSE)
