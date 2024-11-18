from topsis import *
import json
import csv
import math

np.set_printoptions(suppress=True)

def save(text):
    with open("Model/output.txt", "a") as f:
        f.write(text + "\n")

validation = ["breaking", "baseball", "flag football", "fencing", "rowing", "artistic gymnastics", "esports", "cricket", "ultimate frisbee"]

with open("Model/1-1 Local.json", "r") as f:
    countries = list(json.load(f).keys())
#countries = ["Japan", "Australia", "United States", "Russia", "France", ]

def mainModel(country):
    total_data = {}

    save("Model weights for " + country)
    with open("Model/1-1 Local.json", "r") as f:
        rawgeomap = rescale_dict_values(json.load(f)[country])
    geomap = {}
    for key, value in rawgeomap.items():
        geomap[key.split(":")[0].lower()] = value

    with open("Model/1-2 Popularity.json", "r") as f:
        rawpopularity = rescale_dict_values(json.load(f))
    popularity = {}
    for key, value in rawpopularity.items():
        popularity[key.split(":")[0].lower()] = value

    data = []
    for key, value in popularity.items():
        if key.split(':')[0] not in validation:
            data.append([key.split(':')[0], value, geomap[key.split(':')[0]]])

    C1weights, _ = topsis(data, ["Sport", "Global", country])

    save("Criteria 1: Global, Local: " + str(C1weights))

    for key, value in popularity.items():
        total_data[key.split(":")[0].lower()] = {"C1": C1weights[0] * value + C1weights[1] * geomap[key.split(':')[0]]}


    data = []
    with open("Model/5-1 Relevance.json", "r") as f:
        relevance = rescale_dict_values(json.load(f))

    with open("Model/5-2 Innovation.json", "r") as f:
        innovation = rescale_dict_values(json.load(f))

    for key, value in relevance.items():
        if key not in validation:
            data.append([key, value, innovation[key]])

    C5weights, _ = topsis(data, ["Sport", "Relevance", "Innovation"])

    save("Criteria 5: Relevance, Innovation: " + str(C5weights))

    for key, value in relevance.items():
        total_data[key.lower()]["C5"] = (C5weights[0] * value + C5weights[1] * innovation[key])

    with open("Model/3 Sustainability.json", "r") as f:
        sustainability = rescale_dict_values(json.load(f))

    for key, value in sustainability.items():
        total_data[key.lower()]["C3"] = value

    gender = {}
    injury = {}
    inclusivity = {}
    with open("Model/246.csv", "r") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            a = float(row[4])
            b = float(row[5])
            gender[row[0].lower()] = 1-abs((a-b)/(a+b))
            total_data[row[0].lower()]["C2"] = gender[row[0].lower()]
            

            inclusivity[row[0]] = float(row[-1])#*random.uniform(0.5, 2)

            injury[row[0]] = float(row[1])#*random.uniform(0.5, 2)

    max_inclu = max(inclusivity.values())
    min_inclu = min(inclusivity.values())
    for item in inclusivity.keys():
        inclusivity[item] = inclusivity[item]/max_inclu
        total_data[item.lower()]["C4"] = inclusivity[item]

    max_injury = max(injury.values())
    min_injury = min(injury.values())
    for item in injury.keys():
        injury[item] = (1-(injury[item]/100))
        total_data[item.lower()]["C6"] = injury[item]




    #Final topsis:
    data = []
    for key, value in total_data.items():
        if key not in validation:
            data.append([key, value["C1"], value["C2"], value["C3"], value["C4"], value["C5"], value["C6"]])

    Cweights, _ = topsis(data, ["Sport", "C1", "C2", "C3", "C4", "C5", "C6"])

    save("Criteria weights: " + str(Cweights))

    for key, value in total_data.items():
        total_data[key.lower()]["Final"] = Cweights[0] * value["C1"] + Cweights[1] * value["C2"] + Cweights[2] * value["C3"] + Cweights[3] * value["C4"] + Cweights[4] * value["C5"] + Cweights[5] * value["C6"]

    sorted_data = sorted_dict = dict(sorted(total_data.items(), key=lambda item: item[1]["Final"], reverse=True))

    with open("Model/output for " + country + ".json", "w") as f:
        json.dump(sorted_data, f)


for country in countries:
    mainModel(country)
