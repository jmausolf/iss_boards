import pandas as pd
import numpy as np 


#F1000 List ID 
f1000 = pd.read_csv("fortune1000-list_id.csv")
f1000['cid_master'] = f1000['fec_company']

#FEC from CH1 - R 
fec = pd.read_csv("fec_cid_master.csv")
fec['found_fec'] = True

#Fortune 500 (2016) with Ticker
f500 = pd.read_csv("2016_fortune500_with_ticker.csv")
cols = ['rank', 'fec_company', 'ticker', 'revenue', 'website']
f500.columns = cols
#print(f500.columns)

#Merge FEC Extract and F1000 List Id
df = f1000.merge(fec, how = 'left')
df = df.sort_values(by='list_id')
df['ticker_alt'] = None
df['search_ticker'] = False


#Merge Existing F500 Tickers
df = df.merge(f500, how = 'left')
print(df.isna().sum())
#print(df.columns)
#print(df)
#print(df.isna().sum())

#Get ISS_id, ticker, cusip, company_name
iss = pd.read_csv("ISS_Boards.csv", low_memory=False, 
					usecols=['company_id', 'cusip',
							 'ticker'])
iss = iss.drop_duplicates()
iss.columns = ['iss_id', 'cusip', 'ticker']
#print(iss.shape)



#Make Missing Tickers Template
dfm = df.loc[df['found_fec'] == True]
dfm = dfm.loc[dfm['ticker'].isna()]
dfm.to_csv("missing_tickers.csv", index=False)
print(dfm.isna().sum())


#Import Found Missing Tickers
tk = pd.read_csv("MASTER_missing_tickers.csv")
tk['search_ticker'] = True
tk = tk.loc[tk['ticker'].notna()]
#print(tk.isna().sum())
#print(tk)
#print(tk.columns)


#Restrict DF to Those With Already Found Tickers
df['ticker_search'] = np.where((df['ticker'].isna() &
								df['found_fec'] == True), 
								True, False)

#print(df)
crit = (
			(df['ticker'].notna() &
			 df['found_fec'] == True)

		)

df1 = df.loc[crit]
print(df1.shape)
#df = df.loc[df['ticker_search'] == False]
#df = df.sort_values(by='list_id')
#print(df)

#Add Iss Columns
df1 = df1.merge(iss, how = 'left', on = 'ticker')
df2 = df.loc[df['ticker_search'] == True]
print(df2.shape)
df = pd.concat([df1, df2], axis=0, sort=True)
print(df.shape)


#print(df)
print(df.isna().sum())


#Merge DF with Found Tickers
df = df.merge(tk, how = 'left',
				on = ['fec_company', 'list_id',
					  'found_fec', 'rank',
					  'revenue', 'website'])
df['ticker'] = df['ticker_y'].fillna(df['ticker_x'])
df['ticker_alt'] = df['ticker_alt_y'].fillna(df['ticker_alt_x'])
df['cusip'] = df['cusip_y'].fillna(df['cusip_x'])
df['search_ticker'] = df['search_ticker_y'].fillna(df['search_ticker_x'])
df['cid_master'] = df['cid_master_x']



df = df.drop(['ticker_x', 'ticker_y',
		 	  'ticker_alt_x', 'ticker_alt_y',
		 	  'search_ticker_x', 'search_ticker_y',
		 	  'cid_master_x', 'cid_master_y',
		 	  'cusip_x', 'cusip_y'], axis=1)

print(df.columns)
df = df[['list_id', 'fec_company', 'cid_master', 'iss_id',
		'ticker', 'ticker_alt', 'cusip',
		 'found_fec', 'search_ticker']]
'''
#df['ticker'] = df['ticker_y'].fillna(df['ticker_x'])
'''

#Data with Multiple CUSIP Values
df = df.loc[df['found_fec'] == True]
print(df.isna().sum())
print(df.shape)
df.to_csv("f400_linked_cusip_dupes.csv", index=False)

#Data with Only First CUISP Value
df = df.drop_duplicates(subset=['list_id', 'ticker'])
print(df.isna().sum())
print(df.shape)
df.to_csv("f400_linked_unique.csv", index=False)
#df.to_csv("_linked_file.csv", index=False)

'''
#Add Missing Tickers
#df = pd.concat([df, tk], axis=0)

#Drop Previously Missing Cases
#df = 
#print(df)

#Check Progress
#dfn = df.loc[df['found_fec'] == True]
#dfn = dfn.loc[dfn['ticker'].isna()]


#print(df)
#print(dfn.isna().sum())
'''

