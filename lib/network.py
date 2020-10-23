from network.networkdb import NetworkDb
from lib.station import Station
from lib.line import Line
from lib.lane import Lane

from typing import Dict, List

class Network:
    def __init__(self, networkdb: 'NetworkDb'):
        self.networkdb = networkdb
        self.all_stations: Dict[str, Station] = {}
        self.all_lines: List[Line] = []
        self.all_lanes: List[Lane] = []
        self.read_all_stations()
        self.read_all_lines()
        self.deduce_lanes()
        self.deduce_subnets()

    def read_all_stations(self):
        self.all_stations: Dict[str, Station] = {}
        for station in self.networkdb.all_stations:
            self.all_stations[station] = Station(station)

    def read_all_lines(self):
        self.all_lines: List[Line] = []
        for line, info in self.networkdb.all_info.items():
            all_station_names: List[str] = info['all_stations']
            all_stations: List[Station] = [self.all_stations[station] for station in all_station_names]
            networkname: str = info['network']
            self.all_lines.append(Line(line, all_stations, networkname))
    
    def deduce_lanes(self):
        for _, station in self.all_stations.items():
            station.deduce_lanes(self.networkdb, self.all_stations, self.all_lines)
        self.all_lanes: List[Lane] = []
        for _, station in self.all_stations.items():
            self.all_lanes.extend([lane for _, lane in station.lanes.items()])
        # Test der Integrität des Netzwerks:
        set_lanes = set(self.all_lanes)
        if len(set_lanes) != len(self.all_lanes):
            raise Exception("Nicht einzigartige Lanes im Netzwerk vorhanden.")

    def deduce_subnets(self):
        self.subnets: Dict[str, 'Network'] = {}
        for networkname, network_all_info in self.networkdb.subnets.items():
            networkdb = NetworkDb([])
            networkdb.construct(network_all_info)
            self.subnets[networkname] = Network(networkdb)

    def generate_networkx(self, line=None):
        import networkx as nx
        graph = nx.Graph()
        stations = self.all_stations.values() if line is None else self.all_lines[line]
        for station in stations:
            graph.add_node(station.name, label=station.name)
        inserted_edges = set()
        for l in self.all_lines:
            if line and line != l.name:
                continue
            for i, station in enumerate(l.all_stations[0:-1]):
                if (station, l.all_stations[i+1]) in inserted_edges:
                    continue
                inserted_edges.add((station, l.all_stations[i+1]))
                inserted_edges.add((l.all_stations[i+1], station))
                graph.add_edge(station.name, l.all_stations[i+1].name)
                graph.add_edge(l.all_stations[i+1].name, station.name)
        return graph

