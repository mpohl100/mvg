f = open("data/UBahnhoefe.txt", "r")
data = {}
current_line = ""
for x in f:
    if not x.startswith(">>"):
        current_line = x.replace(" ", "").replace("\n","").replace("\t","")
        data[current_line] = []
    else:
        data[current_line].append(x.replace(">>","").replace(" ","").replace("\n","").replace("\t",""))
w = open("data/UBahn.txt", "w")
import json
w.write(json.dumps(data))



