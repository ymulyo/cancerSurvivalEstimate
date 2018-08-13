import subprocess
import pandas as pd
import time

test_var = ['control' ,'year_of_birth','race','ethnicity','tumor_stage','days_to_last_follow_up','simple_somatic_mutations','genes_with_simple_somatic_mutations']
results=pd.DataFrame(columns=test_var)
propertiesResults=pd.DataFrame(columns=test_var)
t0 = time.time()

for t in range(0,5):
    t1=time.time()
    bashCommand = "python3 randomForestBC.py"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    runResults = []
    propResults = []
    f = open('BCrun.txt')
    current = f.readline().replace('\n','')

    tests = []
    while (current != ''):
        #print(current)
        properties = []
        mae = []
        m = float('inf')
        mins = []
        if current in test_var:
            tests.append(current)
            #print(current)
            current = f.readline().replace('\n','')
            while (current not in test_var and current != ''):
                current = current.replace('([','').replace(']','').replace(')','').replace(' ','')
                current = current.split(',')
                mae.append(current[6])
                properties.append(current[0:6])
                if float(current[6])<m:
                    mins=[]
                    mins.append(len(mae)-1)
                    m = float(current[6])
                elif float(current[6])==m:
                    mins.append(len(mae))
                current = f.readline().replace('\n','')
        runResults.append(m)
        propResults.append(properties[mins[0]])

    results.loc[t]=runResults
    propertiesResults.loc[t]=propResults
    t2=time.time()
    print('runtime (in seconds) = '+str(t2-t1))

results.to_csv('BCmae.csv')
propertiesResults.to_csv('BCproperties.csv')
t3=time.time()
print('Total time alotted (in seconds) = '+str(t3-t0))
