# Import modules
import pandas as pd
import numpy as np
pd.options.mode.chained_assignment = None #hide SettingWithCopyWarning

########## 2020 ##########

# Read in results from 2020 Election
Results_2020 = pd.read_csv('https://s3.amazonaws.com/dl.ncsbe.gov/ENRS/2020_11_03/results_pct_20201103.zip', sep='\t')
Results_2020_table2 = pd.pivot_table(Results_2020, values='Total Votes', index=['County'], columns=['Choice'], aggfunc=np.sum)
Results_2020_table3 = pd.pivot_table(Results_2020, values='Total Votes', index=['County'], columns=['Election Date'], aggfunc=np.sum)
Results_2020_table = pd.merge(Results_2020_table2, Results_2020_table3, on=['County'])
Results_2020_table = pd.DataFrame(Results_2020_table.to_records()) #Flatten pivot table into dataframe
#Results_2020_table = Results_2020_table.rename(columns={'11/03/2020':'Total Votes'})

# Create table of Presidential results by County
Results_2020_President = Results_2020_table.filter(['County','Donald J. Trump','Joseph R. Biden','Jo Jorgensen','Howie Hawkins','Don Blankenship','Jade Simmons (Write-In)', 'Write-In (Miscellaneous)'], axis=1)

# Rename Presidential column names
Results_2020_President = Results_2020_President.rename(columns={"Donald J. Trump": "Trump", "Joseph R. Biden": "Biden", "Jo Jorgensen": "Jorgensen", "Howie Hawkins": "Hawkins", "Don Blankenship": "Blankenship","Jade Simmons (Write-In)": "Simmons", "Write-In (Miscellaneous)": "Pres_Write_In" })

# Statewide totals for each column in county breakdown
Results_2020_President.loc['Statewide',1:] = Results_2020_President.sum(axis=0)
Results_2020_President['County'] = Results_2020_President['County'].replace(np.nan, 'Statewide', regex=True)
Results_2020_President = Results_2020_President.reset_index()
del Results_2020_President['index']

# Convert NAN to zero and aggregate votes cast for president by county
Results_2020_President = Results_2020_President.fillna(0)
Results_2020_President['Total_Cast'] = Results_2020_President.apply(lambda row: row.Trump + row.Biden + row.Jorgensen + row.Hawkins + row.Blankenship + row.Simmons + row.Pres_Write_In, axis=1)

# Calculated fields for Presidential candidate percentage by county
Results_2020_President['Trump%'] = (100 * Results_2020_President['Trump'] / Results_2020_President['Total_Cast']).round(2)
Results_2020_President['Biden%'] = (100 * Results_2020_President['Biden'] / Results_2020_President['Total_Cast']).round(2)
Results_2020_President['Jorgensen%'] = (100 * Results_2020_President['Jorgensen'] / Results_2020_President['Total_Cast']).round(2)
Results_2020_President['Hawkins%'] = (100 * Results_2020_President['Hawkins'] / Results_2020_President['Total_Cast']).round(2)
Results_2020_President['Blankenship%'] = (100 * Results_2020_President['Blankenship'] / Results_2020_President['Total_Cast']).round(2)
Results_2020_President['Simmons%'] = (100 * Results_2020_President['Simmons'] / Results_2020_President['Total_Cast']).round(2)
Results_2020_President['Pres_Write_In%'] = (100 * Results_2020_President['Pres_Write_In'] / Results_2020_President['Total_Cast']).round(2)
Results_2020_President['Trump-Biden'] = Results_2020_President['Trump'] - Results_2020_President['Biden']
Results_2020_President['Trump-Biden%'] = Results_2020_President['Trump%'] - Results_2020_President['Biden%']

# Create table of Presidential results by County
Results_2020_Senate = Results_2020_table.filter(['County','Thom Tillis','Cal Cunningham','Shannon W. Bray','Kevin E. Hayes'], axis=1)

# Rename Presidential column names
Results_2020_Senate = Results_2020_Senate.rename(columns={"Thom Tillis": "Tillis", "Cal Cunningham": "Cunningham", "Shannon W. Bray": "Bray", "Kevin E. Hayes": "Hayes"})

# Statewide totals for each column in county breakdown
Results_2020_Senate.loc['Statewide',1:] = Results_2020_Senate.sum(axis=0)
Results_2020_Senate['County'] = Results_2020_Senate['County'].replace(np.nan, 'Statewide', regex=True)
Results_2020_Senate = Results_2020_Senate.reset_index()
del Results_2020_Senate['index']

# Total votes cast for Senate in each county
Results_2020_Senate['Total_Cast'] = Results_2020_Senate.apply(lambda row: row.Tillis + row.Cunningham + row.Bray + row.Hayes, axis=1)

# Calculated fields for Senate candidate percentage by county
Results_2020_Senate['Tillis%'] = (100 * Results_2020_Senate['Tillis'] / Results_2020_Senate['Total_Cast']).round(2)
Results_2020_Senate['Cunningham%'] = (100 * Results_2020_Senate['Cunningham'] / Results_2020_Senate['Total_Cast']).round(2)
Results_2020_Senate['Bray%'] = (100 * Results_2020_Senate['Bray'] / Results_2020_Senate['Total_Cast']).round(2)
Results_2020_Senate['Hayes%'] = (100 * Results_2020_Senate['Hayes'] / Results_2020_Senate['Total_Cast']).round(2)

# Create table of Statewide results by County
Results_2020_Statewide = Results_2020_table.filter(['County', 'Donald J. Trump', 'Joseph R. Biden', 'Jo Jorgensen','Howie Hawkins','Don Blankenship','Jade Simmons (Write-In)', 'Write-In (Miscellaneous)', 'Thom Tillis', "Cal Cunningham", 'Shannon W. Bray','Kevin E. Hayes','Dan Forest', 'Roy Cooper', 'Steven J. DiFiore', 'Al Pisano', 'Mark Robinson', 'Yvonne Lewis Holley', "Jim O'Neill", "Josh Stein", 'E.C. Sykes', 'Elaine Marshall', 'Dale R. Folwell', 'Ronnie Chatterji', 'Catherine Truitt', 'Jen Mangrum', 'Anthony Wayne (Tony) Street', 'Beth A. Wood', 'Steve Troxler', 'Jenna Wadsworth', 'Josh Dobson', 'Jessica Holmes', 'Mike Causey', 'Wayne Goodwin'], axis=1)

# Rename Statewide column names
Results_2020_Statewide = Results_2020_Statewide.rename(columns={"Donald J. Trump": "Trump", "Joseph R. Biden": "Biden", "Jo Jorgensen": "Jorgensen", "Howie Hawkins": "Hawkins", "Don Blankenship": "Blankenship","Jade Simmons (Write-In)": "Simmons", "Write-In (Miscellaneous)": "Pres_Write_In", "Thom Tillis": "Tillis", "Cal Cunningham": "Cunningham", "Shannon W. Bray": "Bray", "Kevin E. Hayes": "Hayes", "Steven J. DiFiore": "DiFiore", "Al Pisano": "Pisano","Dan Forest": "Forest", "Roy Cooper": "Cooper","Mark Robinson": "Robinson", "Yvonne Lewis Holley": "Holley", "Jim O'Neill": "ONeill", "Josh Stein": "Stein", "E.C. Sykes": "Sykes", "Elaine Marshall": "Marshall","Dale R. Folwell": "Folwell", "Ronnie Chatterji": "Chatterji", "Catherine Truitt": "Truitt", "Jen Mangrum": "Mangrum", "Anthony Wayne (Tony) Street": "Street", "Beth A. Wood": "Wood", "Steve Troxler": "Troxler", "Jenna Wadsworth": "Wadsworth", "Josh Dobson": "Dobson", "Jessica Holmes": "Holmes", "Mike Causey": "Causey", "Wayne Goodwin": "Goodwin"})

# Calculated fields for Statewide candidates
Results_2020_Statewide['REP_AVG'] = Results_2020_Statewide[['Trump','Tillis','Forest','Robinson','ONeill','Sykes','Folwell','Truitt','Street','Troxler','Dobson','Causey']].mean(numeric_only=True, axis=1).round(0)#round to zero decimal palces
Results_2020_Statewide['REP_MIN'] = Results_2020_Statewide[['Trump','Tillis','Forest','Robinson','ONeill','Sykes','Folwell','Truitt','Street','Troxler','Dobson','Causey']].min(numeric_only=True, axis=1)
Results_2020_Statewide['REP_MAX'] = Results_2020_Statewide[['Trump','Tillis','Forest','Robinson','ONeill','Sykes','Folwell','Truitt','Street','Troxler','Dobson','Causey']].max(numeric_only=True, axis=1)
Results_2020_Statewide['DEM_AVG'] = Results_2020_Statewide[['Biden','Cunningham','Cooper','Holley','Stein','Marshall','Chatterji','Mangrum','Wood','Wadsworth','Holmes','Goodwin']].mean(numeric_only=True, axis=1).round(0)#round to zero decimal palces
Results_2020_Statewide['DEM_MIN'] = Results_2020_Statewide[['Biden','Cunningham','Cooper','Holley','Stein','Marshall','Chatterji','Mangrum','Wood','Wadsworth','Holmes','Goodwin']].min(numeric_only=True, axis=1)
Results_2020_Statewide['DEM_MAX'] = Results_2020_Statewide[['Biden','Cunningham','Cooper','Holley','Stein','Marshall','Chatterji','Mangrum','Wood','Wadsworth','Holmes','Goodwin']].max(numeric_only=True, axis=1)
Results_2020_Statewide['REP_High-Low'] = Results_2020_Statewide['REP_MAX'] - Results_2020_Statewide['REP_MIN']
Results_2020_Statewide['REP_AVG-DEM_AVG'] = Results_2020_Statewide['REP_AVG'] - Results_2020_Statewide['DEM_AVG']
Results_2020_Statewide['REP_Total'] = Results_2020_Statewide[['Trump','Tillis','Forest','Robinson','ONeill','Sykes','Folwell','Truitt','Street','Troxler','Dobson','Causey']].sum(numeric_only=True, axis=1).round(0)#round to zero decimal palces
Results_2020_Statewide['DEM_Total'] = Results_2020_Statewide[['Biden','Cunningham','Cooper','Holley','Stein','Marshall','Chatterji','Mangrum','Wood','Wadsworth','Holmes','Goodwin']].sum(numeric_only=True, axis=1).round(0)#round to zero decimal palces

# Statewide totals for each column in Results_2020_Statewide
Results_2020_Statewide.loc['Statewide',1:] = Results_2020_Statewide.sum(axis=0) 
Results_2020_Statewide['County'] = Results_2020_Statewide['County'].replace(np.nan, 'Statewide', regex=True)
Results_2020_Statewide = Results_2020_Statewide.reset_index()
del Results_2020_Statewide['index']

# Percentages for Statewide candidates
Results_2020_Statewide = Results_2020_Statewide.fillna(0)
Results_2020_Statewide['Total_President'] = Results_2020_Statewide.apply(lambda row: row.Trump + row.Biden + row.Jorgensen + row.Hawkins + row.Blankenship + row.Simmons + row.Pres_Write_In, axis=1)
Results_2020_Statewide['Trump%'] = (100 * Results_2020_Statewide['Trump'] / Results_2020_Statewide['Total_President']).round(2)
Results_2020_Statewide['Biden%'] = (100 * Results_2020_Statewide['Biden'] / Results_2020_Statewide['Total_President']).round(2)

Results_2020_Statewide['Total_Senate'] = Results_2020_Statewide.apply(lambda row: row.Tillis + row.Cunningham + row.Bray + row.Hayes, axis=1)
Results_2020_Statewide['Tillis%'] = (100 * Results_2020_Statewide['Tillis'] / Results_2020_Statewide['Total_Senate']).round(2)
Results_2020_Statewide['Cunningham%'] = (100 * Results_2020_Statewide['Cunningham'] / Results_2020_Statewide['Total_Senate']).round(2)

Results_2020_Statewide['Total_Governor'] = Results_2020_Statewide.apply(lambda row: row.Cooper + row.Forest + row.DiFiore + row.Pisano, axis=1)
Results_2020_Statewide['Forest%'] = (100 * Results_2020_Statewide['Forest'] / Results_2020_Statewide['Total_Governor']).round(2)
Results_2020_Statewide['Cooper%'] = (100 * Results_2020_Statewide['Cooper'] / Results_2020_Statewide['Total_Governor']).round(2)

Results_2020_Statewide['Robinson%'] = (100 * Results_2020_Statewide['Robinson'] / (Results_2020_Statewide['Robinson'] + Results_2020_Statewide['Holley'])).round(2)
Results_2020_Statewide['Holley%'] = (100 * Results_2020_Statewide['Holley'] / (Results_2020_Statewide['Robinson'] + Results_2020_Statewide['Holley'])).round(2)

Results_2020_Statewide['ONeill%'] = (100 * Results_2020_Statewide['ONeill'] / (Results_2020_Statewide['ONeill'] + Results_2020_Statewide['Stein'])).round(2)
Results_2020_Statewide['Stein%'] = (100 * Results_2020_Statewide['Stein'] / (Results_2020_Statewide['ONeill'] + Results_2020_Statewide['Stein'])).round(2)

Results_2020_Statewide['Sykes%'] = (100 * Results_2020_Statewide['Sykes'] / (Results_2020_Statewide['Sykes'] + Results_2020_Statewide['Marshall'])).round(2)
Results_2020_Statewide['Marshall%'] = (100 * Results_2020_Statewide['Marshall'] / (Results_2020_Statewide['Sykes'] + Results_2020_Statewide['Marshall'])).round(2)

Results_2020_Statewide['Folwell%'] = (100 * Results_2020_Statewide['Folwell'] / (Results_2020_Statewide['Folwell'] + Results_2020_Statewide['Chatterji'])).round(2)
Results_2020_Statewide['Chatterji%'] = (100 * Results_2020_Statewide['Chatterji'] / (Results_2020_Statewide['Folwell'] + Results_2020_Statewide['Chatterji'])).round(2)

Results_2020_Statewide['Truitt%'] = (100 * Results_2020_Statewide['Truitt'] / (Results_2020_Statewide['Truitt'] + Results_2020_Statewide['Mangrum'])).round(2)
Results_2020_Statewide['Mangrum%'] = (100 * Results_2020_Statewide['Mangrum'] / (Results_2020_Statewide['Truitt'] + Results_2020_Statewide['Mangrum'])).round(2)

Results_2020_Statewide['Street%'] = (100 * Results_2020_Statewide['Street'] / (Results_2020_Statewide['Street'] + Results_2020_Statewide['Wood'])).round(2)
Results_2020_Statewide['Wood%'] = (100 * Results_2020_Statewide['Wood'] / (Results_2020_Statewide['Street'] + Results_2020_Statewide['Wood'])).round(2)

Results_2020_Statewide['Troxler%'] = (100 * Results_2020_Statewide['Troxler'] / (Results_2020_Statewide['Troxler'] + Results_2020_Statewide['Wadsworth'])).round(2)
Results_2020_Statewide['Wadsworth%'] = (100 * Results_2020_Statewide['Wadsworth'] / (Results_2020_Statewide['Troxler'] + Results_2020_Statewide['Wadsworth'])).round(2)

Results_2020_Statewide['Dobson%'] = (100 * Results_2020_Statewide['Dobson'] / (Results_2020_Statewide['Dobson'] + Results_2020_Statewide['Holmes'])).round(2)
Results_2020_Statewide['Holmes%'] = (100 * Results_2020_Statewide['Holmes'] / (Results_2020_Statewide['Dobson'] + Results_2020_Statewide['Holmes'])).round(2)

Results_2020_Statewide['Causey%'] = (100 * Results_2020_Statewide['Causey'] / (Results_2020_Statewide['Causey'] + Results_2020_Statewide['Goodwin'])).round(2)
Results_2020_Statewide['Goodwin%'] = (100 * Results_2020_Statewide['Goodwin'] / (Results_2020_Statewide['Causey'] + Results_2020_Statewide['Goodwin'])).round(2)

Results_2020_Statewide['REP_AVG%'] = (100 * Results_2020_Statewide['REP_Total'] / (Results_2020_Statewide['REP_Total'] + Results_2020_Statewide['DEM_Total'] )).round(2)
Results_2020_Statewide['DEM_AVG%'] = (100 * Results_2020_Statewide['DEM_Total'] / (Results_2020_Statewide['REP_Total'] + Results_2020_Statewide['DEM_Total'] )).round(2)

# Create lists of column names to re-order clumns
County = ['County']
Statewide_list = ['Trump','Trump%','Biden','Biden%','Tillis','Tillis%','Cunningham','Cunningham%','Forest','Forest%','Cooper','Cooper%','Robinson','Robinson%','Holley','Holley%','ONeill','ONeill%','Stein','Stein%','Sykes','Sykes%','Marshall','Marshall%','Folwell','Folwell%','Chatterji','Chatterji%','Truitt','Truitt%','Mangrum','Mangrum%','Street','Street%','Wood','Wood%','Troxler','Troxler%','Wadsworth','Wadsworth%','Dobson','Dobson%','Holmes','Holmes%','Causey','Causey%','Goodwin','Goodwin%']	
Calc_list = ['REP_AVG','REP_MIN','REP_MAX','DEM_AVG','DEM_MIN','DEM_MAX','REP_High-Low','REP_AVG-DEM_AVG','Total_President','Total_Senate','Total_Governor']

# Combine lists of column names
columns_reordered = County + Statewide_list + Calc_list

# Reassign dataframe column values
Results_2020_Statewide = Results_2020_Statewide[columns_reordered]










# Write 2020 NC Presidential vote by county to CSV file in working directory
Results_2020_President.to_csv('NC2020Presidentcountyreport.csv', sep=',', encoding='utf-8', header='true')

# Write 2020 NC Statewide vote by county to CSV file in working directory
Results_2020_Statewide.to_csv('NC2020Statewidecountyreport.csv', sep=',', encoding='utf-8', header='true')

print(Results_2020_President)
print(Results_2020_Senate)
print(Results_2020_Statewide)