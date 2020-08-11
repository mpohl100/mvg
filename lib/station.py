from network import find_index_in_list

from typing import Dict, List   


def find_neighbour(lanes: Dict[str, List[str]], stations: List[str], index, line):
    if index >= 0 and index < len(stations):
        neighbour_station = stations[index]
        if neighbour_station in lanes:
            lanes[neighbour_station].append(line)
        else:
            lanes[neighbour_station] = [line]
    
def find_neighbours(network: 'Network', station: str):
    lanes: Dict[str, List[str]] = {}
    for line, stations in network.all_lines.items():
        index: int = find_index_in_list(stations, station)
        if index == -1:
            continue
        find_neighbour(lanes, stations, index - 1, line)
        find_neighbour(lanes, stations, index + 1, line)
    return lanes

class Station:
    def __init__(self, name: str, sim: 'Simulation'):
        self.name: str = name
        self.sim: 'Simulation' = sim
        self.lanes: Dict[str, List[str]] = find_neighbours(self.sim.network, name)
        self.trains: List[Train] = []

    def __str__(self):
        return self.name

    def register_arrival(self, train):
        t: Train = train
        self.trains.append(t)

    def register_departure(self, train):
        t: Train = train
        self.trains.remove(t)

    def can_arrive(self, train):
        tr: Train = train
        relevant_lines: List[str] = self.lanes[tr.current_station.name]
        can_arrive = True
        #reason = ""
        for t in self.trains:
            # Die Zielstation der Blockierenden darf nicht meine aktuelle Station sein.
            #TODO auf Line Objekte umstellen
            if t.line.name in relevant_lines and t.target_station != tr.current_station and t.line.is_subway == tr.line.is_subway:
                #reason = str(t)
                can_arrive = False
        #if tr.line:
        #     print("Can train " + str(tr) + " arrive at " + str(self) + "?")
        #     if can_arrive:
        #         print("    Yes.")
        #     else: 
        #         print("    No, because of " + reason)
        return can_arrive