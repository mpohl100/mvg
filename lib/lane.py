from typing import List, Dict

class Lane:
    def __init__(self, from_station: 'Station', to_station: 'Station', lines: List['Line']):
        self.from_station: 'Station' = from_station
        self.to_station: 'Station' = to_station
        self.lines: List['Line'] = lines
        self.lines_by_network: Dict[str, List['Line']] = {}
        for line in self.lines:
            if line.networkname in self.lines_by_network:
                self.lines_by_network[line.networkname].append(line)
            else:
                self.lines_by_network[line.networkname] = [line]
        self.trains: Dict[str, List['Train']] = {}
        for networkname in self.lines_by_network.keys():
            self.trains[networkname] = []

    def __eq__(self, other: 'Lane'):
        return self.from_station.name == other.from_station.name and self.to_station.name == other.to_station.name

    def __hash__(self):
        return hash(self.from_station.name + self.to_station.name)

    def __str__(self):
        return str(self.from_station) + " -> " + str(self.to_station) + " (" + str(self.lines) + "):\n" + self.print_trains()

    def print_trains(self):
        ret: str = ""
        for networkname, trains in self.trains:
            ret += networkname + ": "
            ret += str([str(t) for t in trains])
            ret += '\n'
        return ret

    def register_arrival(self, train: 'Train'):
        self.trains[train.line.networkname].append(train)
        if len(self.trains[train.line.networkname]) == 2:
            # Überprüfen ob die Richtungen entgegengesetzt sind
            sum_direction = 0
            for t in self.trains[train.line.networkname]:
                sum_direction += t.direction
            if sum_direction != 0:
                raise Exception("Mehr als eine Bahn in der gleichen Richtung auf " + str(self))
    
    def register_departure(self, train: 'Train'):
        self.trains[train.line.networkname].remove(train)

    def is_free_for(self, train: 'Train'):
        if len(self.trains[train.line.networkname]) == 0:
            return True
        # ab jetzt sollte maximal ein Zug enthalten sein.
        sum_direction = self.trains[train.line.networkname][0].direction + train.direction
        if sum_direction == 0: # entgegengesetzte Richtungen
            return True
        return False