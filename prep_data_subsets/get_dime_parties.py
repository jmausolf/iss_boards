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
    c0 = str(col).replace(", '')", ")")
    c1 = c0.replace('(', '').replace(')', '')
    c2 = c1.replace("'", "").replace(' ', '')
    c3 = c2.replace(',', '_').lower()
    c4 = c3.replace('.', '_').lower()
    c5 = c4.replace('\n', '').strip()
    return c5

"""
#make edited dm2 with party
#################################################################
# Core Data
#################################################################


#Load FEC CMTE Data
fecA = pd.read_csv("../data/FEC/committee_master_pids.csv")

#Drop NA by CMTE NAME
fecA = fecA.dropna(subset=['cmte_nm'])
fecA = fecA[['cmte_nm', 'cycle', 'party_id', 'partisan_score']]

#Load FEC Cand Data and
fecB = pd.read_csv("../data/FEC/schedule_a_cand_pids.csv")
fecB = fecB.dropna(subset=['cand_name'])
fecB = fecB[['cand_name', 'cmte_cycle', 'party_id', 'partisan_score']]

#Load DIME Data
dm2 = pd.read_csv("../data/DIME/aoi_data/bod_fortune_500_DIME_cont_records.csv")

#Make Rec Party Column
rp = 'recipient.party'
dm2['rec_party'] = np.where(dm2[rp] == '100', "DEM",
					np.where(dm2[rp] == '200', "REP",
					np.where(dm2[rp].notna(), "IND/OTH", None)))

dm2['rec_party_bin'] = np.where(dm2[rp] == '100', "DEM",
					np.where(dm2[rp] == '200', "REP", None))



#Make CF Party Column
cf = 'cfscore'
dm2['cf_party'] = np.where(dm2[cf] < 0, "DEM",
					np.where(dm2[cf] >= 0, "REP", None))

print(dm2.cf_party.value_counts())
print(dm2.notna().sum())


#print(dm2[rp].value_counts())
#print(dm2.rec_party.value_counts())
#print(dm2.notna().sum())


#################################################################
#Joins Using Multiple Methods
#################################################################

#Add Using CMTE Name
df1A = 	dm2.merge(fecA, how = "left",
				left_on=['recipient.name', 'cycle'],
			  	right_on=['cmte_nm', 'cycle'])
df1A['merge_match_type'] = '1A'
df1A = df1A.dropna(subset=['party_id'])
dm2_rem = anti_join(dm2, df1A, key='transaction.id')
print("DM2 1A: remaining:", dm2_rem.shape, df1A.shape)


#Add Using Cand Name
df1B = 	dm2.merge(fecB, how = "left",
				left_on=['recipient.name', 'cycle'],
			  	right_on=['cand_name', 'cmte_cycle'])
df1B['merge_match_type'] = '1B'
df1B = df1B.dropna(subset=['party_id'])
dm2_rem = anti_join(dm2_rem, df1B, key='transaction.id')
print("DM2 1B: remaining:", dm2_rem.shape, df1B.shape)


##Append the Results and Dedupe
df = pd.concat([df1A, df1B, dm2_rem], 
				axis=0, sort=True).reset_index(drop=True)
#df['search'] = "STD"

#Drop Pure Duplicates
df = df.drop_duplicates(subset='transaction.id')


#Consolidate Party Columns
df['party'] = np.where(df['party_id'].notna(), df['party_id'],
					np.where(df['rec_party_bin'].notna(), df['rec_party_bin'],
						df['cf_party']))

'''
gb = ['ticker']
tmp = df.groupby(gb).agg({'dime.cfscore': ['mean', 'median', 'min', 'max'],
                          'total.dem': ['sum', 'mean', 'median', 'min', 'max'],
                          'total.rep': ['sum', 'mean', 'median',  'min', 'max']
    
})

df = tmp.reset_index()
'''


print(df.isna().sum())
print(df.columns)
print(df.shape)
print(dm2.shape)


df.to_csv('dm2_party.csv', index=False)
"""


dm2 = pd.read_csv("dm2_party.csv")

print(dm2.party.value_counts())

p = 'party'
dm2['pid2'] = np.where(dm2[p] == "DEM", "DEM",
					np.where(dm2[p] == "REP", "REP",
					np.where(dm2[p].notna(), "IND/OTH", None)))

dm2['pid2n'] = np.where(dm2[p] == "DEM", -1,
					np.where(dm2[p] == "REP", 1,
					np.where(dm2[p].notna(), 0, None)))
dm2['pid2n'] = pd.to_numeric(dm2['pid2n'])


#print(dm2.party_bin_num.value_counts())
#print(dm2.party_bin_num.mean())

#dm2 = dm2.apply(pd.to_numeric)
#dm2 = pd.to_numeric(dm2)



gbi = ['ticker', 'contributor.lname', 'contributor.fname']
dm2['idx'] = dm2.groupby(gbi).ngroup()

gb = ['idx', 'ticker', 'contributor.lname', 'contributor.fname']

#tmp = dm2.groupby(gb).agg({'party': ['mode'] 
#})

print(dm2.dtypes)

#Add PID2 Numeric Mean and Median
tmp1 = dm2.groupby(gb).agg({'pid2n' : ['mean', 'median', 'count']})
df1 = tmp1.reset_index()

#Clean Column Names
cols = df1.columns
clean_cols = [clean_col(c) for c in cols]
df1.columns = clean_cols

print(df1)


#Get Party Value Counts
tmp2 = dm2.groupby(gb).agg({'pid2': ['value_counts']})
print(tmp2)
df2 = tmp2.reset_index()


#df = pd.DataFrame(df.to_records())

#Clean Column Names
cols = df2.columns
clean_cols = [clean_col(c) for c in cols]
df2.columns = clean_cols



#df2 = df2.pivot(index='index', columns='pid2', values='pid2_value_counts')



#gb = ['ticker', 'contributor_lname', 'contributor_fname']
#df2['idx'] = df2.groupby(gb).ngroup()

df2 = df2.pivot(index='idx',
				columns='pid2',
				values='pid2_value_counts').fillna(0).reset_index()

df2.columns = ['idx', 'dem_n', 'ind_oth_n', 'rep_n']

print(df2)
print(df2.columns)



df = df1.merge(df2, how = 'left', on = ['idx'])
print(df)
print(df.columns)

print(df.isna().sum())


df.to_csv("test_dm2_parties.csv", index=False)
