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
    c4 = c3.replace('\n', '').strip()
    return c4



#################################################################
# Core Supplement Data
#################################################################


#Load FEC CMTE Data
fecA = pd.read_csv("../data/FEC/committee_master_pids.csv", low_memory=False)

#Drop NA by CMTE NAME
fecA = fecA.dropna(subset=['cmte_nm'])
fecA = fecA[['cmte_nm', 'cycle', 'party_id', 'partisan_score']]

#Load FEC Cand Data and
fecB = pd.read_csv("../data/FEC/schedule_a_cand_pids.csv", low_memory=False)
fecB = fecB.dropna(subset=['cand_name'])
fecB = fecB[['cand_name', 'cmte_cycle', 'party_id', 'partisan_score']]



#################################################################
# Core DIME Data
#################################################################

#Load DIME Data
dm1 = pd.read_csv("../data/DIME/aoi_data/cleaned_bod_fortune_500_DIME.csv")
dm2 = pd.read_csv("../data/DIME/aoi_data/cleaned_bod_fortune_500_DIME_cont_records.csv")

dm1_out = "../data/DIME/aoi_data/cleaned_bod_fortune_500_DIME_party.csv"
dm2_out = "../data/DIME/aoi_data/cleaned_bod_fortune_500_DIME_cont_records_party.csv"

#################################################################
#Dime 1 Party Cleans and Supplemental Joins
#################################################################

print(dm1.columns)
print(dm1.isna().sum())

#Make CF Party Column
cf = 'dime.cfscore'
dm1['cf_party'] = np.where(dm1[cf] < 0, "DEM",
					np.where(dm1[cf] >= 0, "REP", None))

#Add Pct Dem/Rep Cols
dm1['pct_dem'] = pd.to_numeric(dm1['total.dem'] / dm1['total']).fillna(0)
dm1['pct_rep'] = pd.to_numeric(dm1['total.rep'] / dm1['total']).fillna(0)
dm1['pct_sum'] = pd.to_numeric(dm1['pct_dem'] + dm1['pct_rep'])


d = 'pct_dem'
r = 'pct_rep'
s = 'pct_sum'
dm1['pct_party'] = np.where( ((dm1[s] > 0) & (dm1[d] > dm1[r])), "DEM",
					np.where(((dm1[s] > 0) & (dm1[r] > dm1[d])), "REP", None))

#Add Binary Pct to Dems Col
p = 'pct.to.dems'
dm1['pct_dem_party'] = np.where( dm1[p] >= 0.500, "DEM",
					np.where( dm1[p] < 0.500, "REP", None))



#Consolidate Party Columns
dm1['party'] = np.where(dm1['pct_party'].notna(), dm1['pct_party'],
					np.where(dm1['pct_dem_party'].notna(), dm1['pct_dem_party'],
						dm1['cf_party']))

dm1['party_cycle'] = None

dm1 = dm1[['ticker', 'first.name_clean', 'last.name_clean', 'dime.cfscore', 'cf_party',
       'pct_dem', 'pct_rep', 'pct_sum', 'pct_party', 'pct_dem_party', 'party',
       'party_cycle']]

#Clean Column Names
cols = dm1.columns
clean_cols = [clean_col(c) for c in cols]
dm1.columns = clean_cols

print(dm1)
print(dm1.columns)
print(dm1.isna().sum())

#Save Party File
dm1.to_csv(dm1_out, index=False)



#################################################################
#Dime 2 Party Cleans and Supplemental Joins
#################################################################

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


#Drop Pure Duplicates
df = df.drop_duplicates(subset='transaction.id')


#Consolidate Party Columns
df['party'] = np.where(df['party_id'].notna(), df['party_id'],
					np.where(df['rec_party_bin'].notna(), df['rec_party_bin'],
						df['cf_party']))



p = 'party'
df['pid2'] = np.where(df[p] == "DEM", "DEM",
					np.where(df[p] == "REP", "REP",
					np.where(df[p].notna(), "IND/OTH", None)))

df['pid2n'] = np.where(df[p] == "DEM", -1,
					np.where(df[p] == "REP", 1,
					np.where(df[p].notna(), 0, None)))
df['pid2n'] = pd.to_numeric(df['pid2n'])



#################################################################
#Joins Using Multiple Methods - Combine Party Data
#################################################################


def make_party_metrics(df, gb, pid2_col, pid2_num_col):

	'''
	:: pid2_col == str, binary party col
	:: pid2_num_col == num, binary party col
	'''
	p2 = pid2_col
	p2n = pid2_num_col

	df['idx'] = df.groupby(gb).ngroup()
	gb = ['idx']+gb

	#Add PID2 Numeric Mean and Median
	tmp1 = df.groupby(gb).agg({p2n : ['mean', 'median', 'count']})
	df1 = tmp1.reset_index()

	#Clean Column Names
	cols = df1.columns
	clean_cols = [clean_col(c) for c in cols]
	df1.columns = clean_cols


	#Get Party Value Counts
	tmp2 = df.groupby(gb).agg({p2: ['value_counts']})
	df2 = tmp2.reset_index()


	#Clean Column Names
	cols = df2.columns
	clean_cols = [clean_col(c) for c in cols]
	df2.columns = clean_cols


	#Convert Pivot Table
	piv_col = p2
	piv_val = p2+'_value_counts'

	df2 = df2.pivot(index='idx',
					columns=piv_col,
					values=piv_val).fillna(0).reset_index()

	df2.columns = ['idx', 'dem_n', 'ind_oth_n', 'rep_n']



	#Add Columns
	df = df1.merge(df2, how = 'left', on = ['idx'])

	return df


dm2 = df.copy()



#Get Overall Party Metrics
gbi = ['ticker', 'contributor.lname_clean', 'contributor.fname_clean']
dfA = make_party_metrics(dm2, gbi, pid2_col='pid2', pid2_num_col='pid2n')

p = 'pid2n_mean'
dfA['party'] = np.where(dfA[p] < 0, "DEM",
					np.where(dfA[p] >= 0, "REP", None))

dfA = dfA.drop(['idx'], axis=1)
dfA.columns = ['ticker', 'contributor.lname_clean', 'contributor.fname_clean',
       'pid2n_mean_sum', 'pid2n_median_sum', 'pid2n_count_sum', 'dem_n_sum', 'ind_oth_n_sum',
       'rep_n_sum', 'party']




#Get Yearly Party Metrics
gbi = ['ticker', 'contributor.lname_clean', 'contributor.fname_clean', 'cycle']
dfB = make_party_metrics(dm2, gbi, pid2_col='pid2', pid2_num_col='pid2n')

dfB['party_cycle'] = np.where(dfB[p] < 0, "DEM",
					np.where(dfB[p] >= 0, "REP", None))
dfB = dfB.drop(['idx'], axis=1)


#Combine Datasets
df = dfB.merge(dfA,
	how = 'left',
	on = ['ticker', 'contributor.lname_clean', 'contributor.fname_clean'])
print(df)
print(df.columns)
print(df.isna().sum())

#Save Party File
df.to_csv(dm2_out, index=False)

