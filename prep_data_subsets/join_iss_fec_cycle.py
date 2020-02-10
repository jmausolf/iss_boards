import pandas as pd 
import numpy as np 

#import alt_join_iss_fec
#from alt_join_iss_fec import *

from name_utils import *

#################################################################
# Set Board Completeness Threshold
#################################################################

p_keep = 0.30

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


fec = pd.read_csv("../data/FEC/clean_fec_df_analysis_party_cycle.csv", low_memory=False)
dm1 = pd.read_csv("../data/DIME/aoi_data/cleaned_bod_fortune_500_DIME_party.csv")
dm2 = pd.read_csv("../data/DIME/aoi_data/cleaned_bod_fortune_500_DIME_cont_records_party_cycle.csv")

#Simulate Creating Neat Party Metrics By Name for DS
fec = fec[['cid_master', 'cycle', 'fullname_fec', 'full_first', 'first_simple', 'last', 'party', 'party_cycle']].drop_duplicates()
dm1 = dm1[['ticker', 'last.name_clean', 'first.name_clean', 'party', 'party_cycle']].drop_duplicates()
dm2 = dm2[['ticker', 'cycle', 'contributor.lname_clean', 'contributor.fname_clean', 'party', 'party_cycle']].drop_duplicates()

#Drop Any NA
fec = fec.dropna(subset=['cid_master', 'cycle', 'fullname_fec', 'full_first', 'first_simple', 'last'])
dm1 = dm1.dropna(subset=['ticker', 'last.name_clean', 'first.name_clean'])
dm2 = dm2.dropna(subset=['ticker', 'cycle', 'contributor.lname_clean', 'contributor.fname_clean'])

#Add Party Flags
#iss['party_flag'] = None
fec['party_flag'] = True
dm1['party_flag'] = True
dm2['party_flag'] = True


#################################################################
#Make Alt Join Company Cols and Join with ISSN
#################################################################

dfa = iss[['name', 'ticker', 'cid_master']].copy()
dfb = iss[['primary_employer']].copy()

#Make Cleaned Columns
dfa['clean_name'] = dfa['name']
dfa = rm_punct_col('clean_name', dfa)

dfb['clean_primary_employer'] = dfb['primary_employer']
dfb = rm_punct_col('clean_primary_employer', dfb)


df_alt = dfb.merge(dfa,
					how = 'inner',
					left_on = ['clean_primary_employer'],
					right_on = ['clean_name'] )
df_alt = df_alt.drop_duplicates(subset='primary_employer')
df_alt = df_alt[['primary_employer', 'clean_primary_employer', 'clean_name', 'ticker',
       'cid_master']]

df_alt.columns = ['primary_employer', 'clean_primary_employer',
				  'alt_name', 'alt_ticker', 'alt_cid_master']




#################################################################
#Join Alt Companies Cols with ISS
#################################################################	  

issn = iss.merge(df_alt, how = 'left', on = 'primary_employer')


#################################################################
#Joins Using Multiple Methods
#################################################################

###############################
#FEC & ISS
###############################

#Method A
df1A = issn.merge(fec, how = "inner",
				left_on=['cid_master', 'fullname_clean_pure', 'cycle'],
			  	right_on=['cid_master', 'fullname_fec', 'cycle'])
df1A['merge_match_type'] = '1A'
iss_rem = anti_join(issn, df1A, key='rid')
print("ISS 1A: remaining:", iss_rem.shape, df1A.shape)

#Method B
df1B = iss_rem.merge(fec, how = "inner",
				left_on=['cid_master', 'fullname_clean_simple', 'cycle'],
			  	right_on=['cid_master', 'fullname_fec', 'cycle'])
df1B['merge_match_type'] = '1B'
iss_rem = anti_join(iss_rem, df1B, key='rid')
print("ISS 1B: remaining:", iss_rem.shape, df1B.shape)

#Method C
df1C = iss_rem.merge(fec, how = "inner",
				left_on=['cid_master', 'fullname_clean_nickname', 'cycle'],
			  	right_on=['cid_master', 'fullname_fec', 'cycle'])
df1C['merge_match_type'] = '1C'
iss_rem = anti_join(iss_rem, df1C, key='rid')
print("ISS 1C: remaining:", iss_rem.shape, df1C.shape)

#Method D
df1D = iss_rem.merge(fec, how = "inner",
				left_on=['cid_master', 'fullname_clean', 'cycle'],
			  	right_on=['cid_master', 'fullname_fec', 'cycle'])
df1D['merge_match_type'] = '1D'
iss_rem = anti_join(iss_rem, df1D, key='rid')
print("ISS 1D: remaining:", iss_rem.shape, df1D.shape)


#Method E
df1E = iss_rem.merge(fec, how = "inner",
				left_on=['cid_master', 'first_name_clean', 'last_name_clean', 'cycle'],
			  	right_on=['cid_master', 'full_first', 'last', 'cycle'])
df1E['merge_match_type'] = '1E'
iss_rem = anti_join(iss_rem, df1E, key='rid')
print("ISS 1E: remaining:", iss_rem.shape, df1E.shape)



###############################
#DIME 2 and ISS
###############################

df2A = iss_rem.merge(dm2, how = "inner",
				left_on=['ticker', 'last_name_clean', 'first_name_clean', 'cycle'],
			  	right_on=['ticker', 'contributor.lname_clean', 'contributor.fname_clean', 'cycle'])
df2A['merge_match_type'] = '2A'
iss_rem = anti_join(iss_rem, df2A, key='rid')
print("ISS 2A: remaining:", iss_rem.shape, df2A.shape)




df2B = iss_rem.merge(dm2, how = "inner",
				left_on=['ticker', 'last_name_clean', 'cycle'],
			  	right_on=['ticker', 'contributor.lname_clean', 'cycle'])
df2B['merge_match_type'] = '2B'
iss_rem = anti_join(iss_rem, df2B, key='rid')
print("ISS 2B: remaining:", iss_rem.shape, df2B.shape)



###############################
#DIME 1 and ISS
###############################

df3A = iss_rem.merge(dm1, how = "inner",
				left_on=['ticker', 'last_name_clean', 'first_name_clean'],
			  	right_on=['ticker', 'last.name_clean', 'first.name_clean'])
df3A['merge_match_type'] = '3A'
iss_rem = anti_join(iss_rem, df3A, key='rid')
print("ISS 3A: remaining:", iss_rem.shape, df3A.shape)


df3B = iss_rem.merge(dm1, how = "inner",
				left_on=['ticker', 'last_name_clean'],
			  	right_on=['ticker', 'last.name_clean'])
df3B['merge_match_type'] = '3B'
iss_rem = anti_join(iss_rem, df3B, key='rid')
print("ISS 3B: remaining:", iss_rem.shape, df3B.shape)





#################################################################
#(ALT) Joins Using Multiple Methods
#################################################################

###############################
#FEC & ISS
###############################

#Method A
df1A_a = iss_rem.merge(fec, how = "inner",
				left_on=['alt_cid_master', 'fullname_clean_pure', 'cycle'],
			  	right_on=['cid_master', 'fullname_fec', 'cycle'])
df1A_a['merge_match_type'] = '1A_alt'
iss_rem = anti_join(iss_rem, df1A_a, key='rid')
print("ISS 1A_alt: remaining:", iss_rem.shape, df1A_a.shape)

#Method B
df1B_a = iss_rem.merge(fec, how = "inner",
				left_on=['alt_cid_master', 'fullname_clean_simple', 'cycle'],
			  	right_on=['cid_master', 'fullname_fec', 'cycle'])
df1B_a['merge_match_type'] = '1B_alt'
iss_rem = anti_join(iss_rem, df1B_a, key='rid')
print("ISS 1B_alt: remaining:", iss_rem.shape, df1B_a.shape)

#Method C
df1C_a = iss_rem.merge(fec, how = "inner",
				left_on=['alt_cid_master', 'fullname_clean_nickname', 'cycle'],
			  	right_on=['cid_master', 'fullname_fec', 'cycle'])
df1C_a['merge_match_type'] = '1C_alt'
iss_rem = anti_join(iss_rem, df1C_a, key='rid')
print("ISS 1C_alt: remaining:", iss_rem.shape, df1C_a.shape)

#Method D
df1D_a = iss_rem.merge(fec, how = "inner",
				left_on=['alt_cid_master', 'fullname_clean', 'cycle'],
			  	right_on=['cid_master', 'fullname_fec', 'cycle'])
df1D_a['merge_match_type'] = '1D_alt'
iss_rem = anti_join(iss_rem, df1D_a, key='rid')
print("ISS 1D_alt: remaining:", iss_rem.shape, df1D_a.shape)


#Method E
df1E_a = iss_rem.merge(fec, how = "inner",
				left_on=['alt_cid_master', 'first_name_clean', 'last_name_clean', 'cycle'],
			  	right_on=['cid_master', 'full_first', 'last', 'cycle'])
df1E_a['merge_match_type'] = '1E_alt'
iss_rem = anti_join(iss_rem, df1E_a, key='rid')
print("ISS 1E_alt: remaining:", iss_rem.shape, df1E_a.shape)



###############################
#DIME 2 and ISS
###############################

df2A_a = iss_rem.merge(dm2, how = "inner",
				left_on=['alt_ticker', 'last_name_clean', 'first_name_clean', 'cycle'],
			  	right_on=['ticker', 'contributor.lname_clean', 'contributor.fname_clean', 'cycle'])
df2A_a['merge_match_type'] = '2A_alt'
iss_rem = anti_join(iss_rem, df2A_a, key='rid')
print("ISS 2A_alt: remaining:", iss_rem.shape, df2A_a.shape)




df2B_a = iss_rem.merge(dm2, how = "inner",
				left_on=['alt_ticker', 'last_name_clean', 'cycle'],
			  	right_on=['ticker', 'contributor.lname_clean', 'cycle'])
df2B_a['merge_match_type'] = '2B_alt'
iss_rem = anti_join(iss_rem, df2B_a, key='rid')
print("ISS 2B_alt: remaining:", iss_rem.shape, df2B_a.shape)



###############################
#DIME 1 and ISS
###############################

df3A_a = iss_rem.merge(dm1, how = "inner",
				left_on=['alt_ticker', 'last_name_clean', 'first_name_clean'],
			  	right_on=['ticker', 'last.name_clean', 'first.name_clean'])
df3A_a['merge_match_type'] = '3A_alt'
iss_rem = anti_join(iss_rem, df3A_a, key='rid')
print("ISS 3A_alt: remaining:", iss_rem.shape, df3A_a.shape)


df3B_a = iss_rem.merge(dm1, how = "inner",
				left_on=['alt_ticker', 'last_name_clean'],
			  	right_on=['ticker', 'last.name_clean'])
df3B_a['merge_match_type'] = '3B_alt'
iss_rem = anti_join(iss_rem, df3B_a, key='rid')
print("ISS 3B_alt: remaining:", iss_rem.shape, df3B_a.shape)



#################################################################
#(ALT) - General Search (Only DIME Boards)
#################################################################


###############################
#Alt General
###############################

df2A_g = iss_rem.merge(dm2, how = "inner",
				left_on=['last_name_clean', 'first_name_clean'],
			  	right_on=['contributor.lname_clean', 'contributor.fname_clean'])
df2A_g['merge_match_type'] = '2A_g'
iss_rem = anti_join(iss_rem, df2A_g, key='rid')
print("ISS 2A_g: remaining:", iss_rem.shape, df2A_g.shape)


###############################
#DIME 1 and ISS
###############################

df3A_g = iss_rem.merge(dm1, how = "inner",
				left_on=['last_name_clean', 'first_name_clean'],
			  	right_on=['last.name_clean', 'first.name_clean'])
df3A_g['merge_match_type'] = '3A_g'
iss_rem = anti_join(iss_rem, df3A_g, key='rid')
print("ISS 3A_g: remaining:", iss_rem.shape, df3A_g.shape)


##Append the Results and Dedupe
df = pd.concat([df1A, df1B, df1C, df1D, df1E, df2A, df2B, df3A, df3B,
				df1A_a, df1B_a, df1C_a, df1D_a, df1E_a,
				df2A_a, df2B_a, df3A_a, df3B_a,
				df2A_g, df3A_g], 
				axis=0, sort=True).reset_index(drop=True)


#Drop Pure Duplicates
df = df.drop_duplicates(subset='rid')
#print(df.columns)

#Keep Only ISS ID, Merge Variables
df = df[['rid',
		 'party_flag', 'party', 'party_cycle', 'merge_match_type',
		 'alt_name', 'alt_ticker', 'alt_cid_master']]

#Rejoin With Master ISS
issf = pd.read_csv("../data/ISS/cleaned_iss_data.csv", low_memory=False)
issf = issf.merge(df, how = 'left', on = ['rid'])
#print(issf.columns.tolist(), '\n', issf.shape)

#################################################################
#Drop Companies w/ High Board NAN 
#################################################################

#Keep Rel. Columns
dfd = issf[['cid_master', 'rid', 'fullname_clean_pure', 'party_flag']]

#NA Sum
dfd1 = dfd.drop('cid_master', 1).isna().groupby(dfd.cid_master, sort=False).sum().reset_index()
dfd1 = dfd1[['cid_master', 'party_flag']]
dfd1.columns = ['cid_master', 'n_missing']


#Overall Sum
dfd2 = dfd.groupby(['cid_master']).count().reset_index()
dfd2 = dfd2[['cid_master', 'rid']]
dfd2.columns = ['cid_master', 'n_iss']

#Get Prop Missing
dfd = dfd2.merge(dfd1)
dfd['p_missing'] = dfd['n_missing'] / dfd['n_iss']

#Drop Criteria
dfd['drop_cid'] = np.where(dfd['p_missing'] <= p_keep, "KEEP", "DROP")
dfd = dfd.sort_values(by='p_missing').reset_index(drop=True)
dfd.to_csv('test_missing_iss_join2.csv', index=False)

#Implement Keep Criteria
dfd = dfd.loc[dfd['drop_cid'] == 'KEEP']
c = dfd.shape[0]


#Merge with ISSF (Inner Join)
dfi = issf.merge(dfd, how = 'inner', on = 'cid_master')
print(dfi.columns.tolist(), '\n', dfi.shape)
bnm = dfi.party_flag.notna().sum()
bm = dfi.party_flag.isna().sum()
pnm = dfi.party.notna().sum()
pm = dfi.party.isna().sum()


pcnm = dfi.party_cycle.notna().sum()
pcm = dfi.party_cycle.isna().sum()

print('[*] board missingness threshold: {}'.format(p_keep))
print('[*] resulting companies at threshold: {}'.format(c))
print('[*] found board member observations: {}'.format(bnm))
print('[*] missing board member observations: {}'.format(bm))
print('[*] board members with party: {}'.format(pnm))
print('[*] board members without party: {}'.format(pm))


print('[*] board members with party cycle: {}'.format(pcnm))
print('[*] board members without party cycle: {}'.format(pcm))

#TODO, think about joins by cycle and imputing

#Implications, Might Not Have Particanship for New Boardmembers
#print(dfi.isna().sum())

#Save Results
dfi.to_csv('../data/ISS/post_join_drop_ISS_select_cycle.csv', index=False)
issf.to_csv('../data/ISS/post_join_drop_ISS_all_cycle.csv', index=False)



