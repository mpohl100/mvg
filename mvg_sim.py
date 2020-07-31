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

def find_all_switches(network, lines_per_station)
    ret = {}
    for line, stations in network.items():
        ret[line] = find_possible_switch_stations(lines_per_station, line)

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
            return accumulate_stations(self, common_lines[0], start, dest)
        
        for start_line in start_lines:
            for dest_line in dest_lines:
                start_switches = self.switches_per_line[start_line]
                dest_switches = self.switches_per_line[dest_line]
                common_switches = start_switches.intersection(dest_switches)
                if len(common_switches) > 0:
                    return find_route(start, common_switches[0]) + find_route(common_switches[0], dest)
        
        # Falls zwei Stationen nicht mit einmal Umsteigen erreicht werden können, muss noch was gemacht werden
        #for start_line in start_lines:
        #    for dest_line in dest_lines:
        #        start_switches = self.switches_per_line[start_line]
        #        dest_switches = self.switches_per_line[dest_line]
                

        return route






def main():
    mvg = MVG()
    route = mvg.find_route(mvg.all_stations[0], mvg.all_stations[1])
    print(json.dumps(route))
    print(json.dumps(mvg.all_stations))

if __name__=="__main__":
    main()