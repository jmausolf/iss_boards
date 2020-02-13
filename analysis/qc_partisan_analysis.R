####################################
## Load SOURCE
####################################

source("analysis_source.R")



# fec <- read_csv("../data/FEC/clean_fec_df_analysis_party.csv") %>% 
#   select('cid_master', 'fullname_fec', 'cycle', 'party', 'party_cycle') 
# 
# dm2 <- read_csv("../data/DIME/aoi_data/cleaned_bod_fortune_500_DIME_cont_records_party.csv")  %>% 
#   select('ticker', 'cycle', 'contributor.lname_clean', 'contributor.fname_clean', 'party', 'party_cycle') 
# 
# 
# 
# df <- read_csv("../prep_data_subsets/test_qc_partisans.csv")
# table(df$source, df$consistent_partisan)
# 




#What about merge_match_types
df1 = read_csv('../data/ISS/post_join_drop_ISS_select.csv')
df2 = read_csv('../data/ISS/post_join_drop_ISS_select_cycle.csv')


#Tables 
table(df1$merge_match_type)
table(df2$merge_match_type)
table(df1$merge_match_type, df2$merge_match_type)



#Load Base Merge Match Type DF
mmt1 <- read_csv("merge_match_types.csv")
mmt2 <- read_csv("merge_match_types_cycle.csv")


#Make DF Join (Party)
dfj1 <- as.data.frame(table(df1$merge_match_type)) %>% 
  rename('Merge_Code' = 'Var1')

dfj2 <- as.data.frame(table(df2$merge_match_type)) %>% 
  rename('Merge_Code' = 'Var1')


#Merge Data DF1 (Party)
mmt_out1 <- left_join(mmt1, dfj1)
mmt_out1[is.na(mmt_out1)] <- 0
mmt_out1 <- mmt_out1 %>% 
  select('Merge Type', 'Partisan Data', 'Left Columns', 'Right Columns', 'Freq') %>% 
  rename('Count' = 'Freq') 
caption = "Summary of Found Partisans by Merge Match Type, Party"
file_path = "output/tables/mmt_party.tex"

save_stargazer(file_path,
               as.data.frame(mmt_out1), header=FALSE, type='latex',
               font.size = "scriptsize",
               title = caption,
               summary = FALSE,
               rownames = FALSE)

#Merge Data DF2 (Party Cycle)
mmt_out2 <- left_join(mmt2, dfj2)
mmt_out2[is.na(mmt_out2)] <- 0
mmt_out2 <- mmt_out2 %>% 
  select('Merge Type', 'Partisan Data', 'Left Columns', 'Right Columns', 'Freq') %>% 
  rename('Count' = 'Freq') 
caption = "Summary of Found Partisans by Merge Match Type, Party Cycle"
file_path = "output/tables/mmt_party_cycle.tex"

save_stargazer(file_path,
               as.data.frame(mmt_out2), header=FALSE, type='latex',
               font.size = "scriptsize",
               title = caption,
               summary = FALSE,
               rownames = FALSE)

#Prep Out Table



