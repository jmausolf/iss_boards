


#Set Options
# models <- list(m1lr, m2lr, m3lr, m4lr)
# ttitle = "Mixed Effects Models of Adding a New Board Member (Republican), Odds Ratios Displayed"
# dvar = "Pr\\{New Board Member: Republican\\}"
# outfile = "output/tables/glmer_models_republican_lag1.tex"


#Set Options
# models <- list(m1lr2, m2lr2, m3lr2, m4lr2)
# ttitle = "Mixed Effects Models of Adding a New Board Member (Republican), Odds Ratios Displayed"
# dvar = "Pr\\{New Board Member: Republican\\}"
# outfile = "output/tables/glmer_models_republican_lag2.tex"


#Set Options
# models <- list(m1ld, m2ld, m3ld, m4ld)
# ttitle = "Mixed Effects Models of Adding a New Board Member (Democrat), Odds Ratios Displayed"
# dvar = "Pr\\{New Board Member: Democrat\\}"
# outfile = "output/tables/glmer_models_democrat_lag1.tex"


#Set Options
# models <- list(m1ld2, m2ld2, m3ld2, m4ld2)
# ttitle = "Mixed Effects Models of Adding a New Board Member (Democrat), Odds Ratios Displayed"
# dvar = "Pr\\{New Board Member: Democrat\\}"
# outfile = "output/tables/glmer_models_democrat_lag2.tex"




#asr
r = 34
d = 3


#outfile = "glmer_tables_test_dem_lag2.tex"

re1l = "Firm"
re2l = "Year"

#Add Insert Row Function
insertrow <- function(existingDF, newrow, r) {
  existingDF[seq(r+1,nrow(existingDF)+1),] <- existingDF[seq(r,nrow(existingDF)),]
  existingDF[r,] <- newrow
  existingDF
}

# Create some standard rows to add.
#randomeffect <- "{\\bf Random Effects} & & & &\\\\"
randomeffect <- "{\\textit{Level-2 Random Intercepts}} & & & &\\\\"
hline <- "\\hline"
hline2 <- "\\hline \\\\[-1.8ex]"
newline <- "\\\\"
blankline <- " & & & & \\\\"



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
                     covariate.labels = c("\\textit{Boards and Firm Politics} \\\\Board Member Swap",
                                          "Republican Board",
                                          "Amphibious Firm",
                                          "Republican Firm",
                                          
                                          "\\\\ \\textit{Board Features} \\\\ Median Age",
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
                                          "Constant")
                     )

tables <- as.data.frame(tables)
tables$tables <- as.character(tables$tables)
tables


#tables <- insertrow(tables, hline2, r)
tables <- insertrow(tables, blankline, r)
tables <- insertrow(tables,randomeffect,r+1)
#tables <- insertrow(tables,hline,r+2)

#Get number of RE's
num.re1.m1 <- sapply(ranef(m1),nrow)[1]
num.re2.m1 <- sapply(ranef(m1),nrow)[2]

num.re1.m2 <- sapply(ranef(m2),nrow)[1]
num.re2.m2 <- sapply(ranef(m2),nrow)[2]

num.re1.m3 <- sapply(ranef(m3),nrow)[1]
num.re2.m3 <- sapply(ranef(m3),nrow)[2]

num.re1.m4 <- sapply(ranef(m4),nrow)[1]
num.re2.m4 <- sapply(ranef(m4),nrow)[2]


#Get Variance
var.re1.m1 <- as.data.frame(VarCorr(m1))$vcov[1]
var.re2.m1 <- as.data.frame(VarCorr(m1))$vcov[2]

var.re1.m2 <- as.data.frame(VarCorr(m2))$vcov[1]
var.re2.m2 <- as.data.frame(VarCorr(m2))$vcov[2]

var.re1.m3 <- as.data.frame(VarCorr(m3))$vcov[1]
var.re2.m3 <- as.data.frame(VarCorr(m3))$vcov[2]

var.re1.m4 <- as.data.frame(VarCorr(m4))$vcov[1]
var.re2.m4 <- as.data.frame(VarCorr(m4))$vcov[2]


#make RE row entries
num.re1 <- paste0(re1l, "s &", num.re1.m1, "&", num.re1.m2, "&", num.re1.m3, "&", num.re1.m4, "\\\\")
var.re1 <- paste0(re1l, " Variance &", round(var.re1.m1, d), "&", round(var.re1.m2, d), "&", round(var.re1.m3, d), "&", round(var.re1.m4, d), "\\\\")

num.re2 <- paste0(re2l, "s &", num.re2.m1, "& ", num.re2.m2, "& ", num.re2.m3, "& ", num.re2.m4, "\\\\")
var.re2 <- paste0(re2l, " Variance &", round(var.re2.m1, d), "&", round(var.re2.m2, d), "&", round(var.re2.m3, d), "&", round(var.re2.m4, d), "\\\\")

#add rows
#tables <- insertrow(tables,num.re1, r+3)
tables <- insertrow(tables,var.re1, r+2)
#tables <- insertrow(tables,newline, r+5)
#tables <- insertrow(tables,num.re2, r+6)
tables <- insertrow(tables,var.re2, r+3)
tables <- insertrow(tables, hline2, r+4)
tables <- insertrow(tables,newline, r+5)
tables <- insertrow(tables,num.re1, r+7)
tables <- insertrow(tables,num.re2, r+8)

write.table(tables,file=outfile,sep="",row.names= FALSE,na="", quote = FALSE, col.names = FALSE)
