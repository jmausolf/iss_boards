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


#Read Data
df = pd.read_csv("../data/DIME/aoi_data/bod_fortune_500_DIME.csv")

#Extract Category Columns
df_cat = df[['ticker', 'privatefirm', 'sector', 'industry']].drop_duplicates()

#Get Overall DIME Stats For Company (In All Years)
gb = ['ticker']
tmp = df.groupby(gb).agg({'dime.cfscore': ['mean', 'median', 'min', 'max'],
                          'total.dem': ['sum', 'mean', 'median', 'min', 'max'],
                          'total.rep': ['sum', 'mean', 'median',  'min', 'max']
    
})

df = tmp.reset_index()

#Clean Column Names
cols = df.columns
clean_cols = [clean_col(c) for c in cols]
df.columns = clean_cols

#Join Category Columns
df = df_cat.merge(df)

#Save DIME Data
df.to_csv("../data/DIME/aoi_data/dime_aoi_metrics.csv", index=False)

