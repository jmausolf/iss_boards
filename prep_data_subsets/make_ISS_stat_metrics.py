import pandas as pd 
import numpy as np 
import ast

from collections import Counter 
from collections import ChainMap
from functools import reduce

#################################################################
# Set Options
#################################################################

infile = '../data/ISS/post_join_drop_ISS_select.csv'
outfile = '../data/ISS/ISS_board_change_analysis.csv'
fullname_var = 'fullname_clean_pure'


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


def make_str_bp_col(party_var, df):

    p = party_var
    bp = 'bp_{}'.format(p)
    df[bp] = np.where(df[p] < 0, "DEM",
                np.where(df[p] >= 0, "REP", None))
    return df

#################################################################
#Load Key Dataframes
#################################################################

#Load Data
dm = pd.read_csv(infile, low_memory=False)
print('[*] loading dataframe {} : {}...'.format(infile, dm.shape))

#Drop Duplicates
dm = dm.drop_duplicates(subset=['ticker', 'year', fullname_var])
print(dm.shape)

#################################################################
#Add Some Basic Metrics
#################################################################

#########################
## Board Size Metrics

#Set Aliases
fn = fullname_var
bs = 'board_size'
y = 'year'
by = 'board_years'
gb1 = ['ticker', 'year']
gb2 = ['ticker']

#Add Yearly Board Size Column
tmp1 = dm.groupby(gb1)[fn].count().reset_index()
tmp1.columns = ['ticker', 'year', bs]

#Add Board Size Min, Max, Mean
tmp2 = tmp1.groupby(gb2).agg({bs : ['min', 'mean', 'max']})
tmp2 = pd.DataFrame(tmp2.to_records())
tmp2 = get_clean_cols(tmp2)

#Add Yearly Board Size Column
tmp3 = dm.groupby(gb1)[fn].count().reset_index()
tmp4 = tmp3.groupby(gb2).size().reset_index(name=by)


#Join
tmp = tmp1.merge(tmp2)
tmp = tmp.merge(tmp4)
dm = dm.merge(tmp)

#print(dm.columns.tolist())

#########################
## Make Function for Getting 
#mean, median, min, max, count of a dummy, such as women or interlock

#
#table(dfx$Interlocking)
#table(dfx$female)
'''
in_var = 'female'

in_var = 'ethnicity'
vd = '{}_flag'.format(in_var)

val_list = dm[in_var].value_counts().index.tolist()

for v in val_list:
	#print(clean_col(v))
	out_var = '{}_flag'.format(clean_val(v))
	print(out_var)

	dm[out_var] = np.where(dm[in_var] == v, 1,
					np.where(dm[in_var].notna(), 0, None))

print(dm)
'''

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

print(dm.country_of_empl.value_counts())
print(dm.non_usa.value_counts())


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

#Female Stats


dl = ['female_yes', 'race_eth_asian', 'race_eth_caucasian']
dl1 = ['age', 'outside_public_boards', 'female_yes', 'minority_yes', 'minority_no', 'aa_hisp_yes', 'aa_hisp_no', ]

dl2 = ['age', 'outside_public_boards',
	   'female_yes', 'minority_yes', 'minority_no',
	   'aa_hisp_yes', 'aa_hisp_no', 'non_usa_yes' ]

dl = dl1+dl2
print(dl)

gb1 = ['ticker', 'year']
sl1 = ['sum', 'mean', 'median']


def get_dummy_stats(groupby_list, stat_list, dummy_list, data):

	gb = groupby_list
	df = data

	out_list = []
	for d in dummy_list:
		tmp = df.groupby(gb).agg({d : stat_list})
		tmp = pd.DataFrame(tmp.to_records())
		tmp = get_clean_cols(tmp)
		out_list.append(tmp)

	#tmp = reduce(lambda l,r: pd.merge(l,r,on=gb), out_list)
	#return tmp

	df = df.merge(tmp)
	return df


tmp = get_dummy_stats(gb1, sl1, dl2, data=dm)
print(tmp)
print(tmp.columns.tolist())



#count().reset_index()
#tmp1.columns = ['ticker', 'year', bs]
#tmp2 = dm[['ticker', 'year', 'fullname_clean_pure', 'female']]

#dt = tmp2.merge(tmp1)

#print(dm.columns.tolist())
#print(dm)

#Name: ethnicity_caucasian, dtype: int64
#1    26759
#0     7269






