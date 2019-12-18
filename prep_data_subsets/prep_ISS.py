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



#Load ISS Base Data
iss_base = pd.read_csv("../data/ISS/ISS_Boards.csv", low_memory=False)
iss_base['iss_row_id'] = iss_base.index.astype(str)

#print(iss_base)


#print(iss_base.columns)
print(iss_base.shape)
#print(iss_base.notna().sum())

#Load F400 Data (FEC Subset)
f400 = pd.read_csv("../data/F400/f400_linked_unique.csv")


#Isolate Sub-DF's w/o NA Join Col
c0 = 'ticker'
#f0A = f400.loc[f400[c0].notna()].drop_duplicates(subset=[c0])
f0A = f400.loc[f400[c0].notna()]
f0A = f400
i0A = iss_base.loc[iss_base[c0].notna()]

#f0A = f400
#i0A = iss_base

print(i0A.shape)

#Companies With Ticker
df0A = i0A.merge(f0A, how = "left", on = c0)
df0A = df0A.loc[df0A['found_fec'] == True]
df0A['rid'] = df0A['iss_row_id'] + '_' + df0A['cid_master']
print(df0A.shape)


#Companies With Alt Ticker
c1 = 'ticker_alt'
f1A = f400.loc[f400[c1].notna()].drop_duplicates(subset=[c1])
f1A = f400.drop(['ticker'], axis = 1)
i1A = iss_base.loc[iss_base[c0].notna()]
df1A = i1A.merge(f1A, how = "left", left_on = c0, right_on = c1)
df1A = df1A.loc[df1A['found_fec'] == True]
df1A['rid'] = df1A['iss_row_id'] + '_' + df1A['cid_master']
print(df1A.shape)

#print(i1A.shape)


#Concat Data and Drop Duplicates
df = pd.concat([df0A, df1A], axis = 0)
print(df.shape)

#But duplicates are okay by cid_master

df = df.drop_duplicates(subset=['rid'], keep='first')
df.to_csv("test_iss_joined.csv", index=False)



#Company Counts 
cc = df.drop_duplicates(subset=['company_id'])
print("Found a total of {} companies using ISS company_id...".format(cc.shape[0]))

cc = df.drop_duplicates(subset=['cid_master'])
print("Found a total of {} companies using fec cid_master...".format(cc.shape[0]))

cc = df.drop_duplicates(subset=['list_id'])
print("Found a total of {} companies using fec list_id...".format(cc.shape[0]))



print(f400.notna().sum())


#What Companies Are Not Being Found
#f4cc = f400[['cid_master']].merge(cc['cid_master'])
f4 = f400[['cid_master', 'ticker', 'ticker_alt', 'cusip', 'found_fec']]


f4cc = anti_join(f4, cc, key='cid_master')

print(f4cc)
f4cc.to_csv('test_f4cc.csv', index=False)

#f0A = f400.loc[f400[c0].notna()].drop_duplicates(subset=[c0])
#print(f0A[['cid_master', 'ticker']])

#




#Companies with Ticker Alt

#Companies with CUSIP



#print(iss_base)

#Left Join ISS Data with FEC by Ticker