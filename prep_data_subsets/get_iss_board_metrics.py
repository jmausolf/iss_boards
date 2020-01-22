import pandas as pd 
import numpy as np 
import ast

from collections import Counter 
from collections import ChainMap

#################################################################
# Set Options
#################################################################

infile = '../data/ISS/post_join_drop_ISS_select.csv'
outfile = '../data/ISS/ISS_board_change_analysis.csv'
fullname_var = 'fullname_clean_pure'

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


def make_str_bp_col(party_var, df):

    p = party_var
    bp = 'bp_{}'.format(p)
    df[bp] = np.where(df[p] < 0, "DEM",
                np.where(df[p] >= 0, "REP", None))
    return df


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


def get_party_change_cols(name_key, party_col, df_in):

    dm1 = df_in.copy()

    #Fullname and Party Columns
    fn = name_key
    pv = party_col

    #Set Outcols
    bpd = 'bp_dict_{}'.format(pv)
    pbpd = 'prior_bp_dict_{}'.format(pv)


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

    #Rename Dict Columns using Party Value
    df.rename(columns={'bp_dict': bpd,
                       'prior_bp_dict': pbpd}, inplace=True)

    return df.astype(str)


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


def val_iter(val, c, sep='.'):
    n = c+1
    val = '{}{}{}'.format(val, sep, n)
    return val


def extract_event_action_counts(row):

    col = 'board_change_events_list'
    e = row[col]

    try:

        #Get Event
        event = e.split('-')[0]

        #Get Action Count, Event Count
        if event == 'NO_CHANGE' or event == 'OTHER':
            ac = 1
            ec = int(e.split('-')[1])
            event = event
        else:
            ac = int(event.split('.')[1])
            ec = int(e.split('-')[1])
            event = event.split('.')[0]

    except:
        import pdb; pdb.set_trace()
        print(row)
        print(e)


    row[col] = event
    row['action_count'] = ac
    row['event_count'] = ec

    return row

def get_simple_event(i):

    if i == 'NO_CHANGE' or i == 'OTHER':
        return [i]
    else:
        #Split of N+ 
        if 'N_' in i:
            i = i.split('N_')[1]
        else:
            pass

        n = int(i.split('_', 1)[0])
        if '_SWAP' in i:
            v = 'SWAP'
            return [val_iter(v, x) for x in range(0, n)]
        if '_ADD' in i:
            v = 'ADD'
            return [val_iter(v, x) for x in range(0, n)]
        if '_DROP' in i:
            v = 'DROP'
            return [val_iter(v, x) for x in range(0, n)]
        else:
            return i


def recode_events(row, simple=True):

    #Out Col 
    o = 'board_change_events_list'
    n = 'total_board_events'

    #Get Column
    i = row['board_all_change_events']

    #Drop Spaces
    i = i.replace(r'\s', '').replace(' ', '')

    #Get Multiple Events
    s = i.split(',')

    if len(s) > 1:
        if simple is True:
            s0 = [get_simple_event(i) for i in s]
            l = flatten(s0)
        else:
            l = s

    else:
        if simple is True:
            i0 = get_simple_event(i)
            l = flatten(i0)
        else:
            l = [i]

    #Add Iteration Number to Full List
    c = len(l)
    l1 = [val_iter(x, y, sep='-') for x, y in zip(l, range(0, c))]

    row[o] = l1
    row[n] = len(row[o])
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

#Load Data
dm = pd.read_csv(infile, low_memory=False)
print('[*] loading dataframe {} : {}...'.format(infile, dm.shape))

#Drop Duplicates
dm = dm.drop_duplicates(subset=['ticker', 'year', fullname_var])

#Isolate Subset for Draft
#dm = dm.loc[(dm['cid_master'] == 'Air Products & Chemicals') | (dm['cid_master'] == 'Apple' )]
#dm = dm.loc[(dm['cid_master'] == 'Marathon Petroleum') | (dm['cid_master'] == 'Apple' ) | (dm['cid_master'] == 'Air Products & Chemicals' )]


dm = dm[['cid_master', 'ticker', 'year', 'cycle', fullname_var, 'party']]

#Make Copy with NA & Fill NA Party Values with UNK
dm['party_na'] = dm['party']
dm['party'] = dm['party'].fillna("UNK")

#################################################################
#Add Some Basic Metrics
#################################################################

#Add Yearly Board Size Column
gb = ['ticker', 'year']
tmp = dm.groupby(gb)[fullname_var].count().reset_index()
tmp.columns = ['ticker', 'year', 'board_size']
dm = dm.merge(tmp)


#################################################################
#Add Board Partisanship Overall Measures
#################################################################

print('[*] calculating board partisanship measures...')

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

#Combine data with imputed columns
dm = pd.concat([dm, tmp1, tmp2], axis=1)

#Add Yearly Board Size Column
gb = ['ticker', 'year']
tmp = dm.groupby(gb).agg({'pid2n' : ['mean', 'median'],
                          'pid2ni_mean' : ['mean', 'median'],
                          'pid2ni_med' : ['mean', 'median'],
                          'pid3n' : ['mean', 'median']

                          }).reset_index()

#Clean Column Names
cols = tmp.columns
clean_cols = [clean_col(c) for c in cols]
tmp.columns = clean_cols


#Add Board Party Columns
bp_cols = ['pid2n_mean', 'pid2n_median',
        'pid2ni_mean_mean', 'pid2ni_mean_median',
        'pid2ni_med_mean', 'pid2ni_med_median',
        'pid3n_mean', 'pid3n_median']

for c in bp_cols:
    tmp = make_str_bp_col(c, tmp)

#Merge Party Metrics
dm = dm.merge(tmp)



#################################################################
#Get Board Member Change Metrics
#################################################################

print('[*] calculating board member changes...')

#Get Yearly Board Member List
c = fullname_var
tmp = dm.groupby(gb)[c].apply(list).apply(lsort)
tmp = tmp.reset_index(name='board')

#Get Lagged Board List (By Company)
tmp['prior_board'] = tmp.groupby(['ticker'])['board'].shift(1)


#Get Board Change Results
tmp = tmp.dropna(subset=['prior_board'])
tmp =  tmp.apply(get_board_metrics, axis=1)

#Add Yearly Board Member Change Metrics
dm0 = dm.merge(tmp)

#################################################################
#Need Board Change Flags
#################################################################

c1 = 'new_bm_count'
c2 = 'dropped_bm_count'
dm0['net_added'] = dm0[c1] - dm0[c2]
dm0['net_added'] = dm0.net_added.astype(str)
dm0['net_dropped'] = dm0[c2] - dm0[c1]
dm0['net_dropped'] = dm0.net_dropped.astype(str)


a = 'new_bm_count'
d = 'dropped_bm_count'
ald = 'net_added'
dla = 'net_dropped'


dm0['board_net_change'] = np.where( ((dm0[c1] == 0) & (dm0[c2] == 0)), "NO_CHANGE",
                    np.where( ((dm0[c1] == dm0[c2]) & (dm0[c1] == 1)), "1_BM_SWAP",
                    np.where( ((dm0[c1] == dm0[c2]) & (dm0[c1] == 2)), "2_BM_SWAP",
                    np.where( ((dm0[c1] == dm0[c2]) & (dm0[c1] == 3)), "3_BM_SWAP",
                    np.where( ((dm0[c1] == dm0[c2]) & (dm0[c1] > 3)), dm0[c1].apply(str)+'_BM_SWAP',

                    np.where( ((dm0[c1] > dm0[c2]) & (dm0[c1] - dm0[c2] == 1)), "1_BM_ADD",
                    np.where( ((dm0[c1] > dm0[c2]) & (dm0[c1] - dm0[c2] == 2)), "2_BM_ADD",
                    np.where( ((dm0[c1] > dm0[c2]) & (dm0[c1] - dm0[c2] == 3)), "3_BM_ADD",
                    np.where( ((dm0[c1] > dm0[c2]) & (dm0[c1] - dm0[c2] > 3)), dm0[c1].apply(str)+'_BM_ADD',

                    np.where( ((dm0[c1] < dm0[c2]) & (dm0[c2] - dm0[c1] == 1)), "1_BM_DROP",
                    np.where( ((dm0[c1] < dm0[c2]) & (dm0[c2] - dm0[c1] == 2)), "2_BM_DROP",
                    np.where( ((dm0[c1] < dm0[c2]) & (dm0[c2] - dm0[c1] == 3)), "3_BM_DROP",
                    np.where( ((dm0[c1] < dm0[c2]) & (dm0[c2] - dm0[c1] > 3)), dm0[c2].apply(str)+'_BM_DROP',
                    "OTHER")))))))))))))


dm0['board_all_change'] = np.where( 

                    #No Change
                    ((dm0[c1] == 0) & (dm0[c2] == 0)), "NO_CHANGE",

                    #Equal Replacement
                    np.where( ((dm0[c1] == dm0[c2]) & (dm0[c1] == 1)), "1_BM_SWAP",
                    np.where( ((dm0[c1] == dm0[c2]) & (dm0[c1] == 2)), "2_BM_SWAP",
                    np.where( ((dm0[c1] == dm0[c2]) & (dm0[c1] == 3)), "3_BM_SWAP",
                    np.where( ((dm0[c1] == dm0[c2]) & (dm0[c1] > 3)), dm0[c1].apply(str)+'_BM_SWAP',

                    #Only Added
                    np.where( ((dm0[c1] > dm0[c2]) & (dm0[c2] == 0) & (dm0[c1] == 1)), "1_BM_ADD",
                    np.where( ((dm0[c1] > dm0[c2]) & (dm0[c2] == 0) & (dm0[c1] == 2)), "2_BM_ADD",
                    np.where( ((dm0[c1] > dm0[c2]) & (dm0[c2] == 0) & (dm0[c1] == 3)), "3_BM_ADD",
                    np.where( ((dm0[c1] > dm0[c2]) & (dm0[c2] == 0) & (dm0[c1] > 3)), dm0[c1].apply(str)+'_BM_ADD',

                    #Only Dropped
                    np.where( ((dm0[c1] < dm0[c2]) & (dm0[c1] == 0) & (dm0[c2] == 1)), "1_BM_DROP",
                    np.where( ((dm0[c1] < dm0[c2]) & (dm0[c1] == 0) & (dm0[c2] == 2)), "2_BM_DROP",
                    np.where( ((dm0[c1] < dm0[c2]) & (dm0[c1] == 0) & (dm0[c2] == 3)), "3_BM_DROP",
                    np.where( ((dm0[c1] < dm0[c2]) & (dm0[c1] == 0) & (dm0[c2] > 3)), dm0[c2].apply(str)+'_BM_DROP',

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
                    np.where( ((dm0[c1] == dm0[c2]) & (dm0[c1] > 3)), dm0[c1].apply(str)+'_BM_SWAP',

                    #Only Added
                    np.where( ((dm0[c1] > dm0[c2]) & (dm0[c2] == 0) & (dm0[c1] == 1)), "1_BM_ADD",
                    np.where( ((dm0[c1] > dm0[c2]) & (dm0[c2] == 0) & (dm0[c1] == 2)), "2_BM_ADD",
                    np.where( ((dm0[c1] > dm0[c2]) & (dm0[c2] == 0) & (dm0[c1] == 3)), "3_BM_ADD",
                    np.where( ((dm0[c1] > dm0[c2]) & (dm0[c2] == 0) & (dm0[c1] > 3)), dm0[c1].apply(str)+'_BM_ADD',

                    #Only Dropped
                    np.where( ((dm0[c1] < dm0[c2]) & (dm0[c1] == 0) & (dm0[c2] == 1)), "1_BM_DROP",
                    np.where( ((dm0[c1] < dm0[c2]) & (dm0[c1] == 0) & (dm0[c2] == 2)), "2_BM_DROP",
                    np.where( ((dm0[c1] < dm0[c2]) & (dm0[c1] == 0) & (dm0[c2] == 3)), "3_BM_DROP",
                    np.where( ((dm0[c1] < dm0[c2]) & (dm0[c1] == 0) & (dm0[c2] > 3)), dm0[c2].apply(str)+'_BM_DROP',

                    #Replacement and Add
                    np.where( (dm0[c1] > dm0[c2]), dm0[d].apply(str)+'_BM_SWAP,'+dm0[ald].apply(str)+'_BM_ADD',

                    #Replacement and Drop
                    np.where( (dm0[c1] < dm0[c2]), dm0[a].apply(str)+'_BM_SWAP,'+dm0[dla].apply(str)+'_BM_DROP',

                    "OTHER")))))))))))))))



#Recode Board All Change Events [Make Change Event List]
dm0 = dm0.apply(recode_events, simple = True, axis=1)


#################################################################
#Need Board Party Change Metrics
#################################################################

print('[*] calculating board member party changes...')

#Make Copy of Data
dm1 = dm.copy()

#Fullname and Party Columns
fn = fullname_var
pv = 'party'

#Get Party Change with Original Party Variable
df1 = get_party_change_cols(fn, pv, dm)

#Get Party Change with Imputed Party Variable
pv = 'pid2ni_med_str'
df2 = get_party_change_cols(fn, pv, dm)

#Combine
df = df1.merge(df2)

#Convert to Company, Year Data
df = df.astype(str)
df = df.drop_duplicates(subset=['cid_master', 'ticker', 'year'])

#Drop Non-Board-Level Cols
drop_cols = [fullname_var, 'party', 'party_na',
             'pid3n', 'pid2n', 'pid2ni_mean', 
             'pid2ni_med', 'pid2ni_med_str']
df = df.drop(drop_cols, axis=1)

#df.to_csv("test_base_test_metrics.csv", index=False)

#################################################################
#Convert Multi-Change Events to Event Rows
#################################################################

#df = pd.read_csv("test_base_test_metrics.csv")

print('[*] converting compound events to rows...')

#make duplicate cols of originals
df['cp_board_change_events_list'] = df['board_change_events_list']
df['cp_new_bm_pid2ni_med_str'] = df['new_bm_pid2ni_med_str']
df['cp_dropped_bm_pid2ni_med_str'] = df['dropped_bm_pid2ni_med_str']
df['cp_new_bm_party'] = df['new_bm_party']
df['cp_dropped_bm_party'] = df['dropped_bm_party']

print(df.shape)

#Do Events
change_cols = []
change_cols.append(['board_change_events_list', ','])
df = split_subjects_nvars(change_cols, df)


#Extract Event Action Codes
df = df.apply(extract_event_action_counts, axis=1)

print(df)





def recode_add_drop_events(row, events, event_count, add_col, drop_col):

    e = events
    c = event_count
    a = add_col
    d = drop_col

    #Get Add, Drop Lists
    la = ast.literal_eval(row[a])
    ld = ast.literal_eval(row[d])

    #Get Index Number
    n = int(row[c])
    i = n-1

    if row[e] == 'NO_CHANGE' or row[e] == 'OTHER':
        row[a] = None
        row[d] = None

    if 'ADD' in row[e]:
        row[a] = la[i]
        row[d] = None

    if 'DROP' in row[e]:
        row[d] = ld[i]
        row[a] = None

    if 'SWAP' in row[e]:
        row[a] = la[i]
        row[d] = ld[i]

    return row

e = 'board_change_events_list'
c = 'event_count'
a = 'new_bm_party'
d = 'dropped_bm_party'
df = df.apply(recode_add_drop_events, events = e, event_count = c, add_col = a, drop_col = d, axis=1)


a = 'new_bm_pid2ni_med_str'
d = 'dropped_bm_pid2ni_med_str'
df = df.apply(recode_add_drop_events, events = e, event_count = c, add_col = a, drop_col = d, axis=1)

'''
df = df[['cid_master', 'ticker', 'year',
       'cp_board_change_events_list', 'cp_new_bm_party', 'cp_dropped_bm_party',
       'new_bm_party', 'dropped_bm_party',
       'cp_new_bm_pid2ni_med_str', 'cp_dropped_bm_pid2ni_med_str',
       'new_bm_pid2ni_med_str', 'dropped_bm_pid2ni_med_str',
       'board_change_events_list']]
'''

#df.to_csv('test_events.csv', index=False)




#################################################################
#Add Matching Columns
#################################################################

print('[*] coding results...')

#Key Cols, Abbreviations

e = 'board_change_events_list'

#BP Party NA (pid2n)
bp1a = 'bp_pid2n_mean' 
bp1b = 'bp_pid2n_median'

#BP Party NA (pid2n imputed)
bp2a = 'bp_pid2ni_med_mean'
bp2b = 'bp_pid2ni_med_median'

a1 = 'new_bm_party'
a2 = 'new_bm_pid2ni_med_str'

d1 = 'dropped_bm_party'
d2 = 'dropped_bm_pid2ni_med_str'

ae = ['SWAP', 'ADD']
de = ['DROP']

##########################################
#Make Equal Swap Columns
##########################################


c = 'equal_swap_party'
df[c] = np.where( ((df[e] == "SWAP") & (df[a1] == df[d1])), "YES",
            np.where( ((df[e] == "SWAP") & (df[a1] != df[d1])), "NO", None))

c = 'equal_swap_pid2ni_med'
df[c] = np.where( ((df[e] == "SWAP") & (df[a2] == df[d2])), "YES",
            np.where( ((df[e] == "SWAP") & (df[a2] != df[d2])), "NO", None))



##########################################
#Make Event Match Columns
#Get Event Match (Partisan Expectation) 
#1. For Swap/Add, 2. Drops

c = 'event_match_party1a'
df[c] = np.where(     ((df[e].isin(ae)) & (df[a1] == df[bp1a])), "YES",
            np.where( ((df[e].isin(ae)) & (df[a1] != df[bp1a])), "NO",
            np.where( ((df[e].isin(de)) & (df[d1] != df[bp1a])), "YES",
            np.where( ((df[e].isin(de)) & (df[d1] == df[bp1a])), "NO", None))))

c = 'event_match_party1b'
df[c] = np.where(     ((df[e].isin(ae)) & (df[a1] == df[bp1b])), "YES",
            np.where( ((df[e].isin(ae)) & (df[a1] != df[bp1b])), "NO",
            np.where( ((df[e].isin(de)) & (df[d1] != df[bp1b])), "YES",
            np.where( ((df[e].isin(de)) & (df[d1] == df[bp1b])), "NO", None))))


c = 'event_match_pid2ni_med2a'
df[c] = np.where(     ((df[e].isin(ae)) & (df[a2] == df[bp2a])), "YES",
            np.where( ((df[e].isin(ae)) & (df[a2] != df[bp2a])), "NO",
            np.where( ((df[e].isin(de)) & (df[d2] != df[bp2a])), "YES",
            np.where( ((df[e].isin(de)) & (df[d2] == df[bp2a])), "NO", None))))

c = 'event_match_pid2ni_med2b'
df[c] = np.where(     ((df[e].isin(ae)) & (df[a2] == df[bp2b])), "YES",
            np.where( ((df[e].isin(ae)) & (df[a2] != df[bp2b])), "NO",
            np.where( ((df[e].isin(de)) & (df[d2] != df[bp2b])), "YES",
            np.where( ((df[e].isin(de)) & (df[d2] == df[bp2b])), "NO", None))))


##########################################
#Make Partisan Match Columns
#(Simple Partisan Matching) 
#1. For Swap/Add, 2. Drops

c = 'partisan_match_party1a'
df[c] = np.where(     ((df[e].isin(ae)) & (df[a1] == df[bp1a])), "YES",
            np.where( ((df[e].isin(ae)) & (df[a1] != df[bp1a])), "NO",
            np.where( ((df[e].isin(de)) & (df[d1] == df[bp1a])), "YES",
            np.where( ((df[e].isin(de)) & (df[d1] != df[bp1a])), "NO", None))))

c = 'partisan_match_party1b'
df[c] = np.where(     ((df[e].isin(ae)) & (df[a1] == df[bp1b])), "YES",
            np.where( ((df[e].isin(ae)) & (df[a1] != df[bp1b])), "NO",
            np.where( ((df[e].isin(de)) & (df[d1] == df[bp1b])), "YES",
            np.where( ((df[e].isin(de)) & (df[d1] != df[bp1b])), "NO", None))))


c = 'partisan_match_pid2ni_med2a'
df[c] = np.where(     ((df[e].isin(ae)) & (df[a2] == df[bp2a])), "YES",
            np.where( ((df[e].isin(ae)) & (df[a2] != df[bp2a])), "NO",
            np.where( ((df[e].isin(de)) & (df[d2] == df[bp2a])), "YES",
            np.where( ((df[e].isin(de)) & (df[d2] != df[bp2a])), "NO", None))))

c = 'partisan_match_pid2ni_med2b'
df[c] = np.where(     ((df[e].isin(ae)) & (df[a2] == df[bp2b])), "YES",
            np.where( ((df[e].isin(ae)) & (df[a2] != df[bp2b])), "NO",
            np.where( ((df[e].isin(de)) & (df[d2] == df[bp2b])), "YES",
            np.where( ((df[e].isin(de)) & (df[d2] != df[bp2b])), "NO", None))))



print(df)
print(df.columns)
print('[*] saving result {} : {}...'.format(outfile, df.shape))
df.to_csv(outfile, index=False)
df.to_csv("test_metrics.csv", index=False)



