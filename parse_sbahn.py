f = open("data/SBahnhoefe.txt", "r")
data = {}
current_line = ""
for i,x in enumerate(f):
    if i % 2 == 0:
        current_line = x.replace(" ", "").replace("\n","").replace("\t","")
        data[current_line] = []
    else:
        xx = x.split('>>')
        for bahnhof in xx:
            data[current_line].append(bahnhof.replace(" ","").replace("\n","").replace("\t",""))
w = open("data/SBahn.txt", "w")
import json
w.write(json.dumps(data))