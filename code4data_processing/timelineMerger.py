import csv
import os
import json

with open('Trends/disciplines.json') as file:
    disciplines = json.load(file)
    list_of_disciplines = disciplines.keys()

allTimeline = {}
allRows = []
addition = 1
baseline = "Marathon swimming: (Worldwide)"
baselineInFile = 1
baselineSum = 118.45
allTimeline[baseline] = []

for file in os.listdir('Trends/Data Round 4/'):
    if file.endswith('.csv') and "multiTimeline" in file:
        with open('Trends/Data Round 4/' + file, 'r') as f:
            reader = csv.reader(f)
            rows = list(reader)
            allRows.append(rows)


with open('Trends/Data Round 4/multiTimeline (25).csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        if len(row)>0:
            if row[0]!="Category: All categories" and row[0] != "Week":
                if row[baselineInFile] == '<1':
                    row[baselineInFile] = "0.45"
                allTimeline[baseline].append(float(row[baselineInFile])/baselineSum * 10000)# /2)

"""
counter = 0
with open('Trends/Data Round 2/multiTimeline cross (2).csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        if len(row)>0:
            if row[0]!="Category: All categories" and row[0] != "Week":
                if row[baselineInFile] == '<1':
                    row[baselineInFile] = "0.45"
                allTimeline[baseline][counter] += (float(row[baselineInFile])/4136 * 10000 /2)
                counter += 1
                """

finished = [baseline]

while len(finished) < 52:
    print(len(finished))
    for rows in allRows:
        counter = 0
        standard = None
        for row in rows:
            if len(row) == 0 or row[0] == 'Category: All categories':
                continue
            if row[0] == "Week":
                names = row

                
                for name in names[1:]:
                    if name in finished: 
                        standard = names.index(name)
                        
                        continue
                
                if standard == None:
                    break
            else:
                for item in range(1, len(row)):
                    if item != standard and names[item] not in finished:
                        if row[item] == '':
                            continue
                        if row[item] == '<1':
                            row[item] = "0.45"
                        if row[standard] == '<1':
                            row[standard] = "0.45"
                        if names[item] in allTimeline:
                            allTimeline[names[item]].append((float(row[item])+addition)/(float(row[standard])+addition)*allTimeline[names[standard]][counter])
                        else:
                            allTimeline[names[item]] = [(float(row[item])+addition)/(float(row[standard])+addition)*allTimeline[names[standard]][counter]]
                counter += 1

        if standard != None:
            for name in names[1:]:
                if name not in finished:
                    finished.append(name)

        




with open('Trends/allTimelines.json', 'w') as f:
    json.dump(allTimeline, f)