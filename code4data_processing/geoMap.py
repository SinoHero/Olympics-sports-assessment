import csv
import os
import json
import math

allTimeline = {}
allRows = []
addition = 1
baseline = "BMX racing"
baselineInFile = 1
baselineSum = 163
allTimeline[baseline] = {}

for file in os.listdir('Trends/Data Round 4/'):
    if file.endswith('.csv') and "geoMap" in file:
        with open('Trends/Data Round 4/' + file, 'r') as f:
            reader = csv.reader(f)
            rows = list(reader)
            allRows.append(rows)


with open('Trends/Data Round 4/geoMap (25).csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        if len(row)>0:
            if row[0]!="Category: All categories" and row[0] != "Country":
                if row[baselineInFile] == '<1%':
                    row[baselineInFile] = "0.45%"
                if row[baselineInFile] == '':
                    row[baselineInFile] = "0%"
                allTimeline[baseline][row[0]] = 0#(float(row[baselineInFile][:-1])/baselineSum * 10000)# /2)

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
        standard = None
        for row in rows:
            if len(row) == 0 or row[0] == 'Category: All categories':
                continue
            if row[0] == "Country":
                names = []
                for item in row:
                    names.append(item.split(':')[0])

                
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
                            row[item] = '0%'
                        if row[standard] == '':
                            row[standard] = '0%'
                        if row[item] == '<1%':
                            row[item] = "0.45%"
                        if row[standard] == '<1%':
                            row[standard] = "0.45%"
                        if names[item] not in allTimeline:
                            allTimeline[names[item]] = {}
                        allTimeline[names[item]][row[0]] = math.log(float(row[item][:-1])+addition)-math.log(float(row[standard][:-1])+addition)+allTimeline[names[standard]][row[0]]

        if standard != None:
            for name in names[1:]:
                if name not in finished:
                    finished.append(name)

        




with open('Trends/allGeomap.json', 'w') as f:
    json.dump(allTimeline, f)