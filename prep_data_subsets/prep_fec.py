import pandas as pd 
import numpy as np 



#Load FEC Base Data
fec_base = pd.read_csv("../data/FEC/fec_df_analysis.csv", low_memory=False)
print(fec_base.shape)

print(fec_base.columns)


#Keep Relevant Data to Load Faster
#e.g. keep only relevant years and cols

fc = fec_base.copy()
keep_cols = ['contributor_name_clean', 'cid_master', 'contributor_cycle',
       'sub_id_count', 'contributor_city_clean_mode',
       'contributor_state_clean_mode',
       'contributor_employer_clean_mode', 'contributor_occupation_clean_mode',
       'pid3', 'pid2', 'partisan_score', 'occ', 'cycle', 'occ3']
fc = fc[keep_cols]
fc = fc.loc[fc['cycle'] >= 2008]
print(fc) 


#ISS year needs a cycle column
#a board member's metrics for 
#	2007 == cycle 2008
# 	2008 == cycle 2008
#	2009 == cycle 2010
# 	2010 == cycle 2010 ...


#TODO
#reverse correct "clean" names
#which have errors in concatting 'jr', 'sr', 'ii', 'iii', 'iiii', 'iv' as
#part of last name in 'contributor_name_clean'

#make fullname, first, last, suffix, middle cols
#iss needs same treatment

#TODO join by company, name, cycle