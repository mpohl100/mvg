f = open("data/bay/BAY_Bahnhoefe.txt", "r")
data = {}
current_line = ""
for i,x in enumerate(f):
    linenumber = i // 3
    if i % 3 == 0:
        line_segments = x.split("|")
        current_line = line_segments[0].replace(" ", "").replace("\n","").replace("\t","")
        network_name = line_segments[1].replace(" ", "").replace("\n","").replace("\t","")
        data[current_line + "(" + str(linenumber) + ")"] = { 'all_stations': [], 'network': network_name }
    elif i % 3 == 1:
        all_stations = x.split('>>')
        for bahnhof in all_stations:
            data[current_line + "(" + str(linenumber) + ")"]['all_stations'].append(bahnhof.replace(" ","").replace("\n","").replace("\t",""))
    elif i % 3 == 2:
        pass
    else:
        raise ValueError("Eigentlich ist alles abgedeckt.")
w = open("data/bay/BAY_Bahn.json", "w")
import json
w.write(json.dumps(data, indent=4))