import json
from typing import List, Set, Dict, Tuple, Optional

def read_network(city: str):
    #                 linename  purpose   list of stations
    network_raw: Dict[str, Dict[str, List[str]]] = {}
    # read U-Bahn
    with open('data/' + city + '_UBahn.json', 'r') as infile:
        ubahn_data = json.load(infile)
        network_raw = ubahn_data
    # read S-Bahn
    with open('data/' + city + '_SBahn.json', 'r') as infile:
        sbahn_data = json.load(infile)
        for lineName, stations in sbahn_data.items():
            network_raw[lineName] = stations
    return network_raw

def find_all_stations(network: Dict[str, List[str]]):
    all_stations: List[str] = []
    for _, stations in network.items():
        all_stations.extend(stations)
    return set(all_stations)

def index_network_by_line(network: Dict[str, List[str]]):
    lines_per_station: Dict[str, List[str]] = {}
    for line, stations in network.items():
        for s in stations:
            if s in lines_per_station:
                lines_per_station[s].append(line)
            else:
                lines_per_station[s] = [line]
    return lines_per_station

def find_possible_switch_stations(lines_per_station: Dict[str, List[str]], line: str):
    ret: List[str] = []
    for station, lines in lines_per_station.items():
        if line in lines and len(lines) >= 2:
            ret.append(station)
    return ret

def find_all_switches(network: Dict[str, List[str]], lines_per_station: Dict[str, List[str]]):
    ret: Dict[str, List[str]] = {}
    for line, _ in network.items():
        ret[line] = find_possible_switch_stations(lines_per_station, line)
    return ret

def find_index_in_list(lst, el):
    for i, e in enumerate(lst):
        if e == el:
            return i
    return -1

def find_index_in_list_pred(lst, pred):
    for i, e in enumerate(lst):
        if pred(e):
            return i
    return -1

def accumulate_stations(stations: List[str], start: str, dest: str):
    start_index: int = find_index_in_list(stations, start)
    dest_index: int = find_index_in_list(stations, dest)
    assert start_index >= 0
    assert dest_index >= 0
    ret: List[str] = []
    indeces: List[int] = []
    if start_index < dest_index:
        indeces = range(start_index, dest_index + 1)
    else:
        indeces = range(start_index, dest_index - 1, -1)
    for i in indeces:
        ret.append(stations[i])
    return ret

def read_from_files(files):
    all_info = {}
    for i, file in enumerate(files):
        with open(file, 'r') as infile:
            data = json.load(infile)
            if i == 0:
                all_info = data
            else:
                all_info.update(data)
    return all_info

class NetworkDb:
    def __init__(self, city=None, testnetwork=None, files=None):
        if not files:
            self.city = city
            self.all_info = self.get_all_info(city, testnetwork)
        else:
            self.all_info = read_from_files(files)
        self.all_lines: Dict[str, List[str]] = {k:v['all_stations'] for k,v in self.all_info.items()}
        self.all_switches: Dict[str, List[str]] = {k:v['switches'] for k,v in self.all_info.items()}
        self.deduce_line_data()

    def get_all_info(self,city, testnetwork):
        all_info: Dict[str, Dict[str, List[str]]] = {} 
        if not testnetwork:
            all_info = read_network(city)
        else:
            all_info = {k: {'all_stations': v, 'switches': []} for k,v in testnetwork.items()}
        return all_info

    def deduce_line_data(self):
        self.all_stations: List[str] = find_all_stations(self.all_lines)
        self.lines_per_station: Dict[str, List[str]] = index_network_by_line(self.all_lines)
        self.switches_per_line: Dict[str, List[str]] = find_all_switches(self.all_lines, self.lines_per_station)    

    def generate_networkx(self, line=None):
        import networkx as nx
        graph = nx.Graph()
        stations = self.all_stations if line is None else self.all_lines[line]
        for station in stations:
            graph.add_node(station, label=station)
        inserted_edges = set()
        for name, line_stations in self.all_lines.items():
            if line and line != name:
                continue
            for i, station in enumerate(line_stations[0:-1]):
                if (station, line_stations[i+1]) in inserted_edges:
                    continue
                inserted_edges.add((station, line_stations[i+1]))
                inserted_edges.add((line_stations[i+1], station))
                graph.add_edge(station, line_stations[i+1])
                graph.add_edge(line_stations[i+1], station)
        return graph

