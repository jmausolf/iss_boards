import pandas as pd 
import numpy as np 

from collections import Counter 
from collections import ChainMap

#from test_dict import *

#from recode_events import *



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
#Get Board Change Functions
#################################################################


def get_board_metrics(row):

    list_ds2 = row['board']
    list_ds1 = row['prior_board']

    #Get Current List Max
    #Should Not Be > 1
    m = Counter(list_ds2).most_common(1)[0][1]

    if m > 1:
        dupe_qc = True
    else:
        dupe_qc = False
    row['dupes_bm'] = dupe_qc

    #New/Added Elements
    new_items = list((Counter(list_ds2) - Counter(list_ds1)).elements())
    new_items.sort()
    row['new_bm'] = new_items

    ni_n = len(new_items)
    row['new_bm_count'] = ni_n

    #Old/Dropped Elements
    old_items = list((Counter(list_ds1) - Counter(list_ds2)).elements())
    old_items.sort()
    row['dropped_bm'] = old_items

    oi_n = len(old_items)
    row['dropped_bm_count'] = oi_n

    #Intersection/Persistent Elements
    s1 = set(list_ds1)
    s2 = set(list_ds2)

    intersection = list(s1.intersection(s2))
    intersection.sort()
    row['constant_bm'] = intersection

    i_n = len(intersection)
    row['constant_bm_count'] = i_n

    return row


def lsort(lst):
    lst.sort()
    return lst


#################################################################
#Get Board Party Change Functions
#################################################################


#Make A Column of Name, Party Dicts
def make_row_dict(row, name_key, party_val):

    k = row[name_key]
    v = row[party_val]

    d = {k: v}

    row['name_party'] = d 

    return row


def c_dict(lst):
    d = dict(ChainMap(*lst))
    return d


def get_party_bm_change(row, party_col):

    n_bm = row['new_bm']
    d_bm = row['dropped_bm']

    n_dict = row['bp_dict']
    d_dict = row['prior_bp_dict']

    #Set Outcols
    nbp = 'new_bm_{}'.format(party_col)
    dbp = 'dropped_bm_{}'.format(party_col)


    #Get New BM Parties
    if len(n_bm) == 0:
        row[nbp] = []
    else:
        n_bm_party = []
        for k in n_bm:
            p = n_dict[k]
            n_bm_party.append(p)
        row[nbp] = n_bm_party


    #Get Dropped BM Parties
    if len(d_bm) == 0:
        row[dbp] = []
    else:
        d_bm_party = []
        for k in d_bm:
            p = d_dict[k]
            d_bm_party.append(p)
        row[dbp] = d_bm_party

    return row


#################################################################
#Recode Event Change Functions
#################################################################

def flatten(lst):
    f = []
    for i in lst:
        if isinstance(i,list):
            f.extend(flatten(i))
        else:
            f.append(i)
    return f


def get_simple_event(i):

    if i == 'NO_CHANGE' or i == 'OTHER':
        return [i]
    else:
        n = int(i.split('_', 1)[0])
        if '_SWAP' in i:
            v = 'SWAP'
            return [v for x in range(0, n)]
        if '_ADD' in i:
            v = 'ADD'
            return [v for x in range(0, n)]
        if '_DROP' in i:
            v = 'DROP'
            return [v for x in range(0, n)]
        else:
            return i


def recode_events(row, simple=True):

    #Out Col 
    o = 'board_change_events_list'

    #Get Column
    i = row['board_all_change_events']

    #Drop Spaces
    i = i.replace(r'\s', '').replace(' ', '')

    #Get Multiple Events
    s = i.split(',')

    if len(s) > 1:
        if simple is True:
            s0 = [get_simple_event(i) for i in s]
            row[o] = flatten(s0)
        else:
            row[o] = s

    else:
        if simple is True:
            i0 = get_simple_event(i)
            row[o] = flatten(i0)
        else:
            row[o] = [i]

    return row


#################################################################
#Convert Multiple Change Events to Rows
#################################################################


def split_sep_var(var, sep, df):

    #Strip Out List, String Elements
    v = df[var].str.replace('[', '').str.replace(']','')
    v = v.str.replace("'", '')
    v = v.str.split(sep, expand=True).stack().str.strip()
    v = v.reset_index(level=1, drop=True)
    return v
    #return df[var].str.split(sep, expand=True).stack().str.strip().reset_index(level=1, drop=True)
    

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
dm = dm.loc[(dm['cid_master'] == 'Marathon Petroleum') | (dm['cid_master'] == 'Apple' )]


dm = dm[['cid_master', 'ticker', 'year', 'cycle', 'fullname_clean_pure', 'party']]
#print(dm)

#Make Copy with NA & Fill NA Party Values with UNK
dm['party_na'] = dm['party']
dm['party'] = dm['party'].fillna("UNK")
print(dm.shape)

#################################################################
#Add Some Basic Metrics
#################################################################

#Add Yearly Board Size Column
gb = ['ticker', 'year']
tmp = dm.groupby(gb)['fullname_clean_pure'].count().reset_index()
tmp.columns = ['ticker', 'year', 'board_size']
dm = dm.merge(tmp)


#Add Numeric Party Cols
p = 'party'
dm['pid3n'] = np.where(dm[p] == "DEM", -1,
                    np.where(dm[p] == "REP", 1,
                    np.where(dm[p].notna(), 0, None)))
dm['pid3n'] = pd.to_numeric(dm['pid3n'])

p = 'party_na'
dm['pid2n'] = np.where(dm[p] == "DEM", -1,
                    np.where(dm[p] == "REP", 1, None))
dm['pid2n'] = pd.to_numeric(dm['pid2n'])

#TODO Add MICE Imputed Col

#Add Mean Imputed PID2N Col
gb = ['ticker', 'year']
tmp1 = dm[['ticker', 'year', 'pid2n']].copy()
tmp1['pid2ni_mean'] = tmp1.groupby(gb).transform(lambda x: x.fillna(x.mean()))
tmp1 = tmp1[['pid2ni_mean']]

#Add Median Imputed PID2N Col
tmp2 = dm[['ticker', 'year', 'pid2n']].copy()
tmp2['pid2ni_med'] = tmp2.groupby(gb).transform(lambda x: x.fillna(x.median()))
tmp2 = tmp2[['pid2ni_med']]

#Make a Character of Imputed Column
c = 'pid2ni_med'
tmp2['pid2ni_med_str'] = np.where(tmp2[c] < 0, "DEM",
                                  np.where(tmp2[c] > 0, "REP", None))



#import pdb; pdb.set_trace()

dm = pd.concat([dm, tmp1, tmp2], axis=1)
print(dm.shape)

#Add Yearly Board Size Column
gb = ['ticker', 'year']
#tmp = dm.groupby(gb)['fullname_clean_pure'].count().reset_index()

tmp = dm.groupby(gb).agg({'pid2n' : ['mean', 'median'],
                          'pid2ni_mean' : ['mean', 'median'],
                          'pid2ni_med' : ['mean', 'median'],
                          'pid3n' : ['mean', 'median']

                          }).reset_index()

#Clean Column Names
cols = tmp.columns
clean_cols = [clean_col(c) for c in cols]
tmp.columns = clean_cols

#Merge Party Metrics
dm = dm.merge(tmp)



#################################################################
#Get Board Member Change Metrics
#################################################################

#Get Yearly Board Member List
c = 'fullname_clean_pure'
tmp = dm.groupby(gb)[c].apply(list).apply(lsort)
tmp = tmp.reset_index(name='board')

#Get Lagged Board List (By Company)
tmp['prior_board'] = tmp.groupby(['ticker'])['board'].shift(1)


#Get Board Change Results
tmp = tmp.dropna(subset=['prior_board'])
tmp =  tmp.apply(get_board_metrics, axis=1)

#Add Yearly Board Member Change Metrics
dm0 = dm.merge(tmp)
print(dm0.shape)
print(dm0.columns)

dm0.to_csv("test_metrics.csv", index=False)

#################################################################
#Need Board Change Flags
#################################################################

c1 = 'new_bm_count'
c2 = 'dropped_bm_count'
dm0['net_added'] = dm0[c1] - dm0[c2]
dm0['net_added'] = dm0.net_added.astype(str)
dm0['net_dropped'] = dm0[c2] - dm0[c1]
dm0['net_dropped'] = dm0.net_dropped.astype(str)

#print(dm0.isna().sum())

#print(dm0.dtypes)

dm0['board_net_change'] = np.where( ((dm0[c1] == 0) & (dm0[c2] == 0)), "NO_CHANGE",
                    np.where( ((dm0[c1] == dm0[c2]) & (dm0[c1] == 1)), "1_BM_SWAP",
                    np.where( ((dm0[c1] == dm0[c2]) & (dm0[c1] == 2)), "2_BM_SWAP",
                    np.where( ((dm0[c1] == dm0[c2]) & (dm0[c1] == 3)), "3_BM_SWAP",
                    np.where( ((dm0[c1] == dm0[c2]) & (dm0[c1] > 3)), "N_BM_SWAP",

                    np.where( ((dm0[c1] > dm0[c2]) & (dm0[c1] - dm0[c2] == 1)), "1_BM_ADD",
                    np.where( ((dm0[c1] > dm0[c2]) & (dm0[c1] - dm0[c2] == 2)), "2_BM_ADD",
                    np.where( ((dm0[c1] > dm0[c2]) & (dm0[c1] - dm0[c2] == 3)), "3_BM_ADD",
                    np.where( ((dm0[c1] > dm0[c2]) & (dm0[c1] - dm0[c2] > 3)), "N_BM_ADD",

                    np.where( ((dm0[c1] < dm0[c2]) & (dm0[c2] - dm0[c1] == 1)), "1_BM_DROP",
                    np.where( ((dm0[c1] < dm0[c2]) & (dm0[c2] - dm0[c1] == 2)), "2_BM_DROP",
                    np.where( ((dm0[c1] < dm0[c2]) & (dm0[c2] - dm0[c1] == 3)), "3_BM_DROP",
                    np.where( ((dm0[c1] < dm0[c2]) & (dm0[c2] - dm0[c1] > 3)), "N_BM_DROP",
                    "OTHER")))))))))))))


dm0['board_add_change'] = np.where((dm0[c1] == 1), "1_BM_ADD",
                    np.where((dm0[c1] == 2), "2_BM_ADD",
                    np.where((dm0[c1] == 3), "3_BM_ADD",
                    np.where((dm0[c1] > 3), "N_BM_ADD", ""))))

dm0['board_drop_change'] = np.where( (dm0[c2] == 1), "1_BM_DROP",
                    np.where( (dm0[c2] == 2), "2_BM_DROP",
                    np.where( (dm0[c2] == 3), "3_BM_DROP",
                    np.where( (dm0[c2] > 3), "N_BM_DROP", ""))))



a = 'new_bm_count'
d = 'dropped_bm_count'
ald = 'net_added'
dla = 'net_dropped'
dm0['board_all_change'] = np.where( 

                    #No Change
                    ((dm0[c1] == 0) & (dm0[c2] == 0)), "NO_CHANGE",

                    #Equal Replacement
                    np.where( ((dm0[c1] == dm0[c2]) & (dm0[c1] == 1)), "1_BM_SWAP",
                    np.where( ((dm0[c1] == dm0[c2]) & (dm0[c1] == 2)), "2_BM_SWAP",
                    np.where( ((dm0[c1] == dm0[c2]) & (dm0[c1] == 3)), "3_BM_SWAP",
                    np.where( ((dm0[c1] == dm0[c2]) & (dm0[c1] > 3)), "N_BM_SWAP",

                    #Only Added
                    np.where( ((dm0[c1] > dm0[c2]) & (dm0[c2] == 0) & (dm0[c1] == 1)), "1_BM_ADD",
                    np.where( ((dm0[c1] > dm0[c2]) & (dm0[c2] == 0) & (dm0[c1] == 2)), "2_BM_ADD",
                    np.where( ((dm0[c1] > dm0[c2]) & (dm0[c2] == 0) & (dm0[c1] == 3)), "3_BM_ADD",
                    np.where( ((dm0[c1] > dm0[c2]) & (dm0[c2] == 0) & (dm0[c1] > 3)), "N_BM_ADD",

                    #Only Dropped
                    np.where( ((dm0[c1] < dm0[c2]) & (dm0[c1] == 0) & (dm0[c2] == 1)), "1_BM_DROP",
                    np.where( ((dm0[c1] < dm0[c2]) & (dm0[c1] == 0) & (dm0[c2] == 2)), "2_BM_DROP",
                    np.where( ((dm0[c1] < dm0[c2]) & (dm0[c1] == 0) & (dm0[c2] == 3)), "3_BM_DROP",
                    np.where( ((dm0[c1] < dm0[c2]) & (dm0[c1] == 0) & (dm0[c2] > 3)), "N_BM_DROP",

                    #Replacement and Add
                    np.where( (dm0[c1] > dm0[c2]), dm0[d].apply(str)+'_BM_SWAP_'+dm0[ald].apply(str)+'_BM_ADD',

                    #Replacement and Drop
                    np.where( (dm0[c1] < dm0[c2]), dm0[a].apply(str)+'_BM_SWAP_'+dm0[dla].apply(str)+'_BM_DROP',

                    "OTHER")))))))))))))))


dm0['board_all_change_events'] = np.where( 

                    #No Change
                    ((dm0[c1] == 0) & (dm0[c2] == 0)), "NO_CHANGE",

                    #Equal Replacement
                    np.where( ((dm0[c1] == dm0[c2]) & (dm0[c1] == 1)), "1_BM_SWAP",
                    np.where( ((dm0[c1] == dm0[c2]) & (dm0[c1] == 2)), "2_BM_SWAP",
                    np.where( ((dm0[c1] == dm0[c2]) & (dm0[c1] == 3)), "3_BM_SWAP",
                    np.where( ((dm0[c1] == dm0[c2]) & (dm0[c1] > 3)), "N_BM_SWAP",

                    #Only Added
                    np.where( ((dm0[c1] > dm0[c2]) & (dm0[c2] == 0) & (dm0[c1] == 1)), "1_BM_ADD",
                    np.where( ((dm0[c1] > dm0[c2]) & (dm0[c2] == 0) & (dm0[c1] == 2)), "2_BM_ADD",
                    np.where( ((dm0[c1] > dm0[c2]) & (dm0[c2] == 0) & (dm0[c1] == 3)), "3_BM_ADD",
                    np.where( ((dm0[c1] > dm0[c2]) & (dm0[c2] == 0) & (dm0[c1] > 3)), "N_BM_ADD",

                    #Only Dropped
                    np.where( ((dm0[c1] < dm0[c2]) & (dm0[c1] == 0) & (dm0[c2] == 1)), "1_BM_DROP",
                    np.where( ((dm0[c1] < dm0[c2]) & (dm0[c1] == 0) & (dm0[c2] == 2)), "2_BM_DROP",
                    np.where( ((dm0[c1] < dm0[c2]) & (dm0[c1] == 0) & (dm0[c2] == 3)), "3_BM_DROP",
                    np.where( ((dm0[c1] < dm0[c2]) & (dm0[c1] == 0) & (dm0[c2] > 3)), "N_BM_DROP",

                    #Replacement and Add
                    np.where( (dm0[c1] > dm0[c2]), dm0[d].apply(str)+'_BM_SWAP,'+dm0[ald].apply(str)+'_BM_ADD',

                    #Replacement and Drop
                    np.where( (dm0[c1] < dm0[c2]), dm0[a].apply(str)+'_BM_SWAP,'+dm0[dla].apply(str)+'_BM_DROP',

                    "OTHER")))))))))))))))



#Recode Board All Change Events [Make Change Event List]
dm0 = dm0.apply(recode_events, simple = True, axis=1)




#################################################################
#Need Board Partisanship Overall Measures
#################################################################

#***All needs to occur on df prior to bm lag and drop na
#since we are lagging again, needs to be on initial df
dm1 = dm.copy()


#Fullname and Party Columns
fn = 'fullname_clean_pure'
pv = 'party'




#################################################################
#Need Board Party Change Metrics
#################################################################


def get_party_change_cols(name_key, party_col, df_in):

    dm1 = df_in.copy()


    #Fullname and Party Columns
    fn = name_key
    pv = party_col

    #Set Outcols



    #Make Base Dict Col
    dm1 = dm1.apply(make_row_dict, name_key = fn, party_val = pv, axis=1)


    #Get Yearly Board Member, Party Dict
    c = 'name_party'
    gb = ['ticker', 'year']
    tmp = dm1.groupby(gb)[c].apply(list).apply(c_dict)
    tmp = tmp.reset_index(name='bp_dict')

    #Get Lagged Board List (By Company)
    tmp['prior_bp_dict'] = tmp.groupby(['ticker'])['bp_dict'].shift(1)

    #Get Board Party Change Results
    tmp = tmp.dropna(subset=['prior_bp_dict'])

    #Add Yearly Board Party and Lagged Dicts
    dm1 = dm1.merge(tmp)
    dm1 = dm1.drop(['name_party'], axis=1)

    #Combine Before Calculating Metrics
    df = dm0.merge(dm1)

    df = df.apply(get_party_bm_change, party_col = pv, axis=1)

    #Drop Extra Columns
    df = df.drop(['bp_dict', 'prior_bp_dict'], axis=1)

    #TODO
    #Rename Dict Columns with PV, vs Drop

    return df.astype(str)


#Fullname and Party Columns
#dm1 = dm.copy()
fn = 'fullname_clean_pure'
pv = 'party'

#Get Party Change with Original Party Variable
df1 = get_party_change_cols(fn, pv, dm)
print(df1.columns)
#df = df.astype(str)

#Get Party Change with Imputed Party Variable
pv = 'pid2ni_med_str'
df2 = get_party_change_cols(fn, pv, dm)
print(df2.columns)

#Combine
df = df1.merge(df2)
print(df.columns)




#Convert to Company, Year Data
df = df.astype(str)
df = df.drop_duplicates(subset=['cid_master', 'ticker', 'year'])


#Convert Change Events to Rows
change_cols = []
#change_cols.append(['board_change_events_list', ','])
change_cols.append(['new_bm_party', ','])
#change_cols.append(['dropped_bm_party', ','])
change_cols.append(['new_bm_pid2ni_med_str', ','])
#change_cols.append(['dropped_bm_pid2ni_med_str', ','])

print(change_cols)

#Do Events
change_cols = []
change_cols.append(['board_change_events_list', ','])
df = split_subjects_nvars(change_cols, df)

#Do Adds
change_cols = []
change_cols.append(['new_bm_party', ','])
change_cols.append(['new_bm_pid2ni_med_str', ','])
df = split_subjects_nvars(change_cols, df)

#Do Drops
change_cols = []
change_cols.append(['dropped_bm_party', ','])
change_cols.append(['dropped_bm_pid2ni_med_str', ','])
df = split_subjects_nvars(change_cols, df)

print(df)
df.to_csv("test_metrics.csv", index=False)


#################################################################
#TODO
#Unfold Party Change Lists, Change Events Into Rows
#[SWAP, DROP] | ['DEM'] | ['DEM', 'REP'] 
# -->
#SWAP | DEM | DEM
#DROP |     | REP

#################################################################


