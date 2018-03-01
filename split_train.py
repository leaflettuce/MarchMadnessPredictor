# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 11:15:42 2018

@author: andyj
"""

import numpy as np 
import pandas as pd 
from sklearn.utils import shuffle

#import data and trim unnecessary columns
data_dir = 'd://Projects/MarchMadness/data/'
df = pd.read_csv('MM_Cleaned_2.csv')

df.drop(labels=['SeedDiff', 'WLength', 'LLength'], inplace=True, axis=1) 



'''Import RPI and Connect'''
df_massey = pd.read_csv(data_dir + 'MasseyOrdinals.csv')
df_rpi = df_massey[(df_massey.SystemName == 'RPI') & (df_massey.RankingDayNum == 133)]
df_rpi.drop(labels=['SystemName', 'RankingDayNum'], inplace=True, axis=1) 

df_winrpi = df_rpi.rename(columns={'TeamID' : 'WTeamID', 'OrdinalRank' : 'WOrdinalRank'})
df_lossrpi = df_rpi.rename(columns={'TeamID' : 'LTeamID', 'OrdinalRank' : 'LOrdinalRank'})
df_dummy = pd.merge(left=df, right=df_winrpi, on=['Season', 'WTeamID'])
df = pd.merge(left=df_dummy, right=df_lossrpi, on=['Season', 'LTeamID'])
df['Rank_Diff'] = df['WOrdinalRank'] - df['LOrdinalRank']


'''TRAIN cols'''
df_wins = pd.DataFrame()
df_wins['Season'] = df['Season']
df_wins['TeamID'] = df['WTeamID']
df_wins['OtherTeamID'] = df['LTeamID']
df_wins['Loc'] = df['WLoc']
#df_wins['Coach'] = df['WCoach']
#df_wins['Seed'] = df['WSeed']

df_wins['PPG'] = df['WSeason_ppg']
df_wins['AST'] = df['WSeason_ast']
df_wins['FGP'] = df['WSeason_FGPercent']
df_wins['FGP3'] = df['WSeason_FGPercent3']
df_wins['FTP'] = df['WSeason_FTPercent']
df_wins['OR'] = df['WSeason_OR']
df_wins['DR'] = df['WSeason_DR']
df_wins['STL'] = df['WSeason_stl']
df_wins['BLK'] = df['WSeason_blk']
df_wins['Rank'] = df['WOrdinalRank']

df_wins['PPG_Diff'] = df['Season_ppg_diff']
df_wins['FGP_Diff'] = df['Season_FGP_Diff']
df_wins['AST_Diff'] = df['Season_ast_diff']
df_wins['FGP3_Diff'] = df['Season_FGP3_Diff']
df_wins['FTP_Diff'] = df['Season_FTP_Diff']
df_wins['OR_Diff'] = df['Season_OR_diff']
df_wins['DR_Diff'] = df['Season_DR_diff'] 
df_wins['STL_Diff'] = df['Season_stl_diff']
df_wins['BLK_Diff'] = df['Season_blk_diff']
df_wins['Rank_Diff'] = df['Rank_Diff']
df_wins['Result'] = 1

df_losses = pd.DataFrame()
df_losses['Season'] = df['Season']
df_losses['TeamID'] = df['LTeamID']
df_losses['OtherTeamID'] = df['WTeamID']
df_losses['Loc'] = df['LLoc']
#df_losses['Coach'] = df['LCoach']
#df_losses['Seed'] = df['LSeed']

df_losses['PPG'] = df['LSeason_ppg']
df_losses['AST'] = df['LSeason_ast']
df_losses['FGP'] = df['LSeason_FGPercent']
df_losses['FGP3'] = df['LSeason_FGPercent3']
df_losses['FTP'] = df['LSeason_FTPercent']
df_losses['OR'] = df['LSeason_OR']
df_losses['DR'] = df['LSeason_DR']
df_losses['STL'] = df['LSeason_stl']
df_losses['BLK'] = df['LSeason_blk']
df_wins['Rank'] = df['LOrdinalRank']

df_losses['PPG_Diff'] = -df['Season_ppg_diff']
df_losses['FGP_Diff'] = -df['Season_FGP_Diff']
df_losses['AST_Diff'] = -df['Season_ast_diff']
df_losses['FGP3_Diff'] = -df['Season_FGP3_Diff']
df_losses['FTP_Diff'] = -df['Season_FTP_Diff']
df_losses['OR_Diff'] = -df['Season_OR_diff']
df_losses['DR_Diff'] = -df['Season_DR_diff'] 
df_losses['STL_Diff'] = -df['Season_stl_diff']
df_losses['BLK_Diff'] = -df['Season_blk_diff']
df_losses['Rank_Diff'] = -df['Rank_Diff']
df_losses['Result'] = 0


df_predictions = pd.concat((df_wins, df_losses))
df_predictions.TeamID = df_predictions.TeamID.astype('category')
df_predictions.head()



'''PRINT OUT CLEAN CSV'''
df_predictions.to_csv('train_data_diff.csv', index=False)