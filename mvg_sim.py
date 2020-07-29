import json

def read_network():
    network_raw = {}
    # read U-Bahn
    with open('UBahn.txt', 'r') as infile:
        ubahn_data = json.load(infile)
        network_raw = ubahn_data
    # read S-Bahn
    with open('SBahn.txt', 'r') as infile:
        sbahn_data = json.load(infile)
        for lineName, stations in sbahn_data.items():
            network_raw[lineName] = stations
    return network_raw

def find_all_stations(network):
    all_stations = []
    for line, stations in network.items():
        all_stations.extend(stations)
    return set(all_stations)

def index_network_by_line(network):
    lines_per_station = {}
    for line, stations in network.items():
        for s in stations:
            if s in lines_per_station:
                lines_per_station[s].append(line)
            else:
                lines_per_station[s] = [line]
    return lines_per_station


def main():
    network = read_network()
    all_stations = find_all_stations(network)
    lines_per_station = index_network_by_line(network)
    print(json.dumps(lines_per_station))

if __name__=="__main__":
    main()