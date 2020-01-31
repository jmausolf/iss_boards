import pandas as pd 
import numpy as np 



#################################################################
# Set Options
#################################################################

iss_file = '../data/ISS/post_join_drop_ISS_select.csv'
bc_file = '../data/ISS/ISS_board_change_analysis.csv'
outfile = '../data/ISS/ISS_ANALYSIS.csv'
fullname_var = 'fullname_clean_pure'


#################################################################
#Load Key Dataframes
#################################################################


#Load Base ISS Data
iss = pd.read_csv(iss_file, low_memory=False)
print('[*] loading dataframe {} : {}...'.format(iss_file, iss.shape))

#Load Cleaned Board Change Data
bc = pd.read_csv(bc_file, low_memory=False)



print(iss.columns.tolist(), iss.shape)

print(bc.columns, bc.shape)


#################################################################
# Utility Functions
#################################################################

def clean_val(val):
    c0 = str(val).replace(", '')", ")")
    c1 = c0.replace('(', '').replace(')', '')
    c2 = c1.replace("'", "").replace(' ', '')
    c3 = c2.replace('/', '-')
    c4 = c3.replace(',', '_').lower()
    c5 = c4.replace('\n', '').strip()
    return c5

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



#################################################################
#Keep Company Level Data
#################################################################

#TODO Get Lat/Long Data from DIME? Only available for one ds
#Can give descriptive stats of bm location, demographics, ect

#Board change analysis

#Get Only Company, Year Level Data
#Drop Duplicates
iss = iss.drop_duplicates(subset=['ticker', 'cycle'])

print(iss.shape)

iss = iss[['company_id', 'ticker', 'ticker_alt',
			'cycle', 'list_id',
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
			'fec_partisan_score_percent_rank']]

print(iss.shape)
print(iss.isna().sum())

#TODO
#QC, Fill in DIME Metric Data that's missing from prior join
#for some companies with inconsistent tickers, e.g. Google, Berkshire, etc.

#Also see if I can get more complete FEC data summary metrics
iss.to_csv('test_iss.csv', index=False)

#Join
print(bc.shape)
df = bc.merge(iss, how = 'left', on = ['ticker', 'cycle'])
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


