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
# Core FEC Data
#################################################################

#Load DIME Data
fec = pd.read_csv("../data/FEC/clean_fec_df_analysis.csv", low_memory=False)
print(fec.shape)
fec_out = "../data/FEC/clean_fec_df_analysis_party.csv"
fec_cycle_out = "../data/FEC/clean_fec_df_analysis_party_cycle.csv"


#################################################################
#Dime 2 Party Cleans and Supplemental Joins
#################################################################

print(fec.columns)

#Make Partisan Score Party Column
ps = 'partisan_score'
fec['ps_party'] = np.where(fec[ps] < 0, "DEM",
					np.where(fec[ps] >= 0, "REP", None))

#Consolidate Party Columns
fec['party_cycle'] = np.where(fec['pid2'].notna(), fec['pid2'],
					np.where(fec['ps_party'].notna(), fec['ps_party'], 	None))


#Impute Party Metrics, Keep Copy Original
#Phase 1: FFILL, Phase 2: BFILL
fec['party_cycle_org'] = fec['party_cycle']
gb = ['cid_master', 'fullname_fec',
	   'full_first', 'first_simple', 'last']
fec['party_cycle'] = fec.groupby(gb)['party_cycle'].ffill()
fec['party_cycle'] = fec.groupby(gb)['party_cycle'].bfill()

#Make Columns to Calculate Overall Party
p = 'party_cycle'
fec['pc2'] = np.where(fec[p] == "DEM", "DEM",
					np.where(fec[p] == "REP", "REP", None))

fec['pc2n'] = np.where(fec[p] == "DEM", -1,
					np.where(fec[p] == "REP", 1, None))
fec['pc2n'] = pd.to_numeric(fec['pc2n'])



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

	df2.columns = ['idx', 'dem_n', 'rep_n']



	#Add Columns
	df = df1.merge(df2, how = 'left', on = ['idx'])

	return df


#Get Overall Party Metrics
gbi = ['cid_master', 'fullname_fec',
	   'full_first', 'first_simple', 'last']
dfA = make_party_metrics(fec, gbi, pid2_col='pc2', pid2_num_col='pc2n')
print(dfA)


p = 'pc2n_mean'
dfA['party'] = np.where(dfA[p] < 0, "DEM",
					np.where(dfA[p] >= 0, "REP", None))

dfA = dfA.drop(['idx'], axis=1)


#Combine with Yearly Party Metrics (FEC Data)
#inner join because some small missingness on first, last names
df = fec.merge(dfA, how = 'inner',
					on = ['cid_master', 'fullname_fec',
					'full_first', 'first_simple', 'last'])

#Add FEC Key
#df['fec_row_id'] = df.index.astype(str)
#df['fec_rid'] = 'fec_' + df['fec_row_id']


print(df)
print(df.shape)
print(df.columns)
print(df.isna().sum())

#Save Non-Cycle Party File
df.to_csv(fec_out, index=False)

#import pdb; pdb.set_trace()
#Artificial Expansion for Cycle Merge

#Get Unique Combination of Names by Firm
dfu = df[['cid_master', 'fullname_fec', 'full_first', 'first_simple', 'last', 'party']].drop_duplicates()

print(dfu)
print(dfu.isna().sum())

#Add Artificial Cycles for ISS Range
iss = pd.read_csv("../data/ISS/cleaned_iss_data.csv", low_memory=False)
iss = iss[['cid_master', 'cycle']].drop_duplicates()

print(iss)
print(iss.isna().sum())


#Join ISS and FEC by Firm and Cycle
dfi = iss.merge(dfu, how='inner', on='cid_master')
dfi = dfi.dropna()

print(dfi)
print(dfi.isna().sum())

#Make a Subset of Cleaned FEC Party Data
dfs = df[['cid_master', 'cycle', 'fullname_fec', 'full_first', 'first_simple', 'last', 'party', 'party_cycle']]

#Full Outside Join Between Datasets
#Captures all years actually in FEC with all years in the ISS for imputing
dfo = dfi.merge(dfs, how = 'outer', on=['cid_master', 'cycle', 'fullname_fec', 'full_first', 'first_simple', 'last', 'party'])
dfo = dfo.sort_values(by=['cid_master', 'fullname_fec', 'cycle'])

print(dfo)
print(dfo.isna().sum())


#Re-Impute Party Metrics, Keep Copy Original
#Phase 1: FFILL, Phase 2: BFILL
dfo['party_cycle_org'] = dfo['party_cycle']
gb = ['cid_master', 'fullname_fec', 'full_first', 'first_simple', 'last']
dfo['party_cycle'] = dfo.groupby(gb)['party_cycle'].ffill()
dfo['party_cycle'] = dfo.groupby(gb)['party_cycle'].bfill()

print(dfo)
print(dfo.isna().sum())

#Save Party File
dfo.to_csv(fec_cycle_out, index=False)
