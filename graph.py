import matplotlib.pyplot as plt
import json


with open("Model/output for United States.json", "r") as f:
    data = json.load(f)


def graph(plotInfo):
    
    disciplines = list(plotInfo.keys())
    scores = list(plotInfo.values())
    disciplines.reverse()
    scores.reverse()
    plt.barh(disciplines, scores, color='skyblue')

    # Add titles and labels
    plt.title('Score')
    plt.xlabel('Disciplines')
    plt.ylabel('Score')

    #plt.xticks(rotation=80)

    # Show the plot
    plt.show()


plotInfo = {}
for key, value in data.items():
    plotInfo[key.split(':')[0]] = value["Final"]
graph(plotInfo)