import pandas as pd 
import numpy as np 

from functools import reduce


#################################################################
# Set Options
#################################################################

iss_file = '../data/ISS/post_join_drop_ISS_select_cycle.csv'
bc_file = '../data/ISS/ISS_board_change_analysis_cycle.csv'
outfile = '../data/ISS/ISS_ANALYSIS_cycle.csv'
fullname_var = 'fullname_clean_pure'


#################################################################
# Utility Functions
#################################################################

def clean_col(col):
    c0 = str(col).replace(", '')", ")")
    c1 = c0.replace('(', '').replace(')', '')
    c2 = c1.replace("'", "").replace(' ', '')
    c3 = c2.replace(',', '_').lower()
    c4 = c3.replace('\n', '').strip()
    return c4

def clean_val(val):
    c0 = str(val).replace(", '')", ")")
    c1 = c0.replace('(', '').replace(')', '')
    c2 = c1.replace("'", "").replace(' ', '')
    c3 = c2.replace('/', '-')
    c4 = c3.replace(',', '_').lower()
    c5 = c4.replace('\n', '').strip()
    return c5


def get_clean_cols(df):
    cols = df.columns
    clean_cols = [clean_col(c) for c in cols]
    df.columns = clean_cols
    return df

def get_dummy_flags(df, in_var, keep_none=True):
	val_list = df[in_var].value_counts().index.tolist()
	for v in val_list:
		out_var = '{}_{}'.format(in_var, clean_val(v))

		if keep_none is True:
			df[out_var] = np.where(df[in_var] == v, 1,
							np.where(df[in_var].notna(), 0, None))
		else:
			df[out_var] = np.where(df[in_var] == v, 1, 0)

	return df

def get_dummy_stats(groupby_list, stat_list, dummy_list, data):

	gb = groupby_list
	df = data

	out_list = []
	for d in dummy_list:
		tmp = df.groupby(gb).agg({d : stat_list})
		tmp = pd.DataFrame(tmp.to_records())
		tmp = get_clean_cols(tmp)
		out_list.append(tmp)

	tmp = reduce(lambda l,r: pd.merge(l,r,on=gb), out_list)
	return tmp

	#df = df.merge(tmp)
	#return df



#################################################################
#Load Key Dataframes
#################################################################

#Load Data
dm = pd.read_csv(iss_file, low_memory=False)
print('[*] loading dataframe {} : {}...'.format(iss_file, dm.shape))

#Drop ISS Duplicates
dm = dm.drop_duplicates(subset=['ticker', 'year', fullname_var])
print(dm.shape)

#Load Cleaned Board Change Data
bc = pd.read_csv(bc_file, low_memory=False)




#################################################################
#Make Additional Recoded Dummy Cols
#################################################################


#Recode Base Race Var
v = 'ethnicity'
dm['race_eth'] = np.where(dm[v] == "CAUCASIAN", "CAUCASIAN",
					np.where(dm[v] == "ASIAN", "ASIAN",
					np.where(dm[v] == "BLACK/AFRICAN AMERICAN", "AFRICAN-AMERICAN",
					np.where(dm[v] == "AFRICAN-AMERICAN", "AFRICAN-AMERICAN",
					np.where(dm[v] == "HISPANIC/LATIN AMERICAN", "HISPANIC",
					np.where(dm[v] == "HISPANIC", "HISPANIC",
					np.where(dm[v] == "INDIAN", "INDIAN",
					np.where(dm[v] == "MIDDLE-EASTERN", "MIDDLE-EASTERN", "OTHER"))))))))

#import pdb; pdb.set_trace()
#Make Minority Variable
v = 'race_eth'
dm['minority'] = np.where(dm[v] == "CAUCASIAN", "NO", "YES")

#Make African-American or Hispanic Var
v = 'race_eth'
dm['aa_hisp'] = np.where(dm[v] == "AFRICAN-AMERICAN", "YES",
					np.where(dm[v] == "HISPANIC", "YES", "NO"))

#Non-US Country of Employment
v = 'country_of_empl'
dm['non_usa'] = np.where(dm[v] == "USA", "NO",
				np.where(dm[v].notna(), "YES", None))

#print(dm.country_of_empl.value_counts())
#print(dm.non_usa.value_counts())



dm = get_dummy_flags(dm, 'female', keep_none=False)
dm = get_dummy_flags(dm, 'race_eth', keep_none=False)
dm = get_dummy_flags(dm, 'minority', keep_none=False)
dm = get_dummy_flags(dm, 'aa_hisp', keep_none=False)
dm = get_dummy_flags(dm, 'interlocking', keep_none=False)
dm = get_dummy_flags(dm, 'non_usa', keep_none=False)

print(dm.columns.tolist())

#################################################################
#Make Summary Metrics
#################################################################

#Get Company Year Summary Metrics
dl = ['age', 'outside_public_boards',
	   'female_yes', 'minority_yes', 'minority_no',
	   'aa_hisp_yes', 'aa_hisp_no', 'non_usa_yes',
	   'interlocking_yes']

gb1 = ['ticker', 'year']
sl1 = ['sum', 'mean', 'median']





tmp = get_dummy_stats(gb1, sl1, dl, data=dm)
tmp_cols = tmp.columns.tolist()
tmp_cols = [c for c in tmp_cols if c not in gb1]

iss = dm.merge(tmp)

#import pdb; pdb.set_trace()


print(iss)
print(iss.columns.tolist())



#################################################################
#Keep Only Company Level Data
#################################################################

#TODO Get Lat/Long Data from DIME? Only available for one ds
#Can give descriptive stats of bm location, demographics, ect

#Board change analysis

#Get Only Company, Year Level Data
#Drop Duplicates
iss = iss.drop_duplicates(subset=['ticker', 'year'])

core_cols = ['company_id', 'ticker', 'ticker_alt',
			'year', 'list_id',
			'privatefirm', 'sector', 'industry',
			'total_dem_sum', 'total_dem_mean',
			'total_dem_median', 'total_dem_min', 'total_dem_max',
			'total_rep_sum', 'total_rep_mean', 'total_rep_median',
			'total_rep_min', 'total_rep_max', 'dime_cfscore_mean',
			'dime_cfscore_median', 'dime_cfscore_min',
			'dime_cfscore_max',
			'fec_cluster_party', 'fec_mean_pid2', 'fec_median_pid2',
			'fec_mean_ps', 'fec_median_ps', 'fec_mean_ps_mode',
			'fec_mean_ps_min', 'fec_mean_ps_max', 'fec_var_pid',
			'fec_skewness_pid', 'fec_kurtosis_pid',
			'fec_polarization_raw_pid', 'fec_polarization_pid',
			'fec_var_ps', 'fec_skewness_ps', 'fec_kurtosis_ps',
			'fec_polarization_raw_ps', 'fec_polarization_ps',
			'fec_pid2_percent_rank',
			'fec_partisan_score_percent_rank']

#import pdb; pdb.set_trace()
keep_cols = core_cols+tmp_cols
iss = iss[keep_cols]

print(iss.shape)
print(iss.isna().sum())

#TODO
#QC, Fill in DIME Metric Data that's missing from prior join
#for some companies with inconsistent tickers, e.g. Google, Berkshire, etc.

#Also see if I can get more complete FEC data summary metrics
#iss.to_csv('test_iss.csv', index=False)

#Join
print(bc.shape)
df = bc.merge(iss, how = 'left', on = ['ticker', 'year'])
print(df.shape)
print(df.isna().sum())

print(df.columns.tolist())


#################################################################
#Make Additional Columns for Analysis
#################################################################

#Provide Dem/Rep Add/Drop Dummy Variables
df = get_dummy_flags(df, 'new_bm_party', keep_none=True)
df = get_dummy_flags(df, 'dropped_bm_party', keep_none=True)

df = get_dummy_flags(df, 'new_bm_pid2ni_med_str', keep_none=True)
df = get_dummy_flags(df, 'dropped_bm_pid2ni_med_str', keep_none=True)

print(df)
#Save 
df.to_csv(outfile, index=False)


