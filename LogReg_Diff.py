# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 11:54:05 2018

@author: andyj
"""
import os
import numpy as np 
import pandas as pd 
import math
from sklearn.utils import shuffle
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LogisticRegressionCV
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import Imputer

os.chdir('D:/Projects/MarchMadness')
#IMPORTS
df = pd.read_csv('train_data_diff.csv')
data_dir = 'd://Projects/MarchMadness/data/'
sample_sub = pd.read_csv(data_dir + 'SampleSubmissionStage1.csv')
n_test_games = len(sample_sub)


'''SET DUMMIES'''
loc_dummies = pd.get_dummies(df.Loc)
df = pd.concat([df, loc_dummies], axis = 1)


'''Set WIN LOSS RATION'''
def get_count(teamID, year, wl):
    if wl == 1:
        try:
            return df[(df.TeamID == teamID) & (df.Season == year) & (df.Result == 1)].TeamID.value_counts().iloc[0]
        except IndexError:
            return 0
    else:
        try:
            return df[(df.TeamID == teamID) & (df.Season == year) & (df.Result == 0)].TeamID.value_counts().iloc[0]
        except IndexError:
            return 0

df['WLRatio'] = df.apply(lambda row: get_count(row.TeamID, row.Season, 1)/ (get_count(row.TeamID, row.Season, 0) + get_count(row.TeamID, row.Season, 1)).astype('float') - \
      get_count(row.OtherTeamID, row.Season, 1)/ (get_count(row.OtherTeamID, row.Season, 0) + get_count(row.OtherTeamID, row.Season, 1)).astype('float'), axis = 1)



'''SET TRAIN DATA'''
X_train = df[['PPG_Diff', 'FGP_Diff', 'AST_Diff', 'FGP3_Diff',
             'FTP_Diff', 'DR_Diff', 'STL_Diff', 'BLK_Diff', 'Rank_Diff', 'WLRatio']]

#X_train = df[['PPG_Diff', 'FGP_Diff', 'FGP3_Diff', 'DR_Diff']]

y_train = df['Result']
X_train, y_train = shuffle(X_train, y_train)




'''FUNCTIONS TO SETTING TEST DATA'''
def get_year_t1_t2(ID):
    """Return a tuple with ints `year`, `team1` and `team2`."""
    return (int(x) for x in ID.split('_'))


def get_stat(stat, t1, t2, year):
    if not math.isnan(df[(df.TeamID == t1) & (df.Season == year)][stat].mean() - df[(df.TeamID == t2) & (df.Season == year)][stat].mean()):
        return (df[(df.TeamID == t1) & (df.Season == year)][stat].mean() - df[(df.TeamID == t2) & (df.Season == year)][stat].mean())  
    else:
        return df[(df.TeamID == t1)][stat].mean() - df[(df.TeamID == t2)][stat].mean()


'''TRAIN MODEL - LOGISTIC REGRESSION
logreg = LogisticRegression()
params = {'C': np.logspace(start=-5, stop=3, num=9)}
clf = GridSearchCV(logreg, params, scoring='neg_log_loss', refit=True)
clf.fit(X_train, y_train)
print('Best log_loss: {:.4}, with best C: {}'
      .format(clf.best_score_, clf.best_params_['C']))
'''

'''TRAIN MODEL - LOG REG CV
clf = LogisticRegressionCV()
clf.fit(X_train, y_train)
'''


'''TRAIN MODEL - RANDOM FOREST'''
clf = RandomForestClassifier(random_state=42)
clf.fit(X_train, y_train)
clf.feature_importances_

'''SET TEST DATA'''
X_test = np.zeros(shape=(n_test_games, 10))

stat_list = ['PPG', 'FGP', 'AST', 'FGP3', 'FTP', 'DR', 'STL', 'BLK', 'Rank'] 
#stat_list = ['PPG', 'FGP', 'FGP3', 'DR'] 

for ii, row in sample_sub.iterrows():
    year, t1, t2 = get_year_t1_t2(row.ID)
    col_num = 0
    
    for team_stat in stat_list:
        X_test[ii, col_num] = get_stat(team_stat, t1, t2, year)
        col_num += 1
        
    X_test[ii, col_num] =  get_count(t1, year, 1)/ (get_count(t1, year, 0) + get_count(t1, year, 1)).astype('float') - \
      get_count(t2, year, 1)/ (get_count(t2, year, 0) + get_count(t2, year, 1)).astype('float')

      
'''MAKE PREDICTIONS'''
imp = Imputer(missing_values='NaN', strategy='median', axis=1) 
imp.fit(X_test)
X_test = imp.fit_transform(X_test)

preds = clf.predict_proba(X_test)[:,1]

clipped_preds = np.clip(preds, 0.05, 0.95)
sample_sub.Pred = clipped_preds
sample_sub.Pred = clipped_preds
sample_sub.head()


'''WRITE PRED'''
sample_sub.to_csv('RandForest_4FD_clipped_sub.csv', index=False)