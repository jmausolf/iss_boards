import pandas as pd 
import numpy as np 

from prep_ISS_names import *

#################################################################
# Utility Functions
#################################################################

def anti_join(df_A, df_B, key):

	set_diff = set(df_A[key]).difference(df_B[key])
	bool_diff = df_A[key].isin(set_diff)
	df_diff = df_A.loc[bool_diff]

	return df_diff


def clean_col(col):
    c1 = str(col).replace('(', '').replace(')', '')
    c2 = c1.replace("'", "").replace(' ', '')
    c3 = c2.replace(',', '_').lower()
    c4 = c3.replace('\n', '').strip()
    return c4


def convert_cycle(year):
	if int(year) % 2 == 0:
		cycle = str(year)
	else:
		cycle = str(int(year)+1)
	return cycle


#Load ISS Base Data
iss_base = pd.read_csv("../data/ISS/ISS_Boards.csv", low_memory=False)
iss_base['cusip_iss'] = iss_base['cusip']
iss_base.drop(['cusip'], axis=1, inplace=True)
iss_base['iss_row_id'] = iss_base.index.astype(str)
print(iss_base.shape)

#Load F400 Data (FEC Subset)
f400 = pd.read_csv("../data/F400/f400_linked_unique.csv")
f400['cusip_fec'] = f400['cusip']
f400.drop(['cusip'], axis=1, inplace=True)


#Companies With Ticker
c0 = 'ticker'
f0A = f400.loc[f400[c0].notna()]
f0A = f400
i0A = iss_base.loc[iss_base[c0].notna()]
df0A = i0A.merge(f0A, how = "left", on = c0)
df0A = df0A.loc[df0A['found_fec'] == True]
df0A['rid'] = df0A['iss_row_id'] + '_' + df0A['cid_master']
print(df0A.shape)


#Companies With Alt Ticker
c1 = 'ticker_alt'
f1A = f400.loc[f400[c1].notna()]
f1A = f400.drop(['ticker'], axis = 1)
i1A = iss_base.loc[iss_base[c0].notna()]
df1A = i1A.merge(f1A, how = "left", left_on = c0, right_on = c1)
df1A = df1A.loc[df1A['found_fec'] == True]
df1A['rid'] = df1A['iss_row_id'] + '_' + df1A['cid_master']
print(df1A.shape)


#Companies With CUSIP
c2l = 'cusip_iss'
c2r = 'cusip_fec'
f2A = f400.loc[f400[c2r].notna()]
i2A = iss_base.loc[iss_base[c2l].notna()]
df2A = i2A.merge(f2A, how = "left", 
					  left_on = [c2l, c0],
					  right_on = [c2r, c0])
df2A = df2A.loc[df2A['found_fec'] == True]
df2A['rid'] = df2A['iss_row_id'] + '_' + df2A['cid_master']
print(df2A.shape)



#Concat Data and Drop Duplicates
df = pd.concat([df0A, df1A, df2A], axis = 0)
#df = pd.concat([df0A, df1A], axis = 0)

#Clean Column Names
cols = df.columns
clean_cols = [clean_col(c) for c in cols]
df.columns = clean_cols

#Only Keep ISS Row ID X cid_master Unique Obs
df = df.drop_duplicates(subset=['rid'], keep='first')


#ADD DIME AOI Company Metrics
dm = pd.read_csv("../data/DIME/aoi_data/dime_aoi_metrics.csv")
df = df.merge(dm, how = 'left', on = 'ticker')


#Add Election Cycle Column
df['cycle'] = df['year'].apply(convert_cycle)

#Clean ISS Names
df = clean_firstname_col("first_name", df)
df = clean_lastname_col("last_name", df)
df = clean_suffix_col("fullname", df)
df = clean_fullname_col("fullname", df)
df = make_alt_fullnames(df)

print(df)

#year


#TODO
#add my FEC company measures

###################################
#TODO: Join ISS names by company
###################################

#NEED a seperate py file
#steps, clean iss / fec names using same method
#try direct match by ticker/company and name

#if not enough found, could try partial matches or fuzzy match
#on the rest

#iss file cols:
# 	

#fec files 
#




#Save Result
df.to_csv("iss_fec_tmp.csv", index=False)
print(df.columns)
print(df)


##QC

#Company Counts 
cc = df.drop_duplicates(subset=['company_id'])
print("Found a total of {} companies using ISS company_id...".format(cc.shape[0]))

cc = df.drop_duplicates(subset=['cid_master'])
print("Found a total of {} companies using fec cid_master...".format(cc.shape[0]))

cc = df.drop_duplicates(subset=['list_id'])
print("Found a total of {} companies using fec list_id...".format(cc.shape[0]))



#What Companies Are Not Being Found
f4 = f400[['cid_master', 'ticker', 'ticker_alt', 'found_fec']]
f4cc = anti_join(f4, cc, key='cid_master')
print(f4cc)
f4cc.to_csv('not_found_iss_fec.csv', index=False)


