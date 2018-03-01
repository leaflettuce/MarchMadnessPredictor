# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 18:06:58 2018

@author: andyj
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 16:42:04 2018

@author: andyj
"""


import numpy as np 
import pandas as pd 
from sklearn.ensemble import RandomForestClassifier 
from sklearn.utils import shuffle

data_dir = 'd://Projects/MarchMadness/data/'

data = pd.read_csv('MM_Cleaned_2.csv')
sample_sub = pd.read_csv(data_dir + 'SampleSubmissionStage1.csv')

n_test_games = len(sample_sub)



'''FUNCTIONS TO SETTING TEST DATA'''
def get_year_t1_t2(ID):
    """Return a tuple with ints `year`, `team1` and `team2`."""
    return (int(x) for x in ID.split('_'))

def get_ppg(t_number):
    try:
        if t_number in data.LTeamID:
            return data[(data.LTeamID == t_number) & (data.Season == year)].LSeason_ppg.values[0]
        else:
            return data[(data.WTeamID == t_number) & (data.Season == year)].WSeason_ppg.values[0]
    except:
        return 72

def get_seed(t_number):
    try:
        if t_number in data.LTeamID:
            return data[(data.LTeamID == t_number) & (data.Season == year)].LSeed.values[0]
        else:
            return data[(data.WTeamID == t_number) & (data.Season == year)].WSeed.values[0]
    except:
        return 17

def get_fgp(t_number):
    try:
        if t_number in data.LTeamID:
            return data[(data.LTeamID == t_number) & (data.Season == year)].LSeason_FGPercent.values[0]
        else:
            return data[(data.WTeamID == t_number) & (data.Season == year)].WSeason_FGPercent.values[0]
    except:
        return 0.44
    



'''SET SEED for TRAIN Differences'''
df_wins = pd.DataFrame()
df_wins['SeedDiff'] = data['SeedDiff']
df_wins['PointsDiff'] = data['Season_ppg_diff']
df_wins['FGPDiff'] = data['Season_FGP_Diff']
df_wins['Result'] = 1

df_losses = pd.DataFrame()
df_losses['SeedDiff'] = -data['SeedDiff']
df_losses['PointsDiff'] = -data['Season_ppg_diff']
df_losses['FGPDiff'] = -data['Season_FGP_Diff']
df_losses['Result'] = 0

df_predictions = pd.concat((df_wins, df_losses))
df_predictions.head()


#SET TRAIN DATA
X_train = df_predictions[['SeedDiff', 'PointsDiff', 'FGPDiff']]
y_train = df_predictions.Result.values
X_train, y_train = shuffle(X_train, y_train)

#TRAIN MODEL - RANDOM FOREST
clf = RandomForestClassifier(max_depth=3, random_state=42)
clf.fit(X_train, y_train)

print(clf.feature_importances_)


'''SET TEST DATA: (SEED_DIFF, PPG_DIFF, FGP_DIFF)'''
X_test = np.zeros(shape=(n_test_games, 3))
for ii, row in sample_sub.iterrows():
    year, t1, t2 = get_year_t1_t2(row.ID)
    
    t1_seed = get_seed(t1)
    t2_seed = get_seed(t2)
    diff_seed = t1_seed - t2_seed
    X_test[ii, 0] = diff_seed
    
    t1_ppg = get_ppg(t1)
    t2_ppg = get_ppg(t2)
    ppg_diff = t1_ppg - t2_ppg
    X_test[ii, 1] = ppg_diff
    
    t1_fgp = get_fgp(t1)
    t2_fgp = get_fgp(t2)
    fgp_diff = t1_fgp - t2_fgp
    X_test[ii, 2] = fgp_diff
    

    

#MAKE PREDICTIONS
preds = clf.predict_proba(X_test)[:,1]

clipped_preds = np.clip(preds, 0.1, 0.9)
sample_sub.Pred = clipped_preds
sample_sub.head()

#Write it
sample_sub.to_csv('3Feature_RandomForest_sub.csv', index=False)



