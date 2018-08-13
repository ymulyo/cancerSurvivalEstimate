import json

survivalPlot = []
biospecimenCases = []
clinCases = []

#Survival plot data extraction

with open('lung-survival-plot.json') as f:
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

#Biospecimen Data Extraction
with open('lung-biospecimen.json') as f:
    biospecimenCases = json.load(f)

biospecDict = {}
wantedValues = ["sample_type", "intermediate_dimension", "shortest_dimension", "state", "tumor_code", "portions"]
for i in biospecimenCases:
    tempDict = {}
    found = False
    index = 0
    while(not(found) and index < len(i["samples"])):
        curSample = i["samples"][index]
        if curSample["sample_type_id"] == "01" and curSample["state"] == "live":
            for j in wantedValues:
                if j in curSample:
                    if j == "portions":
                        if "slides" in curSample[j][0]:
                            tempDict["slides"] = curSample[j][0]["slides"]
                        else:
                            tempDict["slides"] = None
                    else:
                        tempDict[j] = curSample[j]
                else:
                    tempDict[j] = None
            found = True
        index += 1




    biospecDict[i["case_id"]] = tempDict

#Clinical cases data extraction

with open('lung_clinical_cases.json') as f:
    clinCases = json.load(f)

clinicalCases = {}
cid = ["case_id"]
treatments = ["treatment_or_therapy","treatment_intent_type","therapeutic_agents"]
demographic = ["gender","year_of_birth","race","ethnicity"]
exposures = ["cigarettes_per_day","weight","alcohol_history","alcohol_intensity","bmi","years_smoked"]
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

#Merge them base on patient ID

mergeDataID = biospecDict
popID = []
for key in mergeDataID:
    if key in projectSurvivalDict:
        mergeDataID[key].update(projectSurvivalDict[key])
    else:
        popID.append(key)

for i in popID:
    mergeDataID.pop(i,None)

popID = []
for key in mergeDataID:
    if key in clinicalCases:
        mergeDataID[key].update(clinicalCases[key])
    else:
        popID.append(key)

for i in popID:
    mergeDataID.pop(i,None)

test = list(mergeDataID["14313474-376f-4606-9ed9-25ed2acff411"].values())
test2 = list(mergeDataID["14313474-376f-4606-9ed9-25ed2acff411"].keys())

#Added Mutations and Genes

from pandas import DataFrame
df = DataFrame.from_csv("lungData.tsv", sep="\t")
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
print(mergeDataID)

csvArray = []
first = []
totalList = []
for i in mergeDataID:
    totalList.append([list(mergeDataID[i].keys()), list(mergeDataID[i].values())])

string1 = ','.join(totalList[0][0])
f = open("lungFinalData.csv", "w")
f.write(string1 + "\n")
tl = []
for i in range(0,len(totalList)):
    l1 = []
    for j in range(0, len(totalList[i][1])):
        if j == 5:
            l1.append(str(None))
        else:
            l1.append(str(totalList[i][1][j]))
    tl.append(l1)

for i in range(0, len(tl)):
    string2 = ','.join(tl[i])
    f.write(string2 + "\n")

f.close
