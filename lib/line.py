
from lib.route import Route, find_routes, find_sublines

from typing import Dict, List

class Line:
    def __init__(self, name: str, all_stations: List['Station'], switches: List['Station']):
        self.name: str = name
        self.is_subway: bool = self.name.startswith('U')
        self.all_stations: List['Station'] = all_stations
        self.switches: List['Station'] = switches
        # TODO Management von Sublinien einbauen, niedrige Prio
        self.routes: List[Route] = find_routes(self.switches, self.all_stations, self.name)
        self.sublines: Dict[Route, List['Station']] = find_sublines(self.all_stations, self.routes, self.name)
        self.trains: List['Train'] = []
        self.start_minute = None

    def __str__(self):
        return self.name

    def __eq__(self, other: 'Line'):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def add_train(self, train):
        t: 'Train' = train
        self.trains.append(t)

    def set_start_minute(self, start_minute: 'StartMinute'):
        self.start_minute = start_minute


