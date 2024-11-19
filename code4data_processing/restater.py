import json

with open('Trends/allGeomap.json', 'r') as f:
    data = json.load(f)


countries = []
restated = {}

for discipline, info in data.items():
    for country, value in info.items():
        if country not in countries:
            countries.append(country)
            restated[country] = {}
        restated[country][discipline] = value

final = {}
for country, info in restated.items():
    sorted_dict = dict(sorted(info.items(), key=lambda item: item[1], reverse=True))
    flag = 0
    for key, value in sorted_dict.items():
        if 0.000000001 > value and value >-0.000000001:
            flag +=1
    if flag < 3:
        final[country] = sorted_dict

with open('Trends/RestatedGeomap.json', 'w') as f:
    json.dump(final, f)