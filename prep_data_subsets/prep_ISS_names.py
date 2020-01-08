import pandas as pd 
import numpy as np 

from name_utils import *


def test_names(df, var):

	df['test_col'] = df[var].str.replace('B', 'b8X8X8X000')

	return df




def clean_fullname_col(name_col, df):

	clean_col = name_col+"_clean"

	#make copy of name
	df[clean_col] = df[name_col]

	#add join multipart last names, e.g. van geis = vangeis mc afee = mcafee,
	#df = join_last_names(clean_col, df)
	df = lower_clean_strip(clean_col, df) 
	df = rm_titles_suffixes(clean_col, df)

	df = extract_nickname(clean_col, df)



	#correct non reversed names with commas
	#df = correct_non_reversed_names(clean_col, df)

	#Extract Suffix/Title


	#df = reverse_names(clean_col, df, delim=',')
	#df = rm_punct_except_period_dash(clean_col, df)
	#df = concat_name_initials(clean_col, df)
	#df = rm_suffixes_titles(clean_col, df)
	#df = sep_first_middle(clean_col, df)
	#df = lower_clean_strip(clean_col, df)
	#df = rm_middle_name(clean_col, df)

	return df


def clean_suffix_col(name_col, df):

	clean_col = name_col+"_tmp"

	#make copy of name
	df[clean_col] = df[name_col]

	#Generate Suffix Col
	df = lower_clean_strip(clean_col, df) 
	df = extract_titles_suffixes(clean_col, df)

	return df

