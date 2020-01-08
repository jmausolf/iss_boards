import pandas as pd
import numpy as np
from glob import glob
import re
import unicodedata
import sys
import json
import subprocess



#Some Utility Functions for Cleaning the Data

def remove_non_ascii_2(text):
	import re
	return re.sub(r'[^\x00-\x7F]+', "", text)


def remove_punct(text):
	import re
	return re.sub(r'[]\\?!\"\'#$%&(){}+*/:;,._`|~\\[<=>@\\^-]', "", text)





def replace_char(var, df, inchar=',', outchar='_'):

	s = df[var].str.replace(inchar, outchar)
	s.name = var
	df = df.drop(var, axis=1)
	df = pd.concat([df, s], axis=1)
	return(df)



def rm_suffixes_titles(var, df):

	s = df[var]

	#suffixes
	s = s.str.replace(' jr.', ' ').str.replace(' junior', ' ').str.replace(' jr', ' ')
	s = s.str.replace(' sr.', ' ').str.replace(' senior', ' ').str.replace(' sr', ' ')
	s = s.str.replace(' iii.', ' ').str.replace(' the third', ' ').str.replace(' third', ' ')
	s = s.str.replace(' iv.', ' ').str.replace(' the fourth', ' ').str.replace(' fourth', ' ')
	s = s.str.strip()

	#titles
	s = s.str.replace(' mr.', ' ').str.replace(' mr', ' ')
	s = s.str.replace(' ms.', ' ').str.replace(' ms', ' ')
	s = s.str.replace(' mrs.', ' ').str.replace(' mrs', ' ')
	s = s.str.replace(' miss.', ' ').str.replace(' miss', ' ')
	s = s.str.strip()


	#lingering mr, ms, mrs
	pat = r'(\b[mr]{2,3}\s)|(\b[ms]{2,3}\s)|(\b[mrs]{3,3}\s)'
	s = s.str.replace(pat, ' ').str.strip()

	#other titles or suffixes not caught (with periods)
	s = s.str.replace(r'(\b[a-z]{2,3}\.)', ' ')



	#degrees
	#s = s.str.replace(' dr.', ' ').str.replace(' dr', ' ')
	#s = s.str.replace(' m.d.', ' ').str.replace(' md', ' ')
	#s = s.str.replace(' ph.d.', ' ').str.replace(' phd', ' ')
	#s = s.str.replace(' j.d.', ' ').str.replace(' jd', ' ')
	#s = s.str.replace(' m.b.a.', ' ').str.replace(' mba', ' ')
	#s = s.str.strip()

	#replace more than one white space with a space
	s = s.str.replace(r"\s{2,}", ' ')

	#replace extra periods
	s = s.str.replace(' . ', ' ')

	s.name = var
	df = df.drop(var, axis=1)
	df = pd.concat([df, s], axis=1)
	return(df)



def concat_name_initials(var, df):

	s = df[var]

	#add periods to multiple initials without periods 
	#s = s.str.replace(r"(\b[a-z]{1,1}\s){1,2}", '\\1__')
	#s = s.str.replace(" __", '. ')

	#single letter word without period
	s = s.str.replace(r'(\b[a-z]{1,1}\s)', '\\1__')
	s = s.str.replace(" __", '. ')

	#concat initials with periods 
	s = s.str.replace(r"(\b[a-z]{1,1}\.\s)+(\b[a-z]{1,1}\.)", '\\1__\\2')
	s = s.str.replace(". __", '.')

	#s.name = var
	df = df.drop(var, axis=1)
	df = pd.concat([df, s], axis=1)
	return(df)


def split_fm(name):
	f, m = name[:-3], name[-3:]
	return "{} {}".format(f, m)


def sep_first_middle(var, df):
	s = df[var]
	pat = r"(?P<one>\w+) (?P<two>\w+) (?P<three>\w+)"
	pat = r"([a-z]{4,}\.\s)"
	repl = lambda m: split_fm(m.group(0))
	s = s.str.replace(pat, repl)
	s.name = var
	df = df.drop(var, axis=1)
	df = pd.concat([df, s], axis=1)
	return(df)



def join_last_names(var, df, sep=''):
	s = df[var]
	pat = r'(\b[A-Za-z]{2,}\s)(\b[A-Za-z]{2,}\,)'
	repl = lambda m: m.group(0).replace(' ', sep)
	s = s.str.replace(pat, repl)
	s.name = var
	df = df.drop(var, axis=1)
	df = pd.concat([df, s], axis=1)
	return(df)


def concat_split_cities(var, df, sep=''):
    s = df[var]

    #captures mc lean but not el paso
    pat = r'(\b[CMcm]{2,2}\s)(\b[A-Za-z]{1,})'
    repl = lambda m: m.group(0).replace(' ', sep)
    s = s.str.replace(pat, repl)
    s.name = var
    df = df.drop(var, axis=1)
    df = pd.concat([df, s], axis=1)
    return(df)


def rm_mid_initials_suffixes(var, df):

	s = s.str.replace(r"\,\s[a-z]+", '')


	s = s.str.replace(' jr', ' ').str.replace(' junior', ' ')
	s = s.str.replace(' sr', ' ').str.replace(' senior', ' ')
	s = s.str.replace(' iii', ' ').str.replace(' third', ' ').str.replace(' the third', ' ')
	s = s.str.replace(' iv', ' ').str.replace(' fourth', ' ').str.replace(' the fourth', ' ')
	s = s.str.strip()

	#replace more than one white space with a space
	s = s.str.replace(r"\s{2,}", ' ')

	s.name = var
	df = df.drop(var, axis=1)
	df = pd.concat([df, s], axis=1)
	return(df)



def keep_first_last(namelist):
	try:
		if len(namelist) >= 3:
			first = namelist[0]
			last = namelist[-1]
			first_last = [first, last]

			if re.match(r'([a-z]+\.)+', first):
				name = " ".join(namelist).strip()
			else:
				name = " ".join(first_last).strip()

		else:
			name = " ".join(namelist).strip()

		return name

	except Exception as e:
		print("[*] Error: {}, exception when removing middle name...".format(e))
		return namelist

def rm_middle_name(var, df):
	s = df[var].fillna('unknown')
	s = s.str.split(r'\s')
	s = s.apply(lambda name: keep_first_last(name))
	s.name = var
	df = df.drop(var, axis=1)
	df = pd.concat([df, s], axis=1)
	return(df)


def clean_cols(df):
	df.columns = [remove_punct(x) for x in df.columns]
	df.columns = [x.lower().replace(' ', '') for x in df.columns]
	return(df)




def split_subjects(var, df):
	#Make a Copy
	df['original'] = df[var]

	#Split on Subjects by ';'
	s = df[var].str.replace(', ', '_').str.replace('; ', ';').str.split(';')
	s.name = var
	df = df.drop(var, axis=1).join(s)

	#Convert Multiple Subjects to Multiple Rows
	s = df.apply(lambda x: pd.Series(x[var]),axis=1).stack().reset_index(level=1, drop=True)
	s.name = var
	df = df.drop(var, axis=1).join(s)
	return(df)

def split_subjects_2vars(var1, sep1, var2, sep2, df):

	s1 = df[var1].str.split(sep1, expand=True).stack().str.strip().reset_index(level=1, drop=True)
	s2 = df[var2].str.split(sep2, expand=True).stack().str.strip().reset_index(level=1, drop=True)
	
	print(s1.shape)
	print(s2.shape)
	df1 = pd.concat([s1,s2], axis=1, keys=[var1, var2])

	df = df.drop([var1, var2], axis=1).join(df1).reset_index(drop=True)
	return df


def split_sep_var(var, sep, df):
	return df[var].str.split(sep, expand=True).stack().str.strip().reset_index(level=1, drop=True)
	

def split_subjects_nvars(vslist, df):

	varlist = []
	seplist = []
	series_list = []

	for vs in vslist:
		var = vs[0]
		sep = vs[1]

		varlist.append(var)
		seplist.append(sep)

		s = split_sep_var(var, sep, df)
		series_list.append(s)

	df1 = pd.concat(series_list, axis=1, keys=varlist)
	df = df.drop(varlist, axis=1).join(df1).reset_index(drop=True)
	return df



def split_subjects_gv(var, df):
	#Make a Copy
	df['original'] = df[var]

	#Split on Subjects by '}, {', will not allow replace '[{' or '}]'
	s = df[var].str.replace('}, {', 'x_x, x_x')
	s = s.str.replace('{', '').str.replace('}', '')
	s = s.str.replace('[', '').str.replace(']', '').str.split("x_x, x_x")
	s.name = var
	df = df.drop(var, axis=1).join(s)

	#Convert Multiple Subjects to Multiple Rows
	s = df.apply(lambda x: pd.Series(x[var]),axis=1).stack().reset_index(level=1, drop=True)
	s.name = var
	df = df.drop(var, axis=1).join(s)

	#Turn back into a dictionary
	df[var] = ('{' + df[var] + '}')
	return(df)


def split_vars(ovar, nvar1, nvar2, delim, df):
	df[nvar1], df[nvar2] = df[ovar].str.split(delim, 1).str
	df.drop([ovar], axis=1, inplace=True)
	return(df)


def split_race_gender(df):
	#Split Race/Gender to New Vars
	df['name'], df['race_gender'] = df['subjects'].str.split(' ', 1).str
	df['race'], df['gender'] = df['race_gender'].str.split('/', 1).str
	df.drop(['subjects', 'race_gender'], axis=1, inplace=True)
	return(df)


def reverse_names(var, df, lower=True, delim=','):
	d = delim
	if lower is True:
		s = df[var].apply(lambda x: d.join(x.split(d)[::-1])).str.replace(d, ' ').str.lower().str.strip()
	else:
		s = df[var].apply(lambda x: d.join(x.split(d)[::-1])).str.replace(d, ' ').str.strip()
	#df = df.drop(var, axis=1).join(s)
	df = df.drop(var, axis=1)
	df = pd.concat([df, s], axis=1)
	return(df)


def correct_non_reversed_names(var, df):
	pat = r"(\b[A-Za-z]+\s)((\b[A-Za-z]{0,1}\,)|(\b[A-Za-z]{0,1}\.,))"
	repl = lambda m: m.group(0).replace(',', '  ')
	s = df[var].str.replace(pat, repl)
	s.name = var
	df = df.drop(var, axis=1)
	df = pd.concat([df, s], axis=1)
	return df

def lower_var(var, df):
	s = df[var].str.lower()
	df = df.drop(var, axis=1)
	df = pd.concat([df, s], axis=1)
	return(df)


def lower_clean_strip(var, df):
    s = df[var].str.lower()
    s = s.str.replace(r"\s\-\s", '-')
    s = s.str.replace(r"\s\.", ' ')
    s = s.str.replace(r"\s{2,}", ' ')
    s = s.str.strip()
    df = df.drop(var, axis=1)
    df = pd.concat([df, s], axis=1)
    return(df)


def rm_punct_except_period_dash_comma(var, df):
	s = df[var].str.lower()
	s = s.str.replace(r'[]\\?!\"\'#$%&(){}+*/:;_`|~\\[<=>@\\^]', '')
	df = df.drop(var, axis=1)
	df = pd.concat([df, s], axis=1)
	return(df)

def rm_punct_except_period_dash(var, df):
	s = df[var].str.lower()
	s = s.str.replace(r'[]\\?!\"\'#$%&(){}+*/:;,_`|~\\[<=>@\\^]', '')
	df = df.drop(var, axis=1)
	df = pd.concat([df, s], axis=1)
	return(df)

def rm_punct_col(var, df):
    s = df[var].str.lower()
    s = s.str.replace(r'[]\\?!\"\'#$%&(){}+*/:;,._`|~\\[<=>@\\^-]', '')
    df = df.drop(var, axis=1)
    df = pd.concat([df, s], axis=1)
    return(df)


def title_var(var, df):
	s = df[var].str.title()
	df = df.drop(var, axis=1)
	df = pd.concat([df, s], axis=1)
	return(df)


def lower_var_rm_nonascii(var, df):
	print("remove_non_ascii_2")
	s = df[var].str.lower().replace('\u201c', '')
	df = df.drop(var, axis=1).join(s)
	return(df)


def ren(invar, outvar, df):
	df.rename(columns={invar:outvar}, inplace=True)
	return(df)


def map_dict_col(var, df):
	"""
	## Maps a col containing dict's to seperate columns
	## Expected variable cell: '{u'key': u'value', u'key': u'value'}
	"""
	s = df[var].map(eval)
	df = pd.concat([df.drop([var], axis=1), s.apply(pd.Series)], axis=1)
	return df



def extract_suffixes(var, df):
	s = df[var]

	#suffix patterns (end)
	s1 = s.str.extract(r'(i{2,}$)|(sr$)|(jr$)|(junior$)')
	s1 = s1.apply(lambda x: ','.join(x.dropna()), axis=1)
	#s1.name = 'suffix'
	#print(s)

	#suffix patterns (middle)
	s2 = s.str.extract(r'(\si{2,}\s)|(\ssr\s)|(\sjr\s)|(\sjunior\s)')
	s2 = s2.apply(lambda x: ','.join(x.dropna()), axis=1)

	#renuite
	sf = pd.concat([s1, s2], axis=1)
	sf = sf.apply(lambda x: ''.join(x.dropna()), axis=1)
	sf.name = 'suffix'

	#s.name = var
	#df = df.drop(var, axis=1)
	df = pd.concat([df, sf], axis=1)
	return(df)


def extract_fullname(var, df, outcol='fullname'):
	s = df[var]

	#suffix patterns 
	pat1 = r'(i{2,}$)|(sr$)|(jr$)|(junior$)'
	pat2 = r'(\si{2,}\s)|(\ssr\s)|(\sjr\s)|(\sjunior\s)'
	s = s.str.replace(pat1, '').str.replace(pat2, '')
	s = s.str.replace(r"\s{2,}", ' ')
	s = s.str.strip()
	s.name = outcol

	df = pd.concat([df, s], axis=1)
	return(df)

def rm_titles_suffixes(var, df, outcol=None):
	s = df[var]

	#suffix patterns 
	pat1 = r'(,\s*.+)|(\s[Jj][Rr].)|(\s[Ii]{2,}$)'
	s = s.str.replace(pat1, '')
	s = s.str.replace(r"\s{2,}", ' ')
	s = s.str.strip()

	if outcol is None:
		df = df.drop(var, axis=1).join(s)
	else:
		s.name = outcol
		df = pd.concat([df, s], axis=1)
	
	return(df)


def extract_titles_suffixes(var, df):
	s = df[var]
	pat = r'(,\s*.+)|(\s[Jj][Rr].)|(\s[Ii]{2,}$)'
	s = s.str.extract(pat)
	s = s.apply(lambda x: ','.join(x.dropna()), axis=1)
	s = s.str.replace(r'(^,\s+)|(^\s)|(\s$)', '')
	s.name = 'suffix'
	df = df.drop(var, axis=1).join(s)
	return(df)


def extract_nickname(var, df):

	s = df[var]
	pat = r'\(.+\)'

	#Remove Nickname From Fullname
	s1 = s.str.replace(r'\(.+\)', '')
	s1 = s1.str.replace(r"\s{2,}", ' ')
	s1 = s1.str.strip()

	#Make Nickname Column
	punct = r'[]\\?!\"\'#$%&(){}+*/:;,._`|~\\[<=>@\\^-]'
	s2 = s.str.extract(r'(\(.+\))')
	s2.columns = ['nickname']
	s2 = s2['nickname'].str.replace(punct, '')
	s2.name = 'nickname'

	#Join and Return
	df = df.drop(var, axis=1)
	df = pd.concat([df, s1, s2], axis=1)
	print(df)
	return(df)


def split_first_last(var, df):

	#import pdb; pdb.set_trace()
	s = df[var]

	#Get Full First Name, Last Name
	s1 = s.str.rsplit(' ', n=1, expand=True)
	#s.columns = ['first', 'last', 'other']
	s1.columns = ['full_first', 'last']
	print(s1.columns)


	#Get Simple First and Middle Name Sep
	s2 = s.str.split(' ', n=2, expand=True)
	s2.columns = ['first_simple', 'middle', 'other']
	s2['middle'] = np.where(s2['other'].notna(), 
									s2['middle'], None)
	s2.drop(['other'], axis=1, inplace=True)


	#Combine and Simplify
	s = pd.concat([s1, s2], axis=1)
	s = s[['full_first', 'first_simple', 'middle', 'last']]


	df = pd.concat([df, s], axis=1)
	return(df)










