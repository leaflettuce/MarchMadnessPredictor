# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 17:58:11 2018

@author: andyj
"""
import pandas as pd 


#import seed and results data
data_dir = 'd://Projects/MarchMadness/data/'
df_seeds = pd.read_csv(data_dir + 'NCAATourneySeeds.csv')
df_tour = pd.read_csv(data_dir + 'RegularSeasonDetailedResults.csv')

df_seeds.head()

df_tour.head()

'''Function to set Losing Location'''
def get_lose_loc(win_loc):
    lose_loc = ''
    if win_loc == 'N':
        lose_loc = 'N'  
    elif win_loc == 'H':
        lose_loc = 'A'  
    else:
        lose_loc = 'H'
    return lose_loc

#Get Loser Location
df_tour['LLoc'] = df_tour.apply(lambda row: get_lose_loc(row.WLoc), axis = 1)  

""" SET SEED TO INT ONLY """
def seed_to_int(seed):
    #Get just the digits from the seeding. Return as int
    s_int = int(seed[1:3])
    return s_int
df_seeds['seed_int'] = df_seeds.Seed.apply(seed_to_int)
df_seeds.drop(labels=['Seed'], inplace=True, axis=1) # This is the string label


"""DROP COLS and ADD SCORE DIFF"""
df_tour.drop(labels=['DayNum', 'NumOT'], inplace=True, axis=1)

#ADD score differential
df_tour['Point_Diff'] = df_tour.WScore - df_tour.LScore
df_tour.head()




"""MERGE SEED and TEAM"""
df_winseeds = df_seeds.rename(columns={'TeamID':'WTeamID', 'seed_int':'WSeed'})
df_lossseeds = df_seeds.rename(columns={'TeamID':'LTeamID', 'seed_int':'LSeed'})
df_dummy = pd.merge(left=df_tour, right=df_winseeds, how='left', on=['Season', 'WTeamID']).fillna(17)
df_concat = pd.merge(left=df_dummy, right=df_lossseeds, on=['Season', 'LTeamID']).fillna(17)

df_concat['SeedDiff'] = df_concat.WSeed - df_concat.LSeed
df_concat.head()


"""IMPORT COACHES AND MERGE WITH CONCAT"""
df_coaches = pd.read_csv(data_dir + "TeamCoaches.csv")
df_coaches.drop(labels=['FirstDayNum', 'LastDayNum'], inplace=True, axis=1) 

df_wincoaches = df_coaches.rename(columns={'TeamID':'WTeamID', 'CoachName':'WCoach'})
df_losscoaches = df_coaches.rename(columns={'TeamID':'LTeamID', 'CoachName':'LCoach'})
df_dummy = pd.merge(left=df_concat, right=df_wincoaches, on=['Season', 'WTeamID'])
df_working = pd.merge(left=df_dummy, right=df_losscoaches, on=['Season', 'LTeamID'])

df_working.head()


"""ADD TIME IN DIV ONE"""
df_length = pd.read_csv(data_dir + "Teams.csv")
df_length['length'] = df_length.LastD1Season - df_length.FirstD1Season
df_length.drop(labels=['TeamName', 'FirstD1Season', 'LastD1Season'], inplace=True, axis=1)

#MERGE
df_winlength = df_length.rename(columns={'TeamID':'WTeamID', 'length':'WLength'})
df_losslength = df_length.rename(columns={'TeamID':'LTeamID', 'length':'LLength'})
df_dummy = pd.merge(left=df_working, right=df_winlength, on=['WTeamID'])
df_working = pd.merge(left=df_dummy, right=df_losslength, on=['LTeamID'])

df_working.head()

"""EXPLORE AND INCLUDE DETAILED RESULTS"""
df_detailed = pd.read_csv(data_dir + 'RegularSeasonDetailedResults.csv')

#POINTS PER GAME
df_Wppg = df_detailed.copy()
df_Wppg.drop(labels=['LTeamID', 'LScore', 'DayNum', 'WLoc', 'NumOT', 
                     'WFGM', 'WFGA', 'WFGM3', 'WFGA3','WFTM', 'WFTA', 
                     'WOR', 'WDR', 'WAst', 'WTO', 'WStl', 'WBlk', 'WPF', 
                     'LFGM', 'LFGA', 'LFGM3', 'LFGA3','LFTM', 'LFTA', 
                     'LOR', 'LDR', 'LAst', 'LTO', 'LStl', 'LBlk', 'LPF'], inplace=True, axis=1)
    
WSeason_ppg = df_Wppg.groupby(['Season', 'WTeamID'])['WScore'].mean()
WSeason_ppg = WSeason_ppg.to_frame()
WSeason_ppg.reset_index(inplace=True)  
#MERGE TO WORKING
WSeason_ppg.columns = ["Season", "WTeamID", "WSeason_ppg"]
df_working = pd.merge(left=df_working, right=WSeason_ppg, on=['Season', 'WTeamID'])

##LOSING PPG
df_Lppg = df_detailed.copy()
df_Lppg.drop(labels=['WTeamID', 'WScore', 'DayNum', 'WLoc', 'NumOT', 
                     'WFGM', 'WFGA', 'WFGM3', 'WFGA3','WFTM', 'WFTA', 
                     'WOR', 'WDR', 'WAst', 'WTO', 'WStl', 'WBlk', 'WPF', 
                     'LFGM', 'LFGA', 'LFGM3', 'LFGA3','LFTM', 'LFTA', 
                     'LOR', 'LDR', 'LAst', 'LTO', 'LStl', 'LBlk', 'LPF'], inplace=True, axis=1)
    
LSeason_ppg = df_Lppg.groupby(['Season', 'LTeamID'])['LScore'].mean()
LSeason_ppg = LSeason_ppg.to_frame()
LSeason_ppg.reset_index(inplace=True)  
#MERGE TO WORKING
LSeason_ppg.columns = ["Season", "LTeamID", "LSeason_ppg"]
df_working = pd.merge(left=df_working, right=LSeason_ppg, on=['Season', 'LTeamID'])

##SEASON PPG DIFFERENTIAL
df_working['Season_ppg_diff'] = df_working['WSeason_ppg'] - df_working['LSeason_ppg']


########## ASSISTS PER GAME SEAONS
df_assist = df_detailed.copy()
df_assist.drop(labels=['LTeamID', 'LScore', 'WScore', 'DayNum', 'WLoc', 'NumOT', 
                     'WFGM', 'WFGA', 'WFGM3', 'WFGA3','WFTM', 'WFTA', 
                     'WOR', 'WDR', 'WTO', 'WStl', 'WBlk', 'WPF', 
                     'LFGM', 'LFGA', 'LFGM3', 'LFGA3','LFTM', 'LFTA', 
                     'LOR', 'LDR', 'LAst', 'LTO', 'LStl', 'LBlk', 'LPF'], inplace=True, axis=1)
    
WSeason_ast = df_assist.groupby(['Season', 'WTeamID'])['WAst'].mean()
WSeason_ast = WSeason_ast.to_frame()
WSeason_ast.reset_index(inplace=True)  
#MERGE TO WORKING
WSeason_ast.columns = ["Season", "WTeamID", "WSeason_ast"]
df_working = pd.merge(left=df_working, right=WSeason_ast, on=['Season', 'WTeamID'])


##LOSING ASSIST
df_assist = df_detailed.copy()
df_assist.drop(labels=['WTeamID', 'WScore', 'LScore', 'DayNum', 'WLoc', 'NumOT', 
                     'WFGM', 'WFGA', 'WFGM3', 'WFGA3','WFTM', 'WFTA', 
                     'WOR', 'WDR', 'WTO', 'WStl', 'WBlk', 'WPF', 
                     'LFGM', 'LFGA', 'LFGM3', 'LFGA3','LFTM', 'LFTA', 
                     'LOR', 'LDR', 'WAst', 'LTO', 'LStl', 'LBlk', 'LPF'], inplace=True, axis=1)
    
LSeason_ast = df_assist.groupby(['Season', 'LTeamID'])['LAst'].mean()
LSeason_ast = LSeason_ast.to_frame()
LSeason_ast.reset_index(inplace=True)  
#MERGE TO WORKING
LSeason_ast.columns = ["Season", "LTeamID", "LSeason_ast"]
df_working = pd.merge(left=df_working, right=LSeason_ast, on=['Season', 'LTeamID'])

#ASSIST SDIFF
df_working['Season_ast_diff'] = df_working['WSeason_ast'] - df_working['LSeason_ast']


#FIELD GOAL PERCENTAGES
df_fgp = df_detailed.copy()
df_fgp.drop(labels=['LTeamID', 'LScore', 'WScore', 'DayNum', 'WLoc', 'NumOT', 
                      'WFGM3', 'WFGA3','WFTM', 'WFTA', 
                     'WOR', 'WDR', 'WAst', 'WTO', 'WStl', 'WBlk', 'WPF', 
                     'LFGM', 'LFGA', 'LFGM3', 'LFGA3','LFTM', 'LFTA', 
                     'LOR', 'LDR', 'LAst', 'LTO', 'LStl', 'LBlk', 'LPF'], inplace=True, axis=1)
    
df_fgp['WPerent'] = df_fgp['WFGM'] / df_fgp['WFGA']    
WSeason_FGPercent = df_fgp.groupby(['Season', 'WTeamID'])['WPerent'].mean()
WSeason_FGPercent = WSeason_FGPercent.to_frame()
WSeason_FGPercent.reset_index(inplace=True)  
#MERGE TO WORKING
WSeason_FGPercent.columns = ["Season", "WTeamID", "WSeason_FGPercent"]
df_working = pd.merge(left=df_working, right=WSeason_FGPercent, on=['Season', 'WTeamID'])

##LOSING FGPercent
df_fgp = df_detailed.copy()
df_fgp.drop(labels=['WTeamID', 'WScore', 'LScore', 'DayNum', 'WLoc', 'NumOT', 
                      'WFGM3', 'WFGA3','WFTM', 'WFTA', 
                     'WOR', 'WDR', 'WAst', 'WTO', 'WStl', 'WBlk', 'WPF', 
                     'WFGM', 'WFGA', 'LFGM3', 'LFGA3','LFTM', 'LFTA', 
                     'LOR', 'LDR', 'LAst', 'LTO', 'LStl', 'LBlk', 'LPF'], inplace=True, axis=1)
    
df_fgp['LPerent'] = df_fgp['LFGM'] / df_fgp['LFGA']    
LSeason_FGPercent = df_fgp.groupby(['Season', 'LTeamID'])['LPerent'].mean()
LSeason_FGPercent = LSeason_FGPercent.to_frame()
LSeason_FGPercent.reset_index(inplace=True)  
#MERGE TO WORKING
LSeason_FGPercent.columns = ["Season", "LTeamID", "LSeason_FGPercent"]
df_working = pd.merge(left=df_working, right=LSeason_FGPercent, on=['Season', 'LTeamID'])

#SEASON FGPERCENT DIFF
df_working['Season_FGP_Diff'] = df_working['WSeason_FGPercent'] - df_working['LSeason_FGPercent']


#####THREES####################################
#THREE PERCENTAGES
df_fgp = df_detailed.copy()
df_fgp.drop(labels=['LTeamID', 'LScore', 'WScore', 'DayNum', 'WLoc', 'NumOT', 
                      'WFTM', 'WFTA', 'WFGM', 'WFGA',
                     'WOR', 'WDR', 'WAst', 'WTO', 'WStl', 'WBlk', 'WPF', 
                     'LFGM', 'LFGA', 'LFGM3', 'LFGA3','LFTM', 'LFTA', 
                     'LOR', 'LDR', 'LAst', 'LTO', 'LStl', 'LBlk', 'LPF'], inplace=True, axis=1)
    
df_fgp['WPerent'] = df_fgp['WFGM3'] / df_fgp['WFGA3']    
WSeason_FGPercent = df_fgp.groupby(['Season', 'WTeamID'])['WPerent'].mean()
WSeason_FGPercent = WSeason_FGPercent.to_frame()
WSeason_FGPercent.reset_index(inplace=True)  
#MERGE TO WORKING
WSeason_FGPercent.columns = ["Season", "WTeamID", "WSeason_FGPercent3"]
df_working = pd.merge(left=df_working, right=WSeason_FGPercent, on=['Season', 'WTeamID'])

##LOSING FGPercent
df_fgp = df_detailed.copy()
df_fgp.drop(labels=['WTeamID', 'WScore', 'LScore', 'DayNum', 'WLoc', 'NumOT', 
                      'WFGM3', 'WFGA3','WFTM', 'WFTA', 
                     'WOR', 'WDR', 'WAst', 'WTO', 'WStl', 'WBlk', 'WPF', 
                     'WFGM', 'WFGA', 'LFGM', 'LFGA','LFTM', 'LFTA', 
                     'LOR', 'LDR', 'LAst', 'LTO', 'LStl', 'LBlk', 'LPF'], inplace=True, axis=1)
    
df_fgp['LPerent'] = df_fgp['LFGM3'] / df_fgp['LFGA3']    
LSeason_FGPercent = df_fgp.groupby(['Season', 'LTeamID'])['LPerent'].mean()
LSeason_FGPercent = LSeason_FGPercent.to_frame()
LSeason_FGPercent.reset_index(inplace=True)  
#MERGE TO WORKING
LSeason_FGPercent.columns = ["Season", "LTeamID", "LSeason_FGPercent3"]
df_working = pd.merge(left=df_working, right=LSeason_FGPercent, on=['Season', 'LTeamID'])

#SEASON FGPERCENT DIFF
df_working['Season_FGP3_Diff'] = df_working['WSeason_FGPercent3'] - df_working['LSeason_FGPercent3']



######FREE THROWSSS#################3
#FIELD GOAL PERCENTAGES
df_fgp = df_detailed.copy()
df_fgp.drop(labels=['LTeamID', 'LScore', 'WScore', 'DayNum', 'WLoc', 'NumOT', 
                      'WFGM3', 'WFGA3','WFGM', 'WFGA', 
                     'WOR', 'WDR', 'WAst', 'WTO', 'WStl', 'WBlk', 'WPF', 
                     'LFGM', 'LFGA', 'LFGM3', 'LFGA3','LFTM', 'LFTA', 
                     'LOR', 'LDR', 'LAst', 'LTO', 'LStl', 'LBlk', 'LPF'], inplace=True, axis=1)
    
df_fgp['WPerent'] = df_fgp['WFTM'] / df_fgp['WFTA']    
WSeason_FGPercent = df_fgp.groupby(['Season', 'WTeamID'])['WPerent'].mean()
WSeason_FGPercent = WSeason_FGPercent.to_frame()
WSeason_FGPercent.reset_index(inplace=True)  
#MERGE TO WORKING
WSeason_FGPercent.columns = ["Season", "WTeamID", "WSeason_FTPercent"]
df_working = pd.merge(left=df_working, right=WSeason_FGPercent, on=['Season', 'WTeamID'])

##LOSING FGPercent
df_fgp = df_detailed.copy()
df_fgp.drop(labels=['WTeamID', 'WScore', 'LScore', 'DayNum', 'WLoc', 'NumOT', 
                      'WFGM3', 'WFGA3','WFTM', 'WFTA', 
                     'WOR', 'WDR', 'WAst', 'WTO', 'WStl', 'WBlk', 'WPF', 
                     'WFGM', 'WFGA', 'LFGM3', 'LFGA3','LFGM', 'LFGA', 
                     'LOR', 'LDR', 'LAst', 'LTO', 'LStl', 'LBlk', 'LPF'], inplace=True, axis=1)
    
df_fgp['LPerent'] = df_fgp['LFTM'] / df_fgp['LFTA']    
LSeason_FGPercent = df_fgp.groupby(['Season', 'LTeamID'])['LPerent'].mean()
LSeason_FGPercent = LSeason_FGPercent.to_frame()
LSeason_FGPercent.reset_index(inplace=True)  
#MERGE TO WORKING
LSeason_FGPercent.columns = ["Season", "LTeamID", "LSeason_FTPercent"]
df_working = pd.merge(left=df_working, right=LSeason_FGPercent, on=['Season', 'LTeamID'])

#SEASON FGPERCENT DIFF
df_working['Season_FTP_Diff'] = df_working['WSeason_FTPercent'] - df_working['LSeason_FTPercent']


########## REBOUNDS PER GAME SEAONS
df_rebounds = df_detailed.copy()
df_rebounds.drop(labels=['LTeamID', 'LScore', 'WScore', 'DayNum', 'WLoc', 'NumOT', 
                     'WFGM', 'WFGA', 'WFGM3', 'WFGA3','WFTM', 'WFTA', 
                      'WTO', 'WStl', 'WBlk', 'WPF', 'WAst',
                     'LFGM', 'LFGA', 'LFGM3', 'LFGA3','LFTM', 'LFTA', 
                     'LOR', 'LDR', 'LAst', 'LTO', 'LStl', 'LBlk', 'LPF'], inplace=True, axis=1)
    
WSeason_OR = df_rebounds.groupby(['Season', 'WTeamID'])['WOR'].mean()
WSeason_OR = WSeason_OR.to_frame()
WSeason_OR.reset_index(inplace=True)  
#MERGE TO WORKING
WSeason_OR.columns = ["Season", "WTeamID", "WSeason_OR"]
df_working = pd.merge(left=df_working, right=WSeason_OR, on=['Season', 'WTeamID'])

##Defensive Rebounds
df_rebounds = df_detailed.copy()
df_rebounds.drop(labels=['LTeamID', 'LScore', 'WScore', 'DayNum', 'WLoc', 'NumOT', 
                     'WFGM', 'WFGA', 'WFGM3', 'WFGA3','WFTM', 'WFTA', 
                      'WTO', 'WStl', 'WBlk', 'WPF', 'WAst',
                     'LFGM', 'LFGA', 'LFGM3', 'LFGA3','LFTM', 'LFTA', 
                     'LOR', 'LDR', 'LAst', 'LTO', 'LStl', 'LBlk', 'LPF'], inplace=True, axis=1)
    
WSeason_DR = df_rebounds.groupby(['Season', 'WTeamID'])['WDR'].mean()
WSeason_DR = WSeason_DR.to_frame()
WSeason_DR.reset_index(inplace=True)  
#MERGE TO WORKING
WSeason_DR.columns = ["Season", "WTeamID", "WSeason_DR"]
df_working = pd.merge(left=df_working, right=WSeason_DR, on=['Season', 'WTeamID'])


####LOSING REBOUNDS
df_rebounds = df_detailed.copy()
df_rebounds.drop(labels=['WTeamID', 'LScore', 'WScore', 'DayNum', 'WLoc', 'NumOT', 
                     'WFGM', 'WFGA', 'WFGM3', 'WFGA3','WFTM', 'WFTA', 
                      'WTO', 'WStl', 'WBlk', 'WPF', 'WAst', 'WOR', 'WDR',
                     'LFGM', 'LFGA', 'LFGM3', 'LFGA3','LFTM', 'LFTA', 
                      'LAst', 'LTO', 'LStl', 'LBlk', 'LPF'], inplace=True, axis=1)
    
LSeason_OR = df_rebounds.groupby(['Season', 'LTeamID'])['LOR'].mean()
LSeason_OR = LSeason_OR.to_frame()
LSeason_OR.reset_index(inplace=True)  
#MERGE TO WORKING
LSeason_OR.columns = ["Season", "LTeamID", "LSeason_OR"]
df_working = pd.merge(left=df_working, right=LSeason_OR, on=['Season', 'LTeamID'])

##Defensive Rebounds
df_rebounds = df_detailed.copy()
df_rebounds.drop(labels=['WTeamID', 'LScore', 'WScore', 'DayNum', 'WLoc', 'NumOT', 
                     'WFGM', 'WFGA', 'WFGM3', 'WFGA3','WFTM', 'WFTA', 
                      'WTO', 'WStl', 'WBlk', 'WPF', 'WAst', 'WOR', 'WDR',
                     'LFGM', 'LFGA', 'LFGM3', 'LFGA3','LFTM', 'LFTA', 
                      'LAst', 'LTO', 'LStl', 'LBlk', 'LPF'], inplace=True, axis=1)
    
LSeason_DR = df_rebounds.groupby(['Season', 'LTeamID'])['LDR'].mean()
LSeason_DR = LSeason_DR.to_frame()
LSeason_DR.reset_index(inplace=True)  
#MERGE TO WORKING
LSeason_DR.columns = ["Season", "LTeamID", "LSeason_DR"]
df_working = pd.merge(left=df_working, right=LSeason_DR, on=['Season', 'LTeamID'])


#rebound SDIFF
df_working['Season_OR_diff'] = df_working['WSeason_OR'] - df_working['LSeason_OR']
df_working['Season_DR_diff'] = df_working['WSeason_DR'] - df_working['LSeason_DR']


##STEALS
df_steals = df_detailed.copy()
df_steals.drop(labels=['LTeamID', 'LScore', 'WScore', 'DayNum', 'WLoc', 'NumOT', 
                     'WFGM', 'WFGA', 'WFGM3', 'WFGA3','WFTM', 'WFTA', 'WAst',
                     'WOR', 'WDR', 'WTO', 'WBlk', 'WPF', 
                     'LFGM', 'LFGA', 'LFGM3', 'LFGA3','LFTM', 'LFTA', 
                     'LOR', 'LDR', 'LAst', 'LTO', 'LStl', 'LBlk', 'LPF'], inplace=True, axis=1)
    
WSeason_stl = df_steals.groupby(['Season', 'WTeamID'])['WStl'].mean()
WSeason_stl = WSeason_stl.to_frame()
WSeason_stl.reset_index(inplace=True)  
#MERGE TO WORKING
WSeason_stl.columns = ["Season", "WTeamID", "WSeason_stl"]
df_working = pd.merge(left=df_working, right=WSeason_stl, on=['Season', 'WTeamID'])

##LOSING STEALS\]
df_steals = df_detailed.copy()
df_steals.drop(labels=['WTeamID', 'LScore', 'WScore', 'DayNum', 'WLoc', 'NumOT', 
                     'WFGM', 'WFGA', 'WFGM3', 'WFGA3','WFTM', 'WFTA', 'WAst',
                     'WOR', 'WDR', 'WTO', 'WBlk', 'WPF', 
                     'LFGM', 'LFGA', 'LFGM3', 'LFGA3','LFTM', 'LFTA', 
                     'LOR', 'LDR', 'LAst', 'LTO', 'WStl', 'LBlk', 'LPF'], inplace=True, axis=1)
    
LSeason_stl = df_steals.groupby(['Season', 'LTeamID'])['LStl'].mean()
LSeason_stl = LSeason_stl.to_frame()
LSeason_stl.reset_index(inplace=True)  
#MERGE TO WORKING
LSeason_stl.columns = ["Season", "LTeamID", "LSeason_stl"]
df_working = pd.merge(left=df_working, right=LSeason_stl, on=['Season', 'LTeamID'])

#STEALS SDIFF
df_working['Season_stl_diff'] = df_working['WSeason_stl'] - df_working['LSeason_stl']


###BLOCKS
df_blocks = df_detailed.copy()
df_blocks.drop(labels=['LTeamID', 'LScore', 'WScore', 'DayNum', 'WLoc', 'NumOT', 
                     'WFGM', 'WFGA', 'WFGM3', 'WFGA3','WFTM', 'WFTA', 'WAst',
                     'WOR', 'WDR', 'WTO', 'WStl', 'WPF', 
                     'LFGM', 'LFGA', 'LFGM3', 'LFGA3','LFTM', 'LFTA', 
                     'LOR', 'LDR', 'LAst', 'LTO', 'LStl', 'LBlk', 'LPF'], inplace=True, axis=1)
    
WSeason_blk = df_blocks.groupby(['Season', 'WTeamID'])['WBlk'].mean()
WSeason_blk = WSeason_blk.to_frame()
WSeason_blk.reset_index(inplace=True)  
#MERGE TO WORKING
WSeason_blk.columns = ["Season", "WTeamID", "WSeason_blk"]
df_working = pd.merge(left=df_working, right=WSeason_blk, on=['Season', 'WTeamID'])

##LOSING blocks\]
df_blocks = df_detailed.copy()
df_blocks.drop(labels=['WTeamID', 'LScore', 'WScore', 'DayNum', 'WLoc', 'NumOT', 
                     'WFGM', 'WFGA', 'WFGM3', 'WFGA3','WFTM', 'WFTA', 'WAst',
                     'WOR', 'WDR', 'WTO', 'WBlk', 'WPF', 
                     'LFGM', 'LFGA', 'LFGM3', 'LFGA3','LFTM', 'LFTA', 
                     'LOR', 'LDR', 'LAst', 'LTO', 'WStl', 'LStl', 'LPF'], inplace=True, axis=1)
    
LSeason_blk = df_blocks.groupby(['Season', 'LTeamID'])['LBlk'].mean()
LSeason_blk = LSeason_blk.to_frame()
LSeason_blk.reset_index(inplace=True)  
#MERGE TO WORKING
LSeason_blk.columns = ["Season", "LTeamID", "LSeason_blk"]
df_working = pd.merge(left=df_working, right=LSeason_blk, on=['Season', 'LTeamID'])

#blocks SDIFF
df_working['Season_blk_diff'] = df_working['WSeason_blk'] - df_working['LSeason_blk']

"""SET TEAM ID as Categorica; and drop Scores """
df_working.WTeamID = df_working.WTeamID.astype('category')
df_working.LTeamID = df_working.LTeamID.astype('category')

df_working.drop(labels=['WScore', 'LScore', 'Point_Diff'], inplace=True, axis=1)
df_working.drop(labels=['WFGM', 'WFGA', 'WFGM3', 'WFGA3', 'WFTM', 'WFTA', 
                        'WOR', 'WDR', 'WAst', 'WTO', 'WStl', 'WBlk',
                        'WPF','LFGM', 'LFGA', 'LFGM3', 'LFGA3', 'LFTM', 'LFTA', 
                        'LOR', 'LDR', 'LAst', 'LTO', 'LStl', 'LBlk',
                        'LPF' ], inplace=True, axis=1)

    

'''RETURN NEW CSV WITH CREATED COLUMNS'''
df_working.to_csv('MM_Cleaned_2.csv', index=False)
