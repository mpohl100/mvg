from network.network import find_index_in_list
from lib.lane import Lane
from typing import Dict, List   


def find_neighbour(lanes: Dict[str, List[str]], stations: List[str], index, line):
    if index >= 0 and index < len(stations):
        neighbour_station = stations[index]
        if neighbour_station in lanes:
            lanes[neighbour_station].append(line)
        else:
            lanes[neighbour_station] = [line]
    
def find_neighbours(network: 'Network', station: str):
    neighbours: Dict[str, List[str]] = {}
    for line, stations in network.all_lines.items():
        index: int = find_index_in_list(stations, station)
        if index == -1:
            continue
        find_neighbour(neighbours, stations, index - 1, line)
        find_neighbour(neighbours, stations, index + 1, line)
    return neighbours

def find_lanes(simulation: 'Simulation', station: str):
    neighbours = find_neighbours(simulation.network, station)
    lanes: Dict[str, 'Lane'] = {}
    for neighbour_station, lines in neighbours.items():
        lanes[neighbour_station] = Lane(simulation.all_stations[station], simulation.all_stations[neighbour_station], lines)
    return lanes

class Station:
    def __init__(self, name: str, sim: 'Simulation'):
        self.name: str = name
        self.sim: 'Simulation' = sim
        self.lanes: Dict[str, List[str]] = {}
        self.trains: List['Train'] = []

    def deduce_lanes(self):
        self.lanes = find_lanes(self.sim, self.name)

    def __str__(self):
        return self.name

    def register_arrival(self, train: 'Train'):
        self.trains.append(train)

    def register_departure(self, train: 'Train'):
        self.trains.remove(train)

    def can_arrive(self, train: 'Train'):
        if not train.current_station.name in self.lanes:
            return len(self.trains) == 0
        relevant_lines: List[str] = self.lanes[train.current_station.name].lines
        can_arrive = True
        #reason = ""
        for t in self.trains:
            # Die Zielstation der Blockierenden darf nicht meine aktuelle Station sein.
            #TODO auf Line Objekte umstellen
            if t.line.name in relevant_lines and t.target_station != train.current_station and t.line.is_subway == train.line.is_subway:
                #reason = str(t)
                can_arrive = False
        #if tr.line:
        #     print("Can train " + str(train) + " arrive at " + str(self) + "?")
        #     if can_arrive:
        #         print("    Yes.")
        #     else: 
        #         print("    No, because of " + reason)
        return can_arrive