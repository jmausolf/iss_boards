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
fec = fec[['cid_master', 'fullname_fec', 'full_first', 'first_simple', 'middle', 'last']].drop_duplicates()
dm1 = dm1[['ticker', 'last.name', 'first.name']].drop_duplicates()
dm2 = dm2[['ticker', 'contributor.lname', 'contributor.fname']].drop_duplicates()



#Add Party Flags
#iss['party_flag'] = None
fec['party_flag'] = True
dm1['party_flag'] = True
dm2['party_flag'] = True

print(iss.columns)
print(iss.isna().sum())
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

#TODO add other name match efforts
#redo by cycle
#forward, backward impute party

#Simple method first
#join as is, just constant partisanship summary


###############################
#FEC & ISS
###############################

#Method A
df1A = iss.merge(fec, how = "left",
				left_on=['cid_master', 'fullname_clean_pure'],
			  	right_on=['cid_master', 'fullname_fec'])
df1A['merge_match_type'] = '1A'
df1A = df1A.dropna(subset=['party_flag'])
iss_rem = anti_join(iss, df1A, key='iss_row_id')
print("ISS 1A: remaining:", iss_rem.shape, df1A.shape)

#Method B
df1B = iss_rem.merge(fec, how = "left",
				left_on=['cid_master', 'fullname_clean_simple'],
			  	right_on=['cid_master', 'fullname_fec'])
df1B['merge_match_type'] = '1B'
df1B = df1B.dropna(subset=['party_flag'])
iss_rem = anti_join(iss_rem, df1B, key='iss_row_id')
print("ISS 1B: remaining:", iss_rem.shape, df1B.shape)

#Method C
df1C = iss_rem.merge(fec, how = "left",
				left_on=['cid_master', 'fullname_clean_nickname'],
			  	right_on=['cid_master', 'fullname_fec'])
df1C['merge_match_type'] = '1C'
df1C = df1C.dropna(subset=['party_flag'])
iss_rem = anti_join(iss_rem, df1C, key='iss_row_id')
print("ISS 1C: remaining:", iss_rem.shape, df1C.shape)

#Method D
df1D = iss_rem.merge(fec, how = "left",
				left_on=['cid_master', 'fullname_clean'],
			  	right_on=['cid_master', 'fullname_fec'])
df1D['merge_match_type'] = '1D'
df1D = df1D.dropna(subset=['party_flag'])
iss_rem = anti_join(iss_rem, df1D, key='iss_row_id')
print("ISS 1D: remaining:", iss_rem.shape, df1D.shape)


#Method E
df1E = iss_rem.merge(fec, how = "left",
				left_on=['cid_master', 'first_name_clean', 'last_name_clean'],
			  	right_on=['cid_master', 'full_first', 'last'])
df1E['merge_match_type'] = '1E'
df1E = df1E.dropna(subset=['party_flag'])
iss_rem = anti_join(iss_rem, df1E, key='iss_row_id')
print("ISS 1E: remaining:", iss_rem.shape, df1E.shape)


df2A = iss_rem.merge(dm2, how = "left",
				left_on=['ticker', 'last_name_clean', 'first_name_clean'],
			  	right_on=['ticker', 'contributor.lname', 'contributor.fname'])
df2A['merge_match_type'] = '2A'
df2A = df2A.dropna(subset=['party_flag'])
iss_rem = anti_join(iss_rem, df2A, key='iss_row_id')
print("ISS 2A: remaining:", iss_rem.shape, df2A.shape)




df2B = iss_rem.merge(dm2, how = "left",
				left_on=['ticker', 'last_name_clean'],
			  	right_on=['ticker', 'contributor.lname'])
df2B['merge_match_type'] = '2B'
df2B = df2B.dropna(subset=['party_flag'])
iss_rem = anti_join(iss_rem, df2B, key='iss_row_id')
print("ISS 2B: remaining:", iss_rem.shape, df2B.shape)


df3A = iss_rem.merge(dm1, how = "left",
				left_on=['ticker', 'last_name_clean', 'first_name_clean'],
			  	right_on=['ticker', 'last.name', 'first.name'])
df3A['merge_match_type'] = '3A'
df3A = df3A.dropna(subset=['party_flag'])
iss_rem = anti_join(iss_rem, df3A, key='iss_row_id')
print("ISS 3A: remaining:", iss_rem.shape, df3A.shape)


df3B = iss_rem.merge(dm1, how = "left",
				left_on=['ticker', 'last_name_clean'],
			  	right_on=['ticker', 'last.name'])
df3B['merge_match_type'] = '3B'
df3B = df3B.dropna(subset=['party_flag'])
iss_rem = anti_join(iss_rem, df3B, key='iss_row_id')
print("ISS 3B: remaining:", iss_rem.shape, df3B.shape)



##Append the Results and Dedupe
df = pd.concat([df1A, df1B, df1C, df1D, df1E, df2A, df2B, df3A, df3B], 
				axis=0, sort=True).reset_index(drop=True)

#Drop Pure Duplicates
df = df.drop_duplicates(subset='iss_row_id')
print(df.shape)
print(df.columns)

df2 = pd.concat([df, iss_rem], axis=0, sort=True).reset_index(drop=True)
df2 = df2[['company_id', 'ticker', 'cid_master', 'iss_row_id', 'fullname_clean_pure', 'cycle', 'year', 'party_flag', 'merge_match_type']]
df2 = df2.sort_values(by=['iss_row_id'])

df2.to_csv("test_iss_join.csv", index=False)



#print(df)
print(df.isna().sum())
print(df2.isna().sum())


#Get NA By Group
df3 = df2.drop('cid_master', 1).isna().groupby(df.cid_master, sort=False).sum().reset_index()
df3 = df3.sort_values(by='party_flag')
print(df3)
df3.to_csv("test_missing_iss_join.csv", index=False)


#TODO Drop Those With >X% of NA board, >200 companies with no NA


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

