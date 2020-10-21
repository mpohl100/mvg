import json
from typing import List, Set, Dict, Tuple, Optional

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
        self.all_lines: Dict[str, List[str]] = {k:v['all_stations'] for k,v in self.all_info.items()}
        self.deduce_line_data()

    def deduce_line_data(self):
        self.all_stations: List[str] = find_all_stations(self.all_lines)
        self.lines_per_station: Dict[str, List[str]] = index_network_by_line(self.all_lines)    
