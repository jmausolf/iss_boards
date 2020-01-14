import pandas as pd 
import numpy as np 

from name_utils import *
from prep_dime_names import *


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


#################################################################
# Core Data
#################################################################

#Load DIME Data
dm1 = pd.read_csv("../data/DIME/aoi_data/bod_fortune_500_DIME.csv")
dm2 = pd.read_csv("../data/DIME/aoi_data/bod_fortune_500_DIME_cont_records.csv")


#################################################################
# Clean Names
#################################################################


#Clean DM2 Names
dm2 = clean_firstname_col("contributor.fname", dm2)
dm2 = clean_lastname_col("contributor.lname", dm2)

dm2.to_csv("../data/DIME/aoi_data/cleaned_bod_fortune_500_DIME_cont_records.csv", index=False)


#Clean DM1 Names
dm1 = clean_firstname_col("first.name", dm1)
dm1 = clean_lastname_col("last.name", dm1)

dm1.to_csv("../data/DIME/aoi_data/cleaned_bod_fortune_500_DIME.csv", index=False)

#df = df.drop(['contributor.lname', 'contributor.fname'], axis=1)


