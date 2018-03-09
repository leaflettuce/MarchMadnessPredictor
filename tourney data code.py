# -*- coding: utf-8 -*-
"""
Created on Wed Mar 07 22:49:59 2018

@author: andyj
"""

if math.isnan(tourny_data[(tourny_data.WTeamID == t1) & (tourny_data.Season == year)].count()[0]) and \
     math.isnan(tourny_data[(tourny_data.WTeamID == t2) & (tourny_data.Season == year)].count()[0]):
        return 0
    elif math.isnan(tourny_data[(tourny_data.WTeamID == t1) & (tourny_data.Season == year)].count()[0]):
        return -tourny_data[(tourny_data.WTeamID == t2) & (tourny_data.Season == year)].count()[0]                                      
    elif math.isnan(tourny_data[(tourny_data.WTeamID == t2) & (tourny_data.Season == year)].count()[0]):
        return tourny_data[(tourny_data.WTeamID == t1) & (tourny_data.Season == year)].count()[0]                                   
    else:
        return tourny_data[(tourny_data.WTeamID == t1) & (tourny_data.Season == year)].count()[0] - \
                 tourny_data[(tourny_data.WTeamID == t2) & (tourny_data.Season == year)].count()[0]        