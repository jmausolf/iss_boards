import pandas as pd 
import numpy as np 

from name_utils import *


def clean_fullname_col(name_col, df):

	clean_col = name_col+"_clean"

	#make copy of name
	df[clean_col] = df[name_col]
	df = lower_clean_strip(clean_col, df) 
	df = rm_titles_suffixes(clean_col, df)

	#Get Nickname Column and Extract from Fullname
	df = extract_nickname(clean_col, df)

	return df


def clean_firstname_col(name_col, df):

	clean_col = name_col+"_clean"

	#make copy of name
	df[clean_col] = df[name_col]
	df = lower_clean_strip(clean_col, df)

	#Remove & Names
	s = df[clean_col].str.split(r'\&', expand=True)
	s = s[0]
	print(s)

	#s = s[clean_col]
	s = s.str.strip()
	s = s.str.replace(r"\s{2,}", ' ')
	s = s.str.strip()
	print(s)


	#s.columns = [clean_col]
	s.name = clean_col


	print(s)
	df = df.drop(clean_col, axis=1)
	df = pd.concat([df, s], axis=1)
	print(df)
	print(df.columns)

	#Get Nickname Column and Extract from Fullname
	df = extract_nickname(clean_col, df, keep=False)

	#Concat and Lagging Middle Initials
	df = concat_name_initials(clean_col, df)
	df = rm_middle_initials(clean_col, df)

	return df


def clean_lastname_col(name_col, df):

	clean_col = name_col+"_clean"

	#make copy of name
	df[clean_col] = df[name_col]
	df = lower_clean_strip(clean_col, df)



	#remove titles and suffixes
	#df = rm_titles_suffixes(clean_col, df)

	return df



def make_alt_fullnames(df):

	fn = 'first_name_clean'
	ln = 'last_name_clean'
	nn = 'nickname'

	df['fullname_clean_simple'] = df[fn]+' '+df[ln]
	df['fullname_clean_nickname'] = df[nn]+' '+df[ln]

	#Fullname Simple, No Middle Name
	clean_col = 'fullname_clean_pure'

	#make copy of name
	df[clean_col] = df['fullname_clean_simple']
	df = rm_middle_name(clean_col, df)

	return df


def clean_suffix_col(name_col, df):

	clean_col = name_col+"_tmp"

	#make copy of name
	df[clean_col] = df[name_col]

	#Generate Suffix Col
	df = lower_clean_strip(clean_col, df) 
	df = extract_titles_suffixes(clean_col, df)

	return df

