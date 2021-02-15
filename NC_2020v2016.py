# Import modules
import pandas as pd
import numpy as np
pd.options.mode.chained_assignment = None #hide SettingWithCopyWarning


########## 2016 ##########

# Registrants (registered voters in 2016)
Reg_data_2016 = pd.read_csv('https://s3.amazonaws.com/dl.ncsbe.gov/ENRS/2016_11_08/voter_stats_20161108.zip', sep='\t')
Reg_data_2016['party_cd'] = Reg_data_2016['party_cd'].str.replace('DEM','reg_DEM')
Reg_data_2016['party_cd'] = Reg_data_2016['party_cd'].str.replace('REP','reg_REP')
Reg_data_2016['party_cd'] = Reg_data_2016['party_cd'].str.replace('UNA','reg_Other')
Reg_data_2016['party_cd'] = Reg_data_2016['party_cd'].str.replace('LIB','reg_Other')
Reg_data_2016_table2 = pd.pivot_table(Reg_data_2016, values='total_voters', index=['county_desc'], columns=['party_cd'], aggfunc=np.sum)
Reg_data_2016_table3 = pd.pivot_table(Reg_data_2016, values='total_voters', index=['county_desc'], columns=['election_date'], aggfunc=np.sum)
Reg_data_2016_table = pd.merge(Reg_data_2016_table2, Reg_data_2016_table3, on=['county_desc'])
Reg_data_2016_table = pd.DataFrame(Reg_data_2016_table.to_records()) #Flatten pivot table into dataframe
Reg_data_2016_table = Reg_data_2016_table.rename(columns={'11/08/2016':'reg_Total'})

# Voters (overall turnout in 2016 including election day and AB/EV)
Turnout_data_2016 = pd.read_csv('https://s3.amazonaws.com/dl.ncsbe.gov/ENRS/2016_11_08/history_stats_20161108.zip', sep='\t')
Turnout_data_2016['party_cd'] = Turnout_data_2016['party_cd'].str.replace('DEM','turn_DEM')
Turnout_data_2016['party_cd'] = Turnout_data_2016['party_cd'].str.replace('REP','turn_REP')
Turnout_data_2016['party_cd'] = Turnout_data_2016['party_cd'].str.replace('UNA','turn_Other')
Turnout_data_2016['party_cd'] = Turnout_data_2016['party_cd'].str.replace('LIB','turn_Other')
Turnout_data_2016_table2 = pd.pivot_table(Turnout_data_2016, values='total_voters', index=['county_desc'], columns=['party_cd'], aggfunc=np.sum)
Turnout_data_2016_table3 = pd.pivot_table(Turnout_data_2016, values='total_voters', index=['county_desc'], columns=['election_date'], aggfunc=np.sum)
Turnout_data_2016_table = pd.merge(Turnout_data_2016_table2, Turnout_data_2016_table3, on=['county_desc'])
Turnout_data_2016_table = pd.DataFrame(Turnout_data_2016_table.to_records()) #Flatten pivot table into dataframe
Turnout_data_2016_table = Turnout_data_2016_table.rename(columns={'11/08/2016':'turn_Total'})

# Absentees (AB or EV ballots cast in 2016)
AB_data_2016 = pd.read_csv('https://s3.amazonaws.com/dl.ncsbe.gov/ENRS/2016_11_08/absentee_counts_county_20161108.csv', header=None)
AB_data_2016.columns = ['county_desc', 'voting_method_desc', 'party_cd', 'sex_code', 'race_code', 'total_voters'] 
AB_data_2016['party_cd'] = AB_data_2016['party_cd'].str.replace('DEM','ab_DEM')
AB_data_2016['party_cd'] = AB_data_2016['party_cd'].str.replace('REP','ab_REP')
AB_data_2016['party_cd'] = AB_data_2016['party_cd'].str.replace('UNA','ab_Other')
AB_data_2016['party_cd'] = AB_data_2016['party_cd'].str.replace('LIB','ab_Other')
AB_data_2016_table2 = pd.pivot_table(AB_data_2016, values='total_voters', index=['county_desc'], columns=['party_cd'], aggfunc=np.sum)
AB_data_2016_table3 = pd.pivot_table(AB_data_2016, values='total_voters', index=['county_desc'], aggfunc=np.sum)
AB_data_2016_table = pd.merge(AB_data_2016_table2, AB_data_2016_table3, on=['county_desc'])
AB_data_2016_table = pd.DataFrame(AB_data_2016_table.to_records()) #Flatten pivot table into dataframe
AB_data_2016_table = AB_data_2016_table.rename(columns={'total_voters':'ab_Total'})

# Merge Registration, Turnout, & AB tables by county name
Data_2016 = pd.merge(Reg_data_2016_table, Turnout_data_2016_table, on=['county_desc'])
Data_2016 = pd.merge(Data_2016, AB_data_2016_table, on=['county_desc'])

# Breakdown counties by urban, suburban, or rural, based on population size
top4_2016 = Data_2016.loc[(Data_2016['county_desc'] == 'WAKE') | (Data_2016['county_desc'] == 'GUILFORD') | (Data_2016['county_desc'] == 'MECKLENBURG') | (Data_2016['county_desc'] == 'FORSYTH')]
top4_2016.loc['Urban4',1:] = top4_2016.sum(axis=0)
top4_2016.drop(top4_2016.head(4).index,inplace=True)

mid16_2016 = Data_2016.loc[(Data_2016['county_desc'] == 'ALAMANCE') |
						(Data_2016['county_desc'] == 'BUNCOMBE') |
						(Data_2016['county_desc'] == 'CABARRUS') |
						(Data_2016['county_desc'] == 'CATAWBA') |
						(Data_2016['county_desc'] == 'CUMBERLAND') |
						(Data_2016['county_desc'] == 'DAVIDSON') |
						(Data_2016['county_desc'] == 'DURHAM') |
						(Data_2016['county_desc'] == 'GASTON') |
						(Data_2016['county_desc'] == 'IREDELL') |
						(Data_2016['county_desc'] == 'JOHNSTON') |
						(Data_2016['county_desc'] == 'NEW HANOVER') |
						(Data_2016['county_desc'] == 'ONSLOW') |
						(Data_2016['county_desc'] == 'ORANGE') |
						(Data_2016['county_desc'] == 'PITT') |
						(Data_2016['county_desc'] == 'UNION') |
						(Data_2016['county_desc'] == 'WATAUGA')]
mid16_2016.loc['Suburban16',1:] = mid16_2016.sum(axis=0)
mid16_2016.drop(mid16_2016.head(16).index,inplace=True)

bottom80_2016 = Data_2016.loc[(Data_2016['county_desc'] != 'ALAMANCE') &
						(Data_2016['county_desc'] != 'BUNCOMBE') &
						(Data_2016['county_desc'] != 'CABARRUS') &
						(Data_2016['county_desc'] != 'CATAWBA') &
						(Data_2016['county_desc'] != 'CUMBERLAND') &
						(Data_2016['county_desc'] != 'DAVIDSON') &
						(Data_2016['county_desc'] != 'DURHAM') &
						(Data_2016['county_desc'] != 'GASTON') &
						(Data_2016['county_desc'] != 'IREDELL') &
						(Data_2016['county_desc'] != 'JOHNSTON') &
						(Data_2016['county_desc'] != 'NEW HANOVER') &
						(Data_2016['county_desc'] != 'ONSLOW') &
						(Data_2016['county_desc'] != 'ORANGE') &
						(Data_2016['county_desc'] != 'PITT') &
						(Data_2016['county_desc'] != 'UNION') &
						(Data_2016['county_desc'] != 'WATAUGA') &
						(Data_2016['county_desc'] != 'WAKE') &
						(Data_2016['county_desc'] != 'MECKLENBURG') &
						(Data_2016['county_desc'] != 'GUILFORD') &
						(Data_2016['county_desc'] != 'FORSYTH')]
bottom80_2016.loc['Rural80',1:] = bottom80_2016.sum(axis=0)
bottom80_2016.drop(bottom80_2016.head(80).index,inplace=True)

#Combine urban, suburban, rural dataframes
frames = [top4_2016, mid16_2016, bottom80_2016]
geo2016 = pd.concat(frames)
geo2016.loc['Statewide',1:] = geo2016.sum(axis=0)
newcol = ['Urban4', 'Suburban16', 'Rural80', 'Statewide']
geo2016['county_desc'] = newcol
geo2016 = geo2016.reset_index()
del geo2016['index']

# Statewide totals for each column in county breakdown
Data_2016.loc['Statewide',1:] = Data_2016.sum(axis=0)
Data_2016['county_desc'] = Data_2016['county_desc'].replace(np.nan, 'Statewide', regex=True)
Data_2016 = Data_2016.reset_index()
del Data_2016['index']

# Calculated fields for county breakdown
Data_2016['DEM%_of_registrants'] = (100 * Data_2016['reg_DEM'] / Data_2016['reg_Total']).round(2)
Data_2016['REP%_of_registrants'] = (100 * Data_2016['reg_REP'] / Data_2016['reg_Total']).round(2)
Data_2016['Other%_of_registrants'] = (100 * Data_2016['reg_Other'] / Data_2016['reg_Total']).round(2)
Data_2016['%DEM_voting'] = (100 * Data_2016['turn_DEM'] / Data_2016['reg_DEM']).round(2)
Data_2016['%REP_voting'] = (100 * Data_2016['turn_REP'] / Data_2016['reg_REP']).round(2)
Data_2016['%Other_voting'] = (100 * Data_2016['turn_Other'] / Data_2016['reg_Other']).round(2)
Data_2016['DEM%_of_AB'] = (100 * Data_2016['ab_DEM'] / Data_2016['ab_Total']).round(2)
Data_2016['REP%_of_AB'] = (100 * Data_2016['ab_REP'] / Data_2016['ab_Total']).round(2)
Data_2016['Other%_of_AB'] = (100 * Data_2016['ab_Other'] / Data_2016['ab_Total']).round(2)
Data_2016['DEM%_of_votes'] = (100 * Data_2016['turn_DEM'] / Data_2016['turn_Total']).round(2)
Data_2016['REP%_of_votes'] = (100 * Data_2016['turn_REP'] / Data_2016['turn_Total']).round(2)
Data_2016['Other%_of_votes'] = (100 * Data_2016['turn_Other'] / Data_2016['turn_Total']).round(2)
Data_2016['DEM_votes%-reg%'] = Data_2016['DEM%_of_votes'] - Data_2016['DEM%_of_registrants']
Data_2016['REP_votes%-reg%'] = Data_2016['REP%_of_votes'] - Data_2016['REP%_of_registrants'] 
Data_2016['Other_votes%-reg%'] = Data_2016['Other%_of_votes'] - Data_2016['Other%_of_registrants'] 

# Calculated fields for geographic breakdown
geo2016['DEM%_of_registrants'] = (100 * geo2016['reg_DEM'] / geo2016['reg_Total']).round(2)
geo2016['REP%_of_registrants'] = (100 * geo2016['reg_REP'] / geo2016['reg_Total']).round(2)
geo2016['Other%_of_registrants'] = (100 * geo2016['reg_Other'] / geo2016['reg_Total']).round(2)
geo2016['%DEM_voting'] = (100 * geo2016['turn_DEM'] / geo2016['reg_DEM']).round(2)
geo2016['%REP_voting'] = (100 * geo2016['turn_REP'] / geo2016['reg_REP']).round(2)
geo2016['%Other_voting'] = (100 * geo2016['turn_Other'] / geo2016['reg_Other']).round(2)
geo2016['DEM%_of_AB'] = (100 * geo2016['ab_DEM'] / geo2016['ab_Total']).round(2)
geo2016['REP%_of_AB'] = (100 * geo2016['ab_REP'] / geo2016['ab_Total']).round(2)
geo2016['Other%_of_AB'] = (100 * geo2016['ab_Other'] / geo2016['ab_Total']).round(2)
geo2016['DEM%_of_votes'] = (100 * geo2016['turn_DEM'] / geo2016['turn_Total']).round(2)
geo2016['REP%_of_votes'] = (100 * geo2016['turn_REP'] / geo2016['turn_Total']).round(2)
geo2016['Other%_of_votes'] = (100 * geo2016['turn_Other'] / geo2016['turn_Total']).round(2)
geo2016['DEM_votes%-reg%'] = geo2016['DEM%_of_votes'] - geo2016['DEM%_of_registrants']
geo2016['REP_votes%-reg%'] = geo2016['REP%_of_votes'] - geo2016['REP%_of_registrants'] 
geo2016['Other_votes%-reg%'] = geo2016['Other%_of_votes'] - geo2016['Other%_of_registrants']



########## 2020 ##########

# Registrants (registered voters in 2020)
Reg_data_2020 = pd.read_csv('https://s3.amazonaws.com/dl.ncsbe.gov/ENRS/2020_11_03/voter_stats_20201103.zip', sep='\t')
Reg_data_2020['party_cd'] = Reg_data_2020['party_cd'].str.replace('DEM','reg_DEM')
Reg_data_2020['party_cd'] = Reg_data_2020['party_cd'].str.replace('REP','reg_REP')
Reg_data_2020['party_cd'] = Reg_data_2020['party_cd'].str.replace('UNA','reg_Other')
Reg_data_2020['party_cd'] = Reg_data_2020['party_cd'].str.replace('LIB','reg_Other')
Reg_data_2020['party_cd'] = Reg_data_2020['party_cd'].str.replace('CST','reg_Other')
Reg_data_2020['party_cd'] = Reg_data_2020['party_cd'].str.replace('GRE','reg_Other')
Reg_data_2020_table2 = pd.pivot_table(Reg_data_2020, values='total_voters', index=['county_desc'], columns=['party_cd'], aggfunc=np.sum)
Reg_data_2020_table3 = pd.pivot_table(Reg_data_2020, values='total_voters', index=['county_desc'], columns=['election_date'], aggfunc=np.sum)
Reg_data_2020_table = pd.merge(Reg_data_2020_table2, Reg_data_2020_table3, on=['county_desc'])
Reg_data_2020_table = pd.DataFrame(Reg_data_2020_table.to_records()) #Flatten pivot table into dataframe
Reg_data_2020_table = Reg_data_2020_table.rename(columns={'11/03/2020':'reg_Total'})

# Voters (overall turnout in 2020 including election day and AB/EV)
Turnout_data_2020 = pd.read_csv('https://s3.amazonaws.com/dl.ncsbe.gov/ENRS/2020_11_03/history_stats_20201103.zip', sep='\t')
Turnout_data_2020['party_cd'] = Turnout_data_2020['party_cd'].str.replace('DEM','turn_DEM')
Turnout_data_2020['party_cd'] = Turnout_data_2020['party_cd'].str.replace('REP','turn_REP')
Turnout_data_2020['party_cd'] = Turnout_data_2020['party_cd'].str.replace('UNA','turn_Other')
Turnout_data_2020['party_cd'] = Turnout_data_2020['party_cd'].str.replace('LIB','turn_Other')
Turnout_data_2020['party_cd'] = Turnout_data_2020['party_cd'].str.replace('CST','turn_Other')
Turnout_data_2020['party_cd'] = Turnout_data_2020['party_cd'].str.replace('GRE','turn_Other')
Turnout_data_2020_table2 = pd.pivot_table(Turnout_data_2020, values='total_voters', index=['county_desc'], columns=['party_cd'], aggfunc=np.sum)
Turnout_data_2020_table3 = pd.pivot_table(Turnout_data_2020, values='total_voters', index=['county_desc'], columns=['election_date'], aggfunc=np.sum)
Turnout_data_2020_table = pd.merge(Turnout_data_2020_table2, Turnout_data_2020_table3, on=['county_desc'])
Turnout_data_2020_table = pd.DataFrame(Turnout_data_2020_table.to_records()) #Flatten pivot table into dataframe
Turnout_data_2020_table = Turnout_data_2020_table.rename(columns={'11/03/2020':'turn_Total'})

# Absentees (AB or EV ballots cast in 2020)
AB_data_2020 = pd.read_csv('https://s3.amazonaws.com/dl.ncsbe.gov/ENRS/2020_11_03/absentee_counts_county_20201103.csv', header=None)
AB_data_2020.columns = ['county_desc', 'voting_method_desc', 'party_cd', 'sex_code', 'race_code', 'total_voters'] 
AB_data_2020['party_cd'] = AB_data_2020['party_cd'].str.replace('DEM','ab_DEM')
AB_data_2020['party_cd'] = AB_data_2020['party_cd'].str.replace('REP','ab_REP')
AB_data_2020['party_cd'] = AB_data_2020['party_cd'].str.replace('UNA','ab_Other')
AB_data_2020['party_cd'] = AB_data_2020['party_cd'].str.replace('LIB','ab_Other')
AB_data_2020['party_cd'] = AB_data_2020['party_cd'].str.replace('CST','ab_Other')
AB_data_2020['party_cd'] = AB_data_2020['party_cd'].str.replace('GRE','ab_Other')
AB_data_2020_table2 = pd.pivot_table(AB_data_2020, values='total_voters', index=['county_desc'], columns=['party_cd'], aggfunc=np.sum)
AB_data_2020_table3 = pd.pivot_table(AB_data_2020, values='total_voters', index=['county_desc'], aggfunc=np.sum)
AB_data_2020_table = pd.merge(AB_data_2020_table2, AB_data_2020_table3, on=['county_desc'])
AB_data_2020_table = pd.DataFrame(AB_data_2020_table.to_records()) #Flatten pivot table into dataframe
AB_data_2020_table = AB_data_2020_table.rename(columns={'total_voters':'ab_Total'})


# Merge Registration, Turnout, & AB tables by county name
Data_2020 = pd.merge(Reg_data_2020_table, Turnout_data_2020_table, on=['county_desc'])
Data_2020 = pd.merge(Data_2020, AB_data_2020_table, on=['county_desc'])

# Breakdown counties by urban, suburban, or rural, based on population size
top4_2020 = Data_2020.loc[(Data_2020['county_desc'] == 'WAKE') | (Data_2020['county_desc'] == 'GUILFORD') | (Data_2020['county_desc'] == 'MECKLENBURG') | (Data_2020['county_desc'] == 'FORSYTH')]
top4_2020.loc['Urban4',1:] = top4_2020.sum(axis=0)
top4_2020.drop(top4_2020.head(4).index,inplace=True)

mid16_2020 = Data_2020.loc[(Data_2020['county_desc'] == 'ALAMANCE') |
						(Data_2020['county_desc'] == 'BUNCOMBE') |
						(Data_2020['county_desc'] == 'CABARRUS') |
						(Data_2020['county_desc'] == 'CATAWBA') |
						(Data_2020['county_desc'] == 'CUMBERLAND') |
						(Data_2020['county_desc'] == 'DAVIDSON') |
						(Data_2020['county_desc'] == 'DURHAM') |
						(Data_2020['county_desc'] == 'GASTON') |
						(Data_2020['county_desc'] == 'IREDELL') |
						(Data_2020['county_desc'] == 'JOHNSTON') |
						(Data_2020['county_desc'] == 'NEW HANOVER') |
						(Data_2020['county_desc'] == 'ONSLOW') |
						(Data_2020['county_desc'] == 'ORANGE') |
						(Data_2020['county_desc'] == 'PITT') |
						(Data_2020['county_desc'] == 'UNION') |
						(Data_2020['county_desc'] == 'WATAUGA')]
mid16_2020.loc['Suburban16',1:] = mid16_2020.sum(axis=0)
mid16_2020.drop(mid16_2020.head(16).index,inplace=True)

bottom80_2020 = Data_2020.loc[(Data_2020['county_desc'] != 'ALAMANCE') &
						(Data_2020['county_desc'] != 'BUNCOMBE') &
						(Data_2020['county_desc'] != 'CABARRUS') &
						(Data_2020['county_desc'] != 'CATAWBA') &
						(Data_2020['county_desc'] != 'CUMBERLAND') &
						(Data_2020['county_desc'] != 'DAVIDSON') &
						(Data_2020['county_desc'] != 'DURHAM') &
						(Data_2020['county_desc'] != 'GASTON') &
						(Data_2020['county_desc'] != 'IREDELL') &
						(Data_2020['county_desc'] != 'JOHNSTON') &
						(Data_2020['county_desc'] != 'NEW HANOVER') &
						(Data_2020['county_desc'] != 'ONSLOW') &
						(Data_2020['county_desc'] != 'ORANGE') &
						(Data_2020['county_desc'] != 'PITT') &
						(Data_2020['county_desc'] != 'UNION') &
						(Data_2020['county_desc'] != 'WATAUGA') &
						(Data_2020['county_desc'] != 'WAKE') &
						(Data_2020['county_desc'] != 'MECKLENBURG') &
						(Data_2020['county_desc'] != 'GUILFORD') &
						(Data_2020['county_desc'] != 'FORSYTH')]
bottom80_2020.loc['Rural80',1:] = bottom80_2020.sum(axis=0)
bottom80_2020.drop(bottom80_2020.head(80).index,inplace=True)

#Combine urban, suburban, rural dataframes
frames = [top4_2020, mid16_2020, bottom80_2020]
geo2020 = pd.concat(frames)
geo2020.loc['Statewide',1:] = geo2020.sum(axis=0)
newcol = ['Urban4', 'Suburban16', 'Rural80', 'Statewide']
geo2020['county_desc'] = newcol
geo2020 = geo2020.reset_index()
del geo2020['index']

# Statewide totals for each column in county breakdown
Data_2020.loc['Statewide',1:] = Data_2020.sum(axis=0)
Data_2020['county_desc'] = Data_2020['county_desc'].replace(np.nan, 'Statewide', regex=True)
Data_2020 = Data_2020.reset_index()
del Data_2020['index']

# Calculated fields for county breakdown
Data_2020['DEM%_of_registrants'] = (100 * Data_2020['reg_DEM'] / Data_2020['reg_Total']).round(2)
Data_2020['REP%_of_registrants'] = (100 * Data_2020['reg_REP'] / Data_2020['reg_Total']).round(2)
Data_2020['Other%_of_registrants'] = (100 * Data_2020['reg_Other'] / Data_2020['reg_Total']).round(2)
Data_2020['%DEM_voting'] = (100 * Data_2020['turn_DEM'] / Data_2020['reg_DEM']).round(2)
Data_2020['%REP_voting'] = (100 * Data_2020['turn_REP'] / Data_2020['reg_REP']).round(2)
Data_2020['%Other_voting'] = (100 * Data_2020['turn_Other'] / Data_2020['reg_Other']).round(2)
Data_2020['DEM%_of_AB'] = (100 * Data_2020['ab_DEM'] / Data_2020['ab_Total']).round(2)
Data_2020['REP%_of_AB'] = (100 * Data_2020['ab_REP'] / Data_2020['ab_Total']).round(2)
Data_2020['Other%_of_AB'] = (100 * Data_2020['ab_Other'] / Data_2020['ab_Total']).round(2)
Data_2020['DEM%_of_votes'] = (100 * Data_2020['turn_DEM'] / Data_2020['turn_Total']).round(2)
Data_2020['REP%_of_votes'] = (100 * Data_2020['turn_REP'] / Data_2020['turn_Total']).round(2)
Data_2020['Other%_of_votes'] = (100 * Data_2020['turn_Other'] / Data_2020['turn_Total']).round(2)
Data_2020['DEM_votes%-reg%'] = Data_2020['DEM%_of_votes'] - Data_2020['DEM%_of_registrants']
Data_2020['REP_votes%-reg%'] = Data_2020['REP%_of_votes'] - Data_2020['REP%_of_registrants'] 
Data_2020['Other_votes%-reg%'] = Data_2020['Other%_of_votes'] - Data_2020['Other%_of_registrants']

# Calculated fields for geographic breakdown
geo2020['DEM%_of_registrants'] = (100 * geo2020['reg_DEM'] / geo2020['reg_Total']).round(2)
geo2020['REP%_of_registrants'] = (100 * geo2020['reg_REP'] / geo2020['reg_Total']).round(2)
geo2020['Other%_of_registrants'] = (100 * geo2020['reg_Other'] / geo2020['reg_Total']).round(2)
geo2020['%DEM_voting'] = (100 * geo2020['turn_DEM'] / geo2020['reg_DEM']).round(2)
geo2020['%REP_voting'] = (100 * geo2020['turn_REP'] / geo2020['reg_REP']).round(2)
geo2020['%Other_voting'] = (100 * geo2020['turn_Other'] / geo2020['reg_Other']).round(2)
geo2020['DEM%_of_AB'] = (100 * geo2020['ab_DEM'] / geo2020['ab_Total']).round(2)
geo2020['REP%_of_AB'] = (100 * geo2020['ab_REP'] / geo2020['ab_Total']).round(2)
geo2020['Other%_of_AB'] = (100 * geo2020['ab_Other'] / geo2020['ab_Total']).round(2)
geo2020['DEM%_of_votes'] = (100 * geo2020['turn_DEM'] / geo2020['turn_Total']).round(2)
geo2020['REP%_of_votes'] = (100 * geo2020['turn_REP'] / geo2020['turn_Total']).round(2)
geo2020['Other%_of_votes'] = (100 * geo2020['turn_Other'] / geo2020['turn_Total']).round(2)
geo2020['DEM_votes%-reg%'] = geo2020['DEM%_of_votes'] - geo2020['DEM%_of_registrants']
geo2020['REP_votes%-reg%'] = geo2020['REP%_of_votes'] - geo2020['REP%_of_registrants'] 
geo2020['Other_votes%-reg%'] = geo2020['Other%_of_votes'] - geo2020['Other%_of_registrants']


########## 2020 v. 2016 ##########

Data_2020v2016 = Data_2020.set_index('county_desc').subtract(Data_2016.set_index('county_desc'), fill_value=0)
geo_2020v2016 = geo2020.set_index('county_desc').subtract(geo2016.set_index('county_desc'), fill_value=0)

# Write county comparison to CSV file in working directory
Data_2020v2016.to_csv('NC2020v2016countyreport.csv', sep=',', encoding='utf-8', header='true')

# Write geographic comparison to CSV file in working directory
geo_2020v2016.to_csv('NC2020v2016georeport.csv', sep=',', encoding='utf-8', header='true') 

print(Data_2020v2016)
print(geo_2020v2016)
