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

    def read_all_stations(self):
        self.all_stations: Dict[str, Station] = {}
        for station in self.networkdb.all_stations:
            self.all_stations[station] = Station(station)

    def read_all_lines(self):
        self.all_lines: List[Line] = []
        for line, info in self.networkdb.all_info.items():
            all_station_names: List[str] = info['all_stations']
            switch_names: List[str] = info['switches']
            if '' in switch_names:
                switch_names.remove('')
            all_stations: List[Station] = [self.all_stations[station] for station in all_station_names] 
            switches: List[Station] = [self.all_stations[station] for station in switch_names] 
            self.all_lines.append(Line(line, all_stations, switches))
    
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
