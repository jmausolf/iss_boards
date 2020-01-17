import pandas as pd 
import numpy as np 

from collections import Counter 
from collections import ChainMap


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
dm = dm.loc[(dm['cid_master'] == 'Marathon Petroleum') | (dm['cid_master'] == 'Apple' )]


dm = dm[['cid_master', 'ticker', 'year', 'cycle', 'fullname_clean_pure', 'party']]
print(dm)

#Fill NA Party Values with UNK
dm['party'] = dm['party'].fillna("UNK")

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
dm0 = dm.merge(tmp)
print(dm0.shape)
print(dm0.columns)

dm0.to_csv("test_metrics.csv", index=False)

#################################################################
#Need Board Change Flags
#################################################################



#################################################################
#Need Board Partisanship Overall Measures
#################################################################

#***All needs to occur on df prior to bm lag and drop na
#since we are lagging again, needs to be on initial df
dm1 = dm.copy()


#Fullname and Party Columns
fn = 'fullname_clean_pure'
pv = 'party'




#################################################################
#Need Board Party Change Metrics
#################################################################



#Make A Column of Name, Party Dicts
def make_row_dict(row, name_key, party_val):

    k = row[name_key]
    v = row[party_val]

    d = {k: v}

    row['name_party'] = d 

    return row

dm1 = dm1.apply(make_row_dict, name_key = fn, party_val = pv, axis=1)
#print(dm1)



def c_dict(lst):
    d = dict(ChainMap(*lst))
    return d


#Get Yearly Board Member, Party Dict
c = 'name_party'
gb = ['ticker', 'year']
#tmp = df.groupby(gb)[c].apply(list)
tmp = dm1.groupby(gb)[c].apply(list).apply(c_dict)
tmp = tmp.reset_index(name='bp_dict')
#tmp.columns = ['ticker', 'year', 'board_party_dict']

#Get Lagged Board List (By Company)
tmp['prior_bp_dict'] = tmp.groupby(['ticker'])['bp_dict'].shift(1)



#Get Board Party Change Results
tmp = tmp.dropna(subset=['prior_bp_dict'])

#print(tmp)
#print(tmp.columns)


#Add Yearly Board Party and Lagged Dicts
dm1 = dm1.merge(tmp)
dm1 = dm1.drop(['name_party'], axis=1)
print(dm1.shape)
print(dm1.columns)
#tmp = tmp.reset_index(name='board')

#Combine Before Calculating Metrics
df = dm0.merge(dm1)
print(df.shape)
print(df.columns)

df.to_csv("test_metrics.csv", index=False)





