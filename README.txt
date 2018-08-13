############################
#README
#==========================
#CS542 Final Project
#==========================
############################
#finalDataLung.py
#———————————————
#Used to parse through json and tsk files (lung_clinical.json, lung-biospecimen.json, lung-survival-plot.json, and lungData.tsv)
#and output a csv file (lungFinalData.csv) that is to be used later in our Random Forest Algorithm (RFA)
#
############################
#finalDataBC.py
#———————————————
#Similar to finalDataLung.py but this handles the data for breast cancer (breast_clinical_cases.json, breast-survival-plot.json and breastData.tsv) and 
#outputs breastFinalData.csv
#
############################
#processDataLung.py
#———————————————
#Handles missing values of lungFinalData.csv and changes categorical data into quantitative data and the result is written 
#in processDataLung.csv.
#
############################
#processDataBC.py
#———————————————
#Handles missing values of breastFinalData.csv and changes categorical data into quantitative data and the result is written 
#in processDataBC.csv
#
############################
#randomForestLung.py
#———————————————
#Creates multiple Random Forests with different combinations of features and parameters from lungFinalData.csv and output the
#different results (by error%) into a text file called lungrun.txt
#
############################
#randomForestBC.py
#———————————————
#Similar to randomForestLung.py but handles breastFindalData.csv instead and the results are written into bcrun.txt
#
############################
#runLung.py
#———————————————
#Runs randomForestLung.py five times and creates lungProperties.csv and lungMae.csv
#
############################
#runBC.py
#———————————————
#Runs randomForestBreast.py five times and creates bcProperties.csv and bcMae.csv
#
############################
#oneRun.py
#———————————————
#Creates MAElist.txt which lists all 324 mean absolute errors from one run on the specified feature from the runBC.py or runLung.py output
#
############################

