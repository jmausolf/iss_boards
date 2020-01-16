import pandas as pd 
import numpy as np 

from collections import Counter 


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


def get_board_metrics(row):
    #bc = ['new_bm', 'new_bm_count',
    #  'dropped_bm', 'dropped_bm_count',
    # 'constant_bm', 'constant_bm_count', 'dupes_bm']

    list_ds2 = row['board']
    list_ds1 = row['prior_board']

    #Get Current List Max
    #Should Not Be > 1
    m = Counter(list_ds2).most_common(1)[0][1]

    if m > 1:
        dupe_qc = True
    else:
        dupe_qc = False
    row['dupes_bm'] = dupe_qc

    #New/Added Elements
    new_items = list((Counter(list_ds2) - Counter(list_ds1)).elements())
    new_items.sort()
    row['new_bm'] = new_items

    ni_n = len(new_items)
    row['new_bm_count'] = ni_n

    #Old/Dropped Elements
    old_items = list((Counter(list_ds1) - Counter(list_ds2)).elements())
    old_items.sort()
    row['dropped_bm'] = old_items

    oi_n = len(old_items)
    row['dropped_bm_count'] = oi_n

    #Intersection/Persistent Elements
    s1 = set(list_ds1)
    s2 = set(list_ds2)

    intersection = list(s1.intersection(s2))
    intersection.sort()
    row['constant_bm'] = intersection

    i_n = len(intersection)
    row['constant_bm_count'] = i_n

    return row





#################################################################
#Load Key Dataframes
#################################################################

dm = pd.read_csv('../data/ISS/post_join_drop_ISS_select.csv')
print(dm.columns.tolist())

#Duplicate Tickers? HP?
print(dm.shape)
dm = dm.drop_duplicates(subset=['ticker', 'year', 'fullname_clean_pure'])
print(dm.shape)


#Isolate Subset for Draft
dm = dm.loc[(dm['cid_master'] == 'Facebook') | (dm['cid_master'] == 'Apple' )]


dm = dm[['cid_master', 'ticker', 'year', 'cycle', 'fullname_clean_pure', 'party']]
print(dm)

#################################################################
#Add Some Basic Metrics
#################################################################

#Add Yearly Board Size Column
gb = ['ticker', 'year']
tmp = dm.groupby(gb)['fullname_clean_pure'].count().reset_index()
tmp.columns = ['ticker', 'year', 'board_size']
dm = dm.merge(tmp)
print(dm)


def lsort(lst):
    lst.sort()
    return lst


#################################################################
#Get Board Member Change Metrics
#################################################################

#Get Yearly Board Member List
c = 'fullname_clean_pure'
tmp = dm.groupby(gb)[c].apply(list).apply(lsort)
tmp = tmp.reset_index(name='board')

#Get Lagged Board List (By Company)
tmp['prior_board'] = tmp.groupby(['ticker'])['board'].shift(1)


#Get Board Change Results
tmp = tmp.dropna(subset=['prior_board'])
tmp =  tmp.apply(get_board_metrics, axis=1)

#Add Yearly Board Member Change Metrics
dm = dm.merge(tmp)
print(dm)






