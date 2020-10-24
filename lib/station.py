from network.networkdb import find_index_in_list, find_index_in_list_pred
from lib.lane import Lane
from typing import Dict, List   


def find_neighbour(lanes: Dict[str, List[str]], stations: List[str], index, line):
    if index >= 0 and index < len(stations):
        neighbour_station = stations[index]
        if neighbour_station in lanes:
            lanes[neighbour_station].append(line)
        else:
            lanes[neighbour_station] = [line]
    
def find_neighbours(networkdb: 'NetworkDb', station: str):
    neighbours: Dict[str, List[str]] = {}
    for line, v in networkdb.all_lines.items():
        stations = v['all_stations']
        index: int = find_index_in_list(stations, station)
        if index == -1:
            continue
        find_neighbour(neighbours, stations, index - 1, line)
        find_neighbour(neighbours, stations, index + 1, line)
    return neighbours

def find_lanes(station: str, networkdb: 'NetworkDb', all_stations: List['Station'], all_lines: List['Line']):
    neighbours = find_neighbours(networkdb, station)
    lanes: Dict[str, 'Lane'] = {}
    for neighbour_station, linenames in neighbours.items():
        lines = [] 
        for linename in linenames:
            line_index = find_index_in_list_pred(all_lines, lambda el: el.name == linename)
            if line_index == -1:
                raise ValueError(linename + " missing in simulation.all_lines")
            lines.append(all_lines[line_index])
        lanes[neighbour_station] = Lane(all_stations[station], all_stations[neighbour_station], lines)
    return lanes

class Station:
    def __init__(self, name: str):
        self.name: str = name
        self.lanes: Dict[str, 'Lane'] = {}
        self.trains: List['Train'] = []
        self.passengers: List['Passenger'] = []

    def __eq__(self, other: 'Station'):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def deduce_lanes(self, network: 'Network', all_stations: List['Station'], all_lines: List['Line']):
        self.lanes = find_lanes(self.name, network, all_stations, all_lines)

    def __str__(self):
        return self.name

    def register_arrival(self, train: 'Train'):
        self.trains.append(train)

    def register_departure(self, train: 'Train'):
        self.trains.remove(train)

    def can_arrive(self, train: 'Train'):
        if not train.current_station.name in self.lanes:
            return len(self.trains) == 0
        relevant_lines: List['Line'] = self.lanes[train.current_station.name].lines_by_network[train.line.networkname]
        can_arrive = True
        #reason = ""
        for t in self.trains:
            # Die Zielstation der Blockierenden darf nicht meine aktuelle Station sein.
            if t.line in relevant_lines and t.target_station != train.current_station:
                #reason = str(t)
                can_arrive = False
        #if tr.line:
        #     print("Can train " + str(train) + " arrive at " + str(self) + "?")
        #     if can_arrive:
        #         print("    Yes.")
        #     else: 
        #         print("    No, because of " + reason)
        return can_arrive

    def get_switch_lines(self):
        switch_lines = []
        for _, lane in self.lanes.items():
            switch_lines.extend(lane.lines)
        return list(set(switch_lines))

    def enter_passenger(self, passenger: 'Passenger'):
        self.passengers.append(passenger)

    def depart_passenger(self, passenger: 'Passenger'):
        passenger_index = find_index_in_list(self.passengers, passenger)
        if passenger_index == -1:
            raise ValueError("Passenger not found in station.")
        del self.passengers[passenger_index]