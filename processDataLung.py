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
            if f[i]=='None'or f[i]=='not reported':
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

    def quantGender(f):
        qf = []
        for i in range(0,len(f)):
            if f[i]=='male':
                qf.append(0)
            elif f[i]=="female":
                qf.append(1)
            else:
                print('warning')
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
            elif f[i]=='stage iv' or f[i]=='stage iva':
                qf.append(6)
            elif f[i]=="stage ivb":
                qf.append(7)
            elif f[i]=='stage v' or f[i]=='stage va':
                qf.append(8)
            elif f[i]=="stage vb":
                qf.append(9)
            else:
                print('warning')
        print(len(qf)==len(f))
        return(qf)

    pd.options.mode.chained_assignment = None
    fields_of_interest = ['intermediate_dimension','shortest_dimension','cigarettes_per_day','year_of_birth','gender','tissue_or_organ_of_origin','tumor_stage','age_at_diagnosis','time','survivalEstimate','simple_somatic_mutations','genes_with_simple_somatic_mutations']
    data['intermediate_dimension'] = quantReplace(data['intermediate_dimension'])
    data['shortest_dimension'] = quantReplace(data['shortest_dimension'])
    data['cigarettes_per_day'] = quantReplace(data['cigarettes_per_day'])
    data['year_of_birth'] = quantReplace(data['year_of_birth'])
    data['gender']=quantGender(catReplace(data['gender']))
    data['tissue_or_organ_of_origin']=quantDiagnose(catReplace(data['tissue_or_organ_of_origin']))
    data['tumor_stage']=quantTumor(catReplace(data['tumor_stage']))
    data['age_at_diagnosis']=quantReplace(data['age_at_diagnosis'])
    data['simple_somatic_mutations']=quantReplace(data['simple_somatic_mutations'])
    data['genes_with_simple_somatic_mutations']=quantReplace(data['genes_with_simple_somatic_mutations'])
    data=data[fields_of_interest]

    data.to_csv('processedDataLung.csv')
