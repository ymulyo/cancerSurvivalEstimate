import json

survivalPlot = []
biospecimenCases = []
clinCases = []

#Survival plot data extraction

with open('breast-survival-plot.json') as f:
    survivalPlot = json.load(f)

projectIDsurvival = survivalPlot[0]["donors"]

for i in projectIDsurvival:
    i.pop("project_id", None)
    i.pop("censored", None)
    i.pop("submitter_id", None)

projectSurvivalDict = {}
for i in projectIDsurvival:
    thisID = i["id"]
    tempDict = {}
    for key in i:
        if key != "id":
            tempDict[key] = i[key]
    projectSurvivalDict[thisID] = tempDict


#Clinical cases data extraction

with open('breast_clinical_cases.json') as f:
    clinCases = json.load(f)

clinicalCases = {}
cid = ["case_id"]
treatments = ["treatment_or_therapy","treatment_intent_type","therapeutic_agents"]
demographic = ["gender","year_of_birth","race","ethnicity"]
exposures = ["alcohol_history","alcohol_intensity","bmi","years_smoked"]
diagnoses = ["classification_of_tumor","last_known_disease_status","primary_diagnosis","tumor_stage","age_at_diagnosis","morphology","tissue_or_organ_of_origin","days_to_birth","progression_or_recurrence","prior_malignancy","site_of_resection_or_biopsy","days_to_last_follow_up"]

for i in range(0, len(clinCases)):
    thisCase = {}
    for j in range(0,len(demographic)):
        thisCase[demographic[j]] = clinCases[i]["demographic"][demographic[j]]
    for j in range(0,len(exposures)):
        thisCase[exposures[j]]= clinCases[i]["exposures"][0][exposures[j]]
    for j in range(0,len(diagnoses)):
        thisCase[diagnoses[j]]= clinCases[i]["diagnoses"][0][diagnoses[j]]
    for j in range(0,len(treatments)):
        thisCase[treatments[j]]= clinCases[i]["diagnoses"][0]["treatments"][0][treatments[j]]
    thisCase["submitter_id"] = clinCases[i]["demographic"]["submitter_id"].split("_")[0]
    clinicalCases[clinCases[i]["case_id"]]= thisCase

#print(clinicalCases['9857be0c-aeca-4a43-90b1-0535bd08e086'])
#Merge them base on patient ID

mergeDataID = projectSurvivalDict

popID = []
for key in mergeDataID:
    if key in clinicalCases:
        mergeDataID[key].update(clinicalCases[key])
    else:
        popID.append(key)

for i in popID:
    mergeDataID.pop(i,None)



#Added Mutations and Genes

from pandas import DataFrame
df = DataFrame.from_csv("breastData.tsv", sep="\t")
dataDict = df.to_dict()

temp = dataDict["Mutations"]
mutDict = {k: {"simple_somatic_mutations" : int(''.join(v.split(',')))} for k, v in temp.items()}
temp = dataDict["Genes"]
genesDict = {k: {"genes_with_simple_somatic_mutations" : int(''.join(v.split(',')))} for k, v in temp.items()}
mutGenes = mutDict
for i in mutGenes:
    mutGenes[i].update(genesDict[i])


for i in mergeDataID:
    curSubID = mergeDataID[i]["submitter_id"]
    if curSubID in mutGenes:
        mergeDataID[i].update(mutGenes[curSubID])
#print(mergeDataID['9857be0c-aeca-4a43-90b1-0535bd08e086'])

csvArray = []
first = []
totalList = []
for i in mergeDataID:
    totalList.append([list(mergeDataID[i].keys()), list(mergeDataID[i].values())])

string1 = ','.join(totalList[0][0])
print(string1)
f = open("breastFinalData.csv", "w")
f.write(string1 + "\n")
tl = []
for i in range(0,len(totalList)):
    l1 = []
    for j in range(0, len(totalList[i][1])):
        l1.append(str(totalList[i][1][j]))
    tl.append(l1)

#print(tl)
for i in range(0, len(tl)):
    string2 = ','.join(tl[i])
    #print(string2)
    f.write(string2 + "\n")

f.close
