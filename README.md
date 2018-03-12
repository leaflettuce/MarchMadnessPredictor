# MarchMadnessPredictor
Machine Learning to Predict 2018 March Madness Bracket

Predictor for NCAA game results. Estimates the probablilty of one team beating another in post-season tourney. Final test will be the 2018 March Madness Bracket. Current test results: 74% accurate.



This project slowly became, more-or-less, a mess of .py and .csv's.  Using data obtained from Kaggle, the final pipeline from cleaning to model fitting is:

-Clean_2.py            -> Cleans and organized data, creates many variables and results

-split_train.py        -> Splits the regulard season data into winning and lossing teams

-Tourny_Test_Formattin -> Adds result labels to tourny data

-Model_fitting.py      -> Final model testing and Kaggle submission code.
