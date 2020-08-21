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

class Network:
    def __init__(self, city, testnetwork=None):
        self.city = city
        self.all_info = self.get_all_info(city, testnetwork)
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
        #self.all_routes = {}
        #for start in self.all_stations:
        #    for dest in self.all_stations:
        #        route = self.find_route(start,dest)
        #        self.all_routes[start + " | " + dest] = route
    


    def find_route(self, start: str, dest: str):
        route: List[str] = []
        start_lines: List[str] = self.lines_per_station[start]
        dest_lines: List[str] = self.lines_per_station[dest]
        common_lines: Set[str] = set(start_lines).intersection(set(dest_lines))
        if len(common_lines) > 0:
            routes: List[str] = []
            for common_line in common_lines:
                routes.append( accumulate_stations(self.all_lines[common_line], start, dest) )
            routes.sort(key=lambda x : len(x))
            return routes[0]
        
        for start_line in start_lines:
            for dest_line in dest_lines:
                start_switches: List[str] = self.switches_per_line[start_line]
                dest_switches: List[str] = self.switches_per_line[dest_line]
                common_switches: Set[str] = set(start_switches).intersection(set(dest_switches))
                if len(common_switches) > 0:
                    routes: List[str] = []
                    for common_switch in common_switches:
                        routes.append( [self.find_route(start, common_switch), self.find_route(common_switch, dest)] )
                    # erst sortieren wir nach der Länge der  Gesamtstrecke und dann nach der Länge des ersten Abschnitts
                    routes.sort(key=lambda x : (len(x[0]) + len(x[1]), len(x[0])) )
                    return routes[0][0] + routes[0][1]
        return route        
        # Falls zwei Stationen nicht mit einmal Umsteigen erreicht werden können, muss noch was gemacht werden
        #for start_line in start_lines:
        #    for dest_line in dest_lines:
        #        start_switches = self.switches_per_line[start_line]
        #        dest_switches = self.switches_per_line[dest_line]

    def generate_graphviz(self, line=None, filename=None):
        import graphviz as gv
        #TODO auf networkx umstellen, wegen Farbupdatefähigkeit
        #import networkx as nx
        graph = gv.Graph(format="png", filename=filename if filename else self.city)
        stations = self.all_stations if line is None else self.all_lines[line]
        for station in stations:
            graph.node(station, label=station)
        inserted_edges = set()
        for name, line_stations in self.all_lines.items():
            if line and line != name:
                continue
            for i, station in enumerate(line_stations[0:-1]):
                if (station, line_stations[i+1]) in inserted_edges:
                    continue
                inserted_edges.add((station, line_stations[i+1]))
                inserted_edges.add((line_stations[i+1], station))
                graph.edge(station, line_stations[i+1])
                graph.edge(line_stations[i+1], station)
        return graph

    def generate_networkx(self, line=None):
        #TODO auf networkx umstellen, wegen Farbupdatefähigkeit
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

