# -*- coding: utf-8 -*-
"""
Created on Wed Mar 07 10:04:27 2018

@author: andyj
"""

import pandas as pd 

#import data and trim unnecessary columns
data_dir = 'd://Projects/MarchMadness/data/'
df = pd.read_csv(data_dir + 'NCAATourneyCompactResults.csv')

df = df[(df.Season >= 2003) & (df.Season <= 2017)]
df_season_test = pd.DataFrame()
df_season_test2 = pd.DataFrame()


for ii, row in df.iterrows():
    info = df['Season'].astype('str') + '_' + df['WTeamID'].astype('str') + '_' + df['LTeamID'].astype('str')
    opp_info = df['Season'].astype('str') + '_' + df['LTeamID'].astype('str') + '_' + df['WTeamID'].astype('str')
    
df_season_test['ID'] = info
df_season_test['Result'] = 1
df_season_test2['ID'] = opp_info
df_season_test2['Result'] = 0
    
df_season_test_final = pd.concat((df_season_test, df_season_test2))

df_season_test_final.to_csv('season_test.csv', index=False)