f = open("data/MUC_UBahnhoefe.txt", "r")
data = {}
current_line = ""
for i,x in enumerate(f):
    if i % 3 == 0:
        current_line = x.replace(" ", "").replace("\n","").replace("\t","")
        data[current_line] = { 'all_stations': [], 'switches': [] }
    elif i % 3 == 1:
        all_stations = x.split('>>')
        for bahnhof in all_stations:
            data[current_line]['all_stations'].append(bahnhof.replace(" ","").replace("\n","").replace("\t",""))
    elif i % 3 == 2:
        switches = x.split('>>')
        for bahnhof in switches:
            data[current_line]['switches'].append(bahnhof.replace(" ","").replace("\n","").replace("\t",""))
    else:
        raise ValueError("Eigentlich ist alles abgedeckt.")
w = open("data/MUC_UBahn.json", "w")
import json
w.write(json.dumps(data, indent=4))