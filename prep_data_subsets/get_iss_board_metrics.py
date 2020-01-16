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
#Load Key Dataframes
#################################################################

dm = pd.read_csv('../data/ISS/post_join_drop_ISS_select.csv')
print(dm.columns.tolist())

#Duplicate Tickers? HP?
print(dm.shape)
dm = dm.drop_duplicates(subset=['ticker', 'year', 'fullname_clean_pure'])
print(dm.shape)


#Isolate Subset for Draft
dm = dm.loc[dm['cid_master'] == 'Facebook']


dm = dm[['cid_master', 'ticker', 'year', 'cycle', 'fullname_clean_pure', 'party']]
print(dm)

#Add Yearly Board Size Column
gb = ['ticker', 'year']
tmp = dm.groupby(gb)['fullname_clean_pure'].count().reset_index()
tmp.columns = ['ticker', 'year', 'board_size']
dm = dm.merge(tmp)
print(dm)



x = ['cid_master', 'ticker', 'year', 'cycle', 'fullname_clean_pure', 'party']
def lsort(lst):
    lst.sort()
    return lst


#Get Yearly Board Member List?
c = 'fullname_clean_pure'
tmp = dm.groupby(gb)[c].apply(list).apply(lsort)
tmp = tmp.reset_index(name='board')

#Board Set Constant Between Years?
#tmp['size'] = int(len(tmp['board']))
#print(tmp)

#TODO

#Perhaps Need to Write Functions to Compare Sets, Intersection, Difference

#Lag the GB Set of Board Members One Year as New Row
#Run Function that Compares Two Sets and Spits Out Data


#tmp = tmp['board'].apply(list_sort)

dm = dm.merge(tmp)
print(dm)

dm.to_csv("test_boards.csv")
#print(tmp)



#Need to Groupby ticker, year








