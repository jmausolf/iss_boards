import pandas as pd 
import numpy as np 


#################################################################
# Utility Functions
#################################################################

def anti_join(df_A, df_B, key):

	set_diff = set(df_A[key]).difference(df_B[key])
	bool_diff = df_A[key].isin(set_diff)
	df_diff = df_A.loc[bool_diff]

	return df_diff


def clean_col(col):
    c1 = str(col).replace('(', '').replace(')', '')
    c2 = c1.replace("'", "").replace(' ', '')
    c3 = c2.replace(',', '_').lower()
    c4 = c3.replace('\n', '').strip()
    return c4


#################################################################
#Load Key Dataframes
#################################################################

iss = pd.read_csv("../data/ISS/cleaned_iss_data.csv", low_memory=False)
fec = pd.read_csv("../data/FEC/clean_fec_df_analysis.csv", low_memory=False)



#################################################################
#Joins Using Multiple Methods
#################################################################

#M1 - Fullname Join
print(iss.columns)
print(fec.columns)

#fullname, company, cycle
#df1A = iss.merge(fec, how = "left",
#				left_on=['cid_master', 'cycle', 'fullname_clean_pure'],
#			  	right_on=['cid_master', 'cycle', 'fullname'])

df1A = iss.merge(fec, how = "left",
				left_on=['cid_master', 'cycle'],
			  	right_on=['cid_master', 'cycle'])


print(df1A)
print(df1A.isna().sum())



