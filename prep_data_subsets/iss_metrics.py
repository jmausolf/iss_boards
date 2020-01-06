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
    c4 = c3.replace('.', '_').lower()
    c5 = c4.replace('\n', '').strip()
    return c5



#Load Data
df = pd.read_csv("iss_fec_tmp.csv")

gb = ['cid_master', 'year']
tmp = df.groupby(gb)['fullname'].count()
print(tmp)

#df = pd.DataFrame(tmp.unstack('year').to_records())
#df = pd.DataFrame(tmp.unstack('cid_master').to_records())

#Use this to get stats for various things
tmp = df.groupby(gb).agg({'age': ['mean', 'std', 'max'],
                          'fullname': ['count']
    
})

df = tmp.reset_index()
df = pd.DataFrame(df.to_records())

#Clean Column Names
cols = df.columns
clean_cols = [clean_col(c) for c in cols]
df.columns = clean_cols


#Need to Also Get Stats for If Set Composition is the Same or Not



print(df)
print(df.columns)