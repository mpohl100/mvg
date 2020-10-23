import json
from typing import List, Set, Dict, Tuple, Optional

def find_all_stations(network: Dict[str, List[str]]):
    all_stations: List[str] = []
    for _, stations in network.items():
        all_stations.extend(stations['all_stations'])
    return set(all_stations)

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
    def __init__(self, files):
        self.all_info = read_from_files(files)
        self.construct(self.all_info)

    # hier wird das Builder-Pattern angewendet, da das Konstruieren von SubnetworkDbs ebenfalls durch ein NetworkDb Objekt dargestellt werden soll.
    def construct(self, all_info):
        self.all_lines = {k:{'all_stations': v['all_stations'], 'network': v['network']} for k,v in all_info.items()}
        self.all_stations: List[str] = find_all_stations(self.all_lines)
        self.by_network()

    def by_network(self):
        self.subnets = {}
        for line, v in self.all_lines.items():
            all_stations: List[str] = v['all_stations']
            network: str = v['network']
            if not network in self.subnets:
                self.subnets[network] = {}
            self.subnets[network][line] = {'all_stations': all_stations, 'network': network}
        if len(self.subnets.keys()) == 1:
            self.subnets = {} # Base Case für Rekursion. Wenn nur ein Netzwerk in der gesamten Datenstruktur ist, braucht es kein Subnetwork mehr
