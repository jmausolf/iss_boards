import pandas as pd 
import numpy as np 


def clean_col(col):
    c0 = str(col).replace(", '')", ")")
    c1 = c0.replace('(', '').replace(')', '')
    c2 = c1.replace("'", "").replace(' ', '')
    c3 = c2.replace(',', '_').lower()
    c4 = c3.replace('.', '_').lower()
    c5 = c4.replace('\n', '').strip()
    return c5




#Load Cleaned Names
df = pd.read_csv("../data/FEC/cleaned_names_fec_df_analysis.csv")

#TODO see if metrics can be combined and recalculated
#Remove Extra Rows from Duplicate Names
gb = ['cid_master', 'cycle', 'fullname_fec']
tmp = df.groupby(gb).agg({'fullname_fec': ['count'],
                          'sub_id_count': ['max']})
tmp = pd.DataFrame(tmp.to_records())

#Clean Column Names and Join
cols = tmp.columns
clean_cols = [clean_col(c) for c in cols]
tmp.columns = clean_cols
df = df.merge(tmp)


#Keep Criteria
keep_crit = (
				(df['fullname_fec_count'] == 1) |

				( (df['fullname_fec_count'] > 1 ) &
				  (df['sub_id_count'] == df['sub_id_count_max'])			

				)

			 )

df = df.loc[keep_crit]
print(df)
df.to_csv("../data/FEC/clean_fec_df_analysis.csv", index=False)
