import json
import copy

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


def find_possible_switch_stations(lines_per_station, line):
    ret = []
    for station, lines in lines_per_station.items():
        if line in lines and len(lines) >= 2:
            ret.append(station)
    return ret

def find_all_switches(network, lines_per_station):
    ret = {}
    for line, stations in network.items():
        ret[line] = find_possible_switch_stations(lines_per_station, line)
    return ret

def find_index_in_list(lst, el):
    for i, e in enumerate(lst):
        if e == el:
            return i
    return -1

def accumulate_stations(stations, start, dest):
    start_index = find_index_in_list(stations, start)
    dest_index = find_index_in_list(stations, dest)
    assert start_index >= 0
    assert dest_index >= 0
    ret = []
    indeces = []
    if start_index < dest_index:
        indeces = range(start_index, dest_index + 1)
    else:
        indeces = range(start_index, dest_index - 1, -1)
    for i in indeces:
        ret.append(stations[i])
    return ret

class MVG:
    def __init__(self):
        self.network = read_network()
        self.all_stations = find_all_stations(self.network)
        self.lines_per_station = index_network_by_line(self.network)
        self.switches_per_line = find_all_switches(self.network, self.lines_per_station)


    def find_route(self, start, dest):
        route = []
        start_lines = self.lines_per_station[start]
        dest_lines = self.lines_per_station[dest]
        common_lines = set(start_lines).intersection(set(dest_lines))
        if len(common_lines) > 0:
            return accumulate_stations(self.network[list(common_lines)[0]], start, dest)
        
        for start_line in start_lines:
            for dest_line in dest_lines:
                start_switches = self.switches_per_line[start_line]
                dest_switches = self.switches_per_line[dest_line]
                common_switches = set(start_switches).intersection(set(dest_switches))
                if len(common_switches) > 0:
                    return self.find_route(start, list(common_switches)[0]) + self.find_route(list(common_switches)[0], dest)
        return route        
        # Falls zwei Stationen nicht mit einmal Umsteigen erreicht werden können, muss noch was gemacht werden
        #for start_line in start_lines:
        #    for dest_line in dest_lines:
        #        start_switches = self.switches_per_line[start_line]
        #        dest_switches = self.switches_per_line[dest_line]







def main():
    mvg = MVG()
    route = mvg.find_route("Erding", "Ebersberg")
    print(json.dumps(route))

if __name__=="__main__":
    main()