import pandas as pd 
import numpy as np 

from name_utils import *



#Load FEC Base Data
fec_base = pd.read_csv("../data/FEC/fec_df_analysis.csv", low_memory=False)


#Keep Relevant Data to Load Faster
fc = fec_base.copy()
keep_cols = ['contributor_name_clean', 'cid_master', 'sub_id_count',
		'contributor_city_clean_mode', 'contributor_state_clean_mode',
		'contributor_zip_code_mode', 
		'contributor_employer_clean_mode',
		'contributor_occupation_clean_mode',
       	'pid3', 'pid2', 'partisan_score', 'cycle', 'occ3']

fc = fc[keep_cols]
fc = fc.loc[fc['cycle'] >= 2008]
print(fc) 


#Reclean and Split FEC Names

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

#TODO need to make summary stats of FEC by cycle, person


#Save Cleaned FEC Names
df.to_csv("../data/FEC/cleaned_names_fec_df_analysis.csv")

