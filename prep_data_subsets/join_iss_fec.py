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
dm1 = pd.read_csv("../data/DIME/aoi_data/bod_fortune_500_DIME.csv")
dm2 = pd.read_csv("../data/DIME/aoi_data/bod_fortune_500_DIME_cont_records.csv")

#Simulate Creating Neat Party Metrics By Name for DS
fec = fec[['cid_master', 'fullname']].drop_duplicates()
dm1 = dm1[['ticker', 'last.name', 'first.name']].drop_duplicates()
dm2 = dm2[['ticker', 'contributor.lname', 'contributor.fname']].drop_duplicates()



#Add Party Flags
#iss['party_flag'] = None
fec['party_flag'] = True
dm1['party_flag'] = True
dm2['party_flag'] = True

print(iss.columns)
print(fec.columns)
print(dm1.columns)
print(dm2.columns)



print(dm1.shape)
print(dm2.shape)





print(iss.shape)

#iss = iss[['cid_master','fullname_clean_pure']].drop_duplicates()
#fec = fec[['cid_master', 'fullname']].drop_duplicates()

#iss = iss[['ticker', 'last_name_clean', 'first_name_clean']].drop_duplicates()

#iss = iss[['cid_master','last_name_clean']].drop_duplicates()
#fec = fec[['cid_master', 'last']].drop_duplicates()

#calc dime stats like fec by company, name, cycle, and supplement with iss

#before calc stats and doing that though, just try to join names from the summary file

#print(iss.shape)
#print(fec.shape)

#################################################################
#Joins Using Multiple Methods
#################################################################

#M1 - Fullname Join
#print(iss.columns)
#print(fec.columns)

#fullname, company, cycle
df1A = iss.merge(fec, how = "left",
				left_on=['cid_master', 'fullname_clean_pure'],
			  	right_on=['cid_master', 'fullname'])
df1A['merge_match_type'] = 'fec_fn'
df1A = df1A.dropna(subset=['party_flag'])
iss_rem = anti_join(iss, df1A, key='iss_row_id')
print("ISS 1A: remaining:", iss_rem.shape, df1A.shape)


#df1A = iss.merge(fec, how = "left",
#				left_on=['cid_master', 'fullname_clean_pure'],
#			  	right_on=['cid_master', 'fullname'])

#df1A = iss.merge(dm1, how = "left",
#				left_on=['ticker', 'last_name_clean', 'first_name_clean'],
#			  	right_on=['ticker', 'last.name', 'first.name'])


df2A = iss_rem.merge(dm2, how = "left",
				left_on=['ticker', 'last_name_clean', 'first_name_clean'],
			  	right_on=['ticker', 'contributor.lname', 'contributor.fname'])
df2A['merge_match_type'] = 'dm2_ln_fn'
df2A = df2A.dropna(subset=['party_flag'])
iss_rem = anti_join(iss_rem, df2A, key='iss_row_id')
print("ISS 2A: remaining:", iss_rem.shape, df2A.shape)




df2B = iss_rem.merge(dm2, how = "left",
				left_on=['ticker', 'last_name_clean'],
			  	right_on=['ticker', 'contributor.lname'])
df2B['merge_match_type'] = 'dm2_ln'
df2B = df2B.dropna(subset=['party_flag'])
iss_rem = anti_join(iss_rem, df2B, key='iss_row_id')
print("ISS 2B: remaining:", iss_rem.shape, df2B.shape)


##Append the Results and Dedupe
df = pd.concat([df1A, df2A, df2B], 
				axis=0, sort=True).reset_index(drop=True)

#Drop Pure Duplicates
df = df.drop_duplicates()
print(df)
print(df.isna().sum())

#df1A = iss.merge(fec, how = "left",
#				left_on=['cid_master', 'last_name_clean'],
#			  	right_on=['cid_master', 'last'])


#print(df1A)
#print(df1A.isna().sum())

#df1A.to_csv("testjoin1.csv", index=False)



#test idea
#keep unique set of data by company and fullname each ds
#try to see final name


#
#dm1 4872 NA
#dm2 5027 NA

