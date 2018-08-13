import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
import csv
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)

estimators = [10, 50, 100]
crit = ["mse", "mae"]
max_dpth = [10, 20, None]
min_smp = [2, 10, 50]
bootstrp = [True, False]
oob_scre = [True, False]
min_leaf = [1, 10, 50]

errors = []


lung_cancer_data = pd.read_csv('processedDataLung.csv')
test_var = ['control' ,'intermediate_dimension', 'shortest_dimension','cigarettes_per_day','year_of_birth','gender','tissue_or_organ_of_origin','tumor_stage','simple_somatic_mutations','genes_with_simple_somatic_mutations']
txt = open("Lungrun.txt", "w")
for n in test_var:
    if n == 'control':
        lung_cancer_predictors = ['time', 'age_at_diagnosis']
    else:
        lung_cancer_predictors = ['time', 'age_at_diagnosis', n]
    txt.write(n + '\n')
    lung_X = lung_cancer_data[lung_cancer_predictors]
    lung_y = lung_cancer_data.survivalEstimate
    train_lung_X, val_lung_X, train_lung_y, val_lung_y = train_test_split(lung_X, lung_y, train_size = 0.9, random_state = 0)
    test_model = RandomForestRegressor()


    best = []
    lowest = 1

    for i in estimators:
        for j in crit:
            for k in  max_dpth:
                for l in min_smp:
                    for m in bootstrp:
                        for o in min_leaf:
                            test_model = RandomForestRegressor(n_estimators=i, criterion=j, max_depth=k, min_samples_split=l, bootstrap=m, min_samples_leaf=o)
                            test_model.fit(train_lung_X, train_lung_y)
                            initial_lung_preds = test_model.predict(val_lung_X)
                            x = mean_absolute_error(initial_lung_preds, val_lung_y)
                            y = [i,j,k,l,m,o]
                            #print(y)
                            #print(mean_absolute_error(initial_lung_preds, val_lung_y))
                            xy = (y,x)
                            txt.write(str(xy) + "\n")
                            errors.append(xy)
                            if lowest > x:
                                lowest = x
                                best = y


txt.close()
