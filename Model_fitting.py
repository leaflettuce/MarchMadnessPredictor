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
from sklearn.preprocessing import Imputer
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_validate
from sklearn.feature_selection import SelectPercentile
from sklearn.feature_selection import SelectKBest
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LogisticRegressionCV
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn import grid_search
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn import svm

import plotly.plotly as py
import plotly.graph_objs as go
from plotly import tools

os.chdir('D:/Projects/MarchMadness')



####################
### IMPORT FILES ###
####################
df = pd.read_csv('train_data_diff.csv')
data_dir = 'd://Projects/MarchMadness/data/'
sample_sub = pd.read_csv(data_dir + 'SampleSubmissionStage1.csv')
n_test_games = len(sample_sub)
tourney_tester = pd.read_csv('season_test.csv')
tourny_data = pd.read_csv(data_dir + 'NCAATourneyCompactResults.csv')
tourny_data = tourny_data[(tourny_data.Season >= 2003) & (tourny_data.Season <= 2017)]
##############################################
########## HELPER FUNCTIONS ##################
##############################################
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


'''PULL INFO FROM SAMPLE SUBMISSION'''
def get_year_t1_t2(ID):
    """Return a tuple with ints `year`, `team1` and `team2`."""
    return (int(x) for x in ID.split('_'))


'''SETS TEAMS STAT MEAN DIFFERENTIALS BASED ON REGULAR SEASON DATA'''
def get_stat(stat, t1, t2, year):
    if not math.isnan(df[(df.TeamID == t1) & (df.Season == year)][stat].mean() - df[(df.TeamID == t2) & (df.Season == year)][stat].mean()):
        return df[(df.TeamID == t1) & (df.Season == year)][stat].mean() - df[(df.TeamID == t2) & (df.Season == year)][stat].mean()  
    else:
        return df[(df.TeamID == t1)][stat].mean() - df[(df.TeamID == t2)][stat].mean()



'''PULLS TRAINING DATA AND ENTERS INTO EMPTY DATASET'''
def set_and_format_train(data_set, input_df, stat_list):
    for ii, row in input_df.iterrows():
        year, t1, t2 = get_year_t1_t2(row.ID)
        col_num = 0
    
        for team_stat in stat_list:
            data_set[ii, col_num] = get_stat(team_stat, t1, t2, year)
            col_num += 1
 
        data_set[ii, col_num] =  get_count(t1, year, 1)/ (get_count(t1, year, 0) + get_count(t1, year, 1)).astype('float') - \
        get_count(t2, year, 1)/ (get_count(t2, year, 0) + get_count(t2, year, 1)).astype('float')
        col_num += 1
        
        data_set[ii, col_num] = get_win_avg(t1, t2)


'''Get avg wins of tourny games for team'''
tourny_data_train = tourny_data[(tourny_data.Season < 2017)]
tourny_win_avg = tourny_data_train.groupby('WTeamID').count().Season / tourny_data.groupby('WTeamID').Season.nunique()
 
def get_win_avg(t1, t2):
    try:
        return tourny_win_avg[t1] - tourny_win_avg[t2]    
    except KeyError:
        try:
            return -tourny_win_avg[t2]
        except KeyError:
            try:
                return tourny_win_avg[t1]
            except KeyError:
                return 0
                 
                 
#######################################
######### EDIT COLUMNS IN DF ##########
#######################################
'''SET DUMMIES'''
loc_dummies = pd.get_dummies(df.Loc)
df = pd.concat([df, loc_dummies], axis = 1)



#######################################
###### CREATE TEST DATA ## ############
#######################################
'''SET TEST DATAFRAME'''
test_data = np.zeros(shape=(len(tourney_tester), 12)) #11

'''SETTING FEATURES'''
stat_list = ['PPG', 'FGP', 'AST', 'FGP3', 'Seed', 'FTP', 'DR', 'STL', 'BLK', 'Rank'] 
set_and_format_train(test_data, tourney_tester, stat_list)

'''REULTS AND SHUFFLE DATA'''
test_data_results = tourney_tester['Result']      
X_data, y_data = shuffle(test_data, test_data_results)

'''FILL NaN's'''
imp = Imputer(missing_values='NaN', strategy='median', axis=1) 
imp.fit(X_data)
X_data = imp.fit_transform(X_data)


######################################
######### RESCALE DATA ###############
######################################
'''Standardize'''
scaler = StandardScaler()
scaler.fit(X_data)
X_data = scaler.transform(X_data)



############################################
#### FEATURE SELECTION AND TRAIN SPLIT #####
############################################
'''SELECTION SCORES'''
#X_new = SelectPercentile(percentile = 20).fit_transform(X_data, y_data)

selector = SelectKBest(k = 6)
X_new = selector.fit_transform(X_data, y_data)
#selector.scores_

'''SPLIT TRAIN AND TEST'''
X_train, X_test, y_train, y_test = train_test_split(X_new, y_data, test_size=0.20, random_state=42)



#######################################
######### FITTING MODELS ##############
#######################################
'''GAUSSIAN NAIVE BAYES'''
#clf = GaussianNB()
#clf.fit(X_train, y_train)


'''LOGISTIC REGRESSION'''
#logreg = LogisticRegression()
#params = {'C': np.logspace(start=-5, stop=3, num=9)}
#clf = GridSearchCV(logreg, params, scoring='neg_log_loss', refit=True)
#clf.fit(X_train, y_train)


'''LOG REG CV'''
#clf = LogisticRegressionCV()
#clf.fit(X_train, y_train)


'''TRAIN MODEL - RANDOM FOREST'''
#clf = RandomForestClassifier(random_state=42)
#clf.fit(X_train, y_train)


'''ADABOOST'''
ada = AdaBoostClassifier()
parameters = {'n_estimators':[10,50,100], 'random_state': [None, 0, 42, 138], \
              'learning_rate': [0.1, 0.5, 0.8, 1.0]}
clf = grid_search.GridSearchCV(ada, parameters)

clf.fit(X_train, y_train)


'''K Nearest Neighbor'''
#knn = KNeighborsClassifier()
#parameters = {'algorithm':['auto','ball_tree', 'kd_tree'], 'n_neighbors': [5, 100], \
 #             'weights': ['uniform', 'distance'], 'p': [1, 2]}
#clf = grid_search.GridSearchCV(knn, parameters)

#clf.fit(X_train, y_train) 


'''Support Vector Machine''' 
#svc = svm.SVC()
#parameters = {'kernel':['linear','rbf'], 'random_state': [None, 0, 42, 138], \
#              'gamma': ['auto', 0.25, 0.5, 0.7, 0.9], 'C': [0.2, 0.5, 0.8, 1.0], \
#              'probability': [True]}
#clf = grid_search.GridSearchCV(svc, parameters)

#clf.fit(X_train, y_train)


'''Multi-layer Perceptron Classifier (NN)'''
#mlp = MLPClassifier()
#parameters = {'hidden_layer_sizes':[(100,), (50,),(200,)], 'activation': ['identity','relu', 'logistic', 'tanh'], \
#              'solver': ['adam', 'lbfgs'], 'learning_rate': ['constant', 'invscaling', 'adaptive'], 'max_iter': [100, 200, 300], \
#              'early_stopping': [True]}
#clf = grid_search.GridSearchCV(mlp, parameters)
 
#clf.fit(X_train, y_train)


################################
### CLASSIFIER  REVIEW ########
################################
'''FEATURE SELECTION (IF GRIDSEARCH)'''
clf.best_estimator_
clf.best_score_

'''CROSS VALIDATE'''
cv_results = cross_validate(clf, X_train, y_train)
cv_results['test_score']  

'''PREDICTOR ACCURACY'''
clf.score(X_test, y_test)

'''Confusion Matrix'''
y_pred = clf.predict(X_test)
# TN,FP, FN, TP
confusion_matrix(y_test, y_pred)


#######################################
###### FORMAT SUBMISSION FILE #########
#######################################
'''SET TEST DATAFRAME'''
X_sub = np.zeros(shape=(n_test_games,  12)) #11

'''SETTING FEATURES'''
stat_list = ['PPG', 'FGP', 'AST', 'FGP3', 'Seed', 'FTP', 'DR', 'STL', 'BLK', 'Rank'] 
set_and_format_train(X_sub, sample_sub, stat_list)

'''Fill NaN's'''
imp = Imputer(missing_values='NaN', strategy='median', axis=1) 
imp.fit(X_sub)
X_sub = imp.fit_transform(X_sub)

'''MAKE PREDICTIONS'''
preds = clf.predict_proba(X_sub)[:,1]

'''CLIP PREDICTIONS'''
clipped_preds = np.clip(preds, 0.05, 0.95)
sample_sub.Pred = clipped_preds

'''WRITE TO CSV'''
sample_sub.to_csv('MLP-NN_12Feature_clipped_sub.csv', index=False)



#
#
#
#
#
#
#
######################
#EXTRA TESTING BELOW #
######################

#################################
##### TEST ON SPECIFIC ##########
#################################
'''TEST ON 2017 SEASON'''
season_tester_2017 = pd.DataFrame()
season_tester_2017_2 = pd.DataFrame()

'''create data'''
tourny_test = tourny_data[(tourny_data.Season == 2017)]
for ii, row in tourny_test.iterrows():
    info = tourny_test['Season'].astype('str') + '_' + tourny_test['WTeamID'].astype('str') + '_' + tourny_test['LTeamID'].astype('str')
    opp_info = tourny_test['Season'].astype('str') + '_' + tourny_test['LTeamID'].astype('str') + '_' + tourny_test['WTeamID'].astype('str')

'''set col names'''    
season_tester_2017['ID'] = info
season_tester_2017['Result'] = 1
season_tester_2017_2['ID'] = opp_info
season_tester_2017_2['Result'] = 0
    
'''split'''
season_test_final = pd.concat((season_tester_2017, season_tester_2017_2))
X_test_2017 = season_test_final['ID']
y_test_2017 = season_test_final['Result']
X_test_2017, y_test_2017 = shuffle(X_test_2017, y_test_2017)

'''format'''
X_sub_2017 = np.zeros(shape=(len(X_test_2017),  12)) #11

'''SETTING FEATURES'''
stat_list = ['PPG', 'FGP', 'AST', 'FGP3', 'Seed', 'FTP', 'DR', 'STL', 'BLK', 'Rank'] 
#stat_list = ['FGP']
season_test_final = season_test_final.reset_index()
set_and_format_train(X_sub_2017, season_test_final, stat_list)

'''nans'''
imp = Imputer(missing_values='NaN', strategy='median', axis=1) 
imp.fit(X_sub_2017)
X_sub_2017 = imp.fit_transform(X_sub_2017)

'''test'''
clf.score(X_sub_2017, y_test_2017)

pred_2017 = clf.predict(X_sub_2017)
confusion_matrix(y_test_2017, pred_2017)
