from lib.lane import Lane
from lib.line import Line
from lib.station import Station
from lib.train import Train

from typing import Dict, List
from collections import defaultdict

class Config:
    def __init__(self, subway_stride: int = 4, sbahn_stride: int = 8, minutes: int = 1440, verbosity: int = 0):
        self.nb_subway = subway_stride
        self.nb_sbahn = sbahn_stride
        self.minutes = minutes
        self.verbosity = verbosity

class Simulation:
    def __init__(self, network: 'Network', config: Config):
        self.network: 'Network' = network
        self.config: Config = config
        self.time: int = 0
        self.read_all_stations()
        self.read_all_lines()
        self.read_trains()

    def read_all_stations(self):
        self.all_stations: Dict[str, Station] = {}
        for station in self.network.all_stations:
            self.all_stations[station] = Station(station, self)
        for _, station in self.all_stations.items():
            station.deduce_lanes()
        self.all_lanes: List[Lane] = []
        for _, station in self.all_stations.items():
            self.all_lanes.extend([lane for _, lane in station.lanes.items()])
        # Test der Integrität des Netzwerks:
        set_lanes = set(self.all_lanes)
        if len(set_lanes) != len(self.all_lanes):
            raise Exception("Nicht einzigartige Lanes im Netzwerk vorhanden.")

    def read_all_lines(self):
        self.all_lines: List[Line] = []
        for line, info in self.network.all_info.items():
            all_station_names: List[str] = info['all_stations']
            switch_names: List[str] = info['switches']
            if '' in switch_names:
                switch_names.remove('')
            all_stations: List[Station] = [self.all_stations[station] for station in all_station_names] 
            switches: List[Station] = [self.all_stations[station] for station in switch_names] 
            self.all_lines.append(Line(line, all_stations, switches))

    def add_train(self, index: int, line, direction: int, nb_trains: int, start_minute: int):
        l: Line = line
        train = Train(self.config, l, l.all_stations[index], direction, nb_trains, start_minute)
        l.add_train(train)
        nb_trains += 1
        self.trains.append(train)
        return nb_trains

    def read_trains(self):
        self.trains: List[Train] = []
        nb_trains: int = 0
        for line in self.all_lines:
            nb_skip: int = self.config.nb_sbahn
            if line.is_subway:
                nb_skip = self.config.nb_subway
            for i in range(0,len(line.all_stations), nb_skip):
                start_minute = i*2 # TODO die richtigen Distanzen der Bahnhöfe einbauen
                nb_trains = self.add_train(0, line, +1, nb_trains, start_minute)
                nb_trains = self.add_train(-1, line, -1, nb_trains, start_minute)

    def update(self):
        self.time += 1
        for t in self.trains:
            t.reset()
        for t in self.trains:
            t.update()

    def run(self):
        for _ in range(0, self.config.minutes):
            self.update()
        if self.config.verbosity >= 1:
            self.print_stats()

    def print_stats(self):
        self.delay_per_train()
        self.delay_per_station()
        #self.print_lanes()
        #self.print_sublines()

    def delay_per_train(self):
        for t in sorted(self.trains, key=lambda x : x.delay):
            print(str(t) + " has " + str(t.delay) + " minutes delay.")

    def delay_per_station(self):
        stations = defaultdict(int)
        for t in self.trains:
            for station, delay in t.delay_per_station.items():
                stations[station.name] += delay
        print({k:v for k,v in sorted(stations.items(), key=lambda item : item[1], reverse=True)})

    def sum_delay(self):
        sum_delay = 0
        for t in self.trains:
            for _, delay in t.delay_per_station.items():
                sum_delay += delay
        return sum_delay       

    def print_lanes(self):
        for _, station in self.all_stations.items():
            print('station ' + station.name + ' has following lanes')
            print(station.lanes)
            print()

    def print_sublines(self):
        for line in self.all_lines:
            print(line)
            for subroute in line.sublines.keys():
                print('    ' + str(subroute))