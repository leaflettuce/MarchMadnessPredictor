# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 15:13:30 2018

@author: andyj
"""

import pandas as pd 
import os

os.chdir('D:/Projects/MarchMadness')

original_sub = pd.read_csv('ADA_12Feature_clipped_final.csv')
five38 = pd.read_csv('five38.csv')