import sys
import pandas as pd
import statistics as st

process = False

try:
    trainingFile = sys.argv[1]
    process = True
except:
    print('Must provide Training CSV file as argument.')

if (process == True):
    data = pd.read_csv(trainingFile)

    def catReplace(f):
        re=st.mode(f)
        for i in range(0,len(f)):
            if f[i]=='None' or f[i]=='not reported' or f[i]=='stage x':
                f[i]=re
        return(f)

    def quantReplace(f):
        ft = []
        for i in range(0,len(f)):
            if f[i]!='None':
                ft.append(float(f[i]))
        med = st.median(ft)
        for i in range(0,len(f)):
            if f[i]=='None':
                f[i]=med
        return(f)

    def quantRace(f):
        qf = []
        for i in range(0,len(f)):
            if f[i]=='white':
                qf.append(0)
            elif f[i]=="asian":
                qf.append(1)
            elif f[i]=="black or african american":
                qf.append(2)
            elif f[i]=="american indian or alaska native":
                qf.append(3)
            else:
                print('race warning: '+f[i])
        return(qf)

    def quantEthnicity(f):
        qf = []
        for i in range(0,len(f)):
            if f[i]=='not hispanic or latino':
                qf.append(0)
            elif f[i]=="hispanic or latino":
                qf.append(1)
            else:
                print('ethnicity warning: '+f[i])
        return(qf)

    def quantDiagnose(f):
        qf = []
        for i in range(0,len(f)):
            qf.append(f[i].replace('C34.',''))
        return(qf)

    def quantTumor(f):
        qf = []
        for i in range(0,len(f)):
            if f[i]=='stage i' or f[i]=='stage ia':
                qf.append(0)
            elif f[i]=="stage ib":
                qf.append(1)
            elif f[i]=='stage ii' or f[i]=='stage iia':
                qf.append(2)
            elif f[i]=="stage iib":
                qf.append(3)
            elif f[i]=='stage iii' or f[i]=='stage iiia':
                qf.append(4)
            elif f[i]=="stage iiib":
                qf.append(5)
            elif f[i]=='stage iiic':
                qf.append(6)
            elif f[i]=='stage iva' or f[i]=='stage iv':
                qf.append(7)
            elif f[i]=="stage ivb":
                qf.append(8)
            else:
                print('tumor warning: '+f[i])
        print(len(qf)==len(f))
        return(qf)

    pd.options.mode.chained_assignment = None
    fields_of_interest = ['year_of_birth','race','ethnicity','tumor_stage','age_at_diagnosis','time','survivalEstimate','days_to_last_follow_up','simple_somatic_mutations','genes_with_simple_somatic_mutations']
    data['year_of_birth'] = quantReplace(data['year_of_birth'])
    data['race']=quantRace(catReplace(data['race']))
    data['ethnicity']=quantEthnicity(catReplace(data['ethnicity']))
    data['tumor_stage']=quantTumor(catReplace(data['tumor_stage']))
    data['age_at_diagnosis']=quantReplace(data['age_at_diagnosis'])
    data['days_to_last_follow_up'] = quantReplace(data['days_to_last_follow_up'])
    data['simple_somatic_mutations']=quantReplace(data['simple_somatic_mutations'])
    data['genes_with_simple_somatic_mutations']=quantReplace(data['genes_with_simple_somatic_mutations'])
    data=data[fields_of_interest]

    data.to_csv('processedDataBC.csv')
