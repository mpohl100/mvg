
from typing import Dict, List, Set

class Line:
    def __init__(self, name: str, all_stations: List['Station'], networkname: str):
        self.name: str = name
        self.networkname: str = networkname
        self.all_stations: List['Station'] = all_stations
        self.all_stations_set: Set['Station'] = set(self.all_stations)
        self.trains: List['Train'] = []
        self.start_minute = None

    def __str__(self):
        return self.name

    def __eq__(self, other: 'Line'):
        return self.name == other.name and self.networkname == other.networkname

    def __hash__(self):
        return hash(self.name + self.networkname)

    def add_train(self, train):
        t: 'Train' = train
        self.trains.append(t)

    def set_start_minute(self, start_minute: 'StartMinute'):
        self.start_minute = start_minute


