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
					np.where(fec['ps_party'].notna(), fec['ps_party'],
						None))

p = 'party_cycle'
fec['pc2'] = np.where(fec[p] == "DEM", "DEM",
					np.where(fec[p] == "REP", "REP",
					np.where(fec[p].notna(), "IND/OTH", None)))

fec['pc2n'] = np.where(fec[p] == "DEM", -1,
					np.where(fec[p] == "REP", 1,
					np.where(fec[p].notna(), 0, None)))
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
df = fec.merge(dfA,
	how = 'left',
	on = ['cid_master', 'fullname_fec',
	   'full_first', 'first_simple', 'last'])
print(df.shape)
print(df.columns)
print(df.isna().sum())

#Save Party File
df.to_csv(fec_out, index=False)

