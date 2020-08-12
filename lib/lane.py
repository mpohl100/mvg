from typing import List

class Lane:
    def __init__(self, from_station: 'Station', to_station: 'Station', lines: List[str]):
        self.from_station: 'Station' = from_station
        self.to_station: 'Station' = to_station
        self.lines: List[str] = lines
        self.is_subway: bool = self.lines[0].startswith('U')
        self.is_double: bool = True # Doppelgleis
        self.trains: List['Train'] = []

    def __eq__(self, other: 'Lane'):
        return self.from_station.name == other.from_station.name and self.to_station.name == other.to_station.name and self.is_subway == other.is_subway

    def __hash__(self):
        return hash(self.from_station.name + self.to_station.name)

    def __str__(self):
        return str(self.from_station) + " -> " + str(self.to_station) + " (" + str(self.lines) + "):\n" + str([str(t) for t in self.trains])

    def register_arrival(self, train: 'Train'):
        self.trains.append(train)
        if len(self.trains) == 2:
            # Überprüfen ob die Richtungen entgegengesetzt sind
            sum_direction = 0
            for t in self.trains:
                sum_direction += t.direction
            if sum_direction != 0:
                raise Exception("Mehr als eine Bahn in der gleichen Richtung auf " + str(self))
    
    def register_departure(self, train: 'Train'):
        self.trains.remove(train)