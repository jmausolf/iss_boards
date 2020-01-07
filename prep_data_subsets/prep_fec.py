import pandas as pd 
import numpy as np 

from name_utils import *



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

#keep_cols = ['contributor_name_clean', 'cycle']
fc = fc[keep_cols]
fc = fc.loc[fc['cycle'] >= 2008]
print(fc) 

'''
df = fc.sample(10000)
df.to_csv("../data/FEC/test_fec.csv", index=False)


df = pd.read_csv("../data/FEC/test_fec.csv")
print(df.shape)
'''

#TODO
#ISS year needs a cycle column
#a board member's metrics for 
#	2007 == cycle 2008
# 	2008 == cycle 2008
#	2009 == cycle 2010
# 	2010 == cycle 2010 ...


#TODO
#reverse correct some errors in "clean" names
#which have errors in concatting 'jr', 'sr', 'ii', 'iii', 'iiii', 'iv' as
#part of last name in 'contributor_name_clean'


def reclean_fec_name_col(name_col, df):

	#Extract Fullname (w/o Suffixes)
	df = extract_fullname(name_col, df)

	#Get First (Full), First Simple, Middle, Last
	df = split_first_last("fullname", df)

	#Make Suffixes Columnn
	df = extract_suffixes(name_col, df)
	
	return df


df = reclean_fec_name_col("contributor_name_clean", fc)
print(df)
print(df.columns)	


#Save Cleaned FEC Names
df.to_csv("../data/FEC/cleaned_names_fec_df_analysis.csv")
#make fullname, first, last, suffix, middle cols
#iss needs same treatment

#TODO join by company, name, cycle