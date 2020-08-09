import json
import copy
from collections import defaultdict
from typing import List, Set, Dict, Tuple, Optional

def read_network(city: str):
    #                 linename  purpose   list of stations
    network_raw: Dict[str, Dict[str, List[str]]] = {}
    # read U-Bahn
    with open('data/' + city + '_UBahn.json', 'r') as infile:
        ubahn_data = json.load(infile)
        network_raw = ubahn_data
    # read S-Bahn
    with open('data/' + city + '_SBahn.json', 'r') as infile:
        sbahn_data = json.load(infile)
        for lineName, stations in sbahn_data.items():
            network_raw[lineName] = stations
    return network_raw

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


def find_possible_switch_stations(lines_per_station: Dict[str, List[str]], line: str):
    ret: List[str] = []
    for station, lines in lines_per_station.items():
        if line in lines and len(lines) >= 2:
            ret.append(station)
    return ret

def find_all_switches(network: Dict[str, List[str]], lines_per_station: Dict[str, List[str]]):
    ret: Dict[str, List[str]] = {}
    for line, _ in network.items():
        ret[line] = find_possible_switch_stations(lines_per_station, line)
    return ret

def find_index_in_list(lst, el):
    for i, e in enumerate(lst):
        if e == el:
            return i
    return -1

def accumulate_stations(stations: List[str], start: str, dest: str):
    start_index: int = find_index_in_list(stations, start)
    dest_index: int = find_index_in_list(stations, dest)
    assert start_index >= 0
    assert dest_index >= 0
    ret: List[str] = []
    indeces: List[int] = []
    if start_index < dest_index:
        indeces = range(start_index, dest_index + 1)
    else:
        indeces = range(start_index, dest_index - 1, -1)
    for i in indeces:
        ret.append(stations[i])
    return ret

class Network:
    def __init__(self, city):
        self.all_info: Dict[str, Dict[str, List[str]]] = read_network(city)
        self.all_lines: Dict[str, List[str]] = {k:v['all_stations'] for k,v in self.all_info.items()}
        self.all_switches: Dict[str, List[str]] = {k:v['switches'] for k,v in self.all_info.items()}
        self.all_stations: List[str] = find_all_stations(self.all_lines)
        self.lines_per_station: Dict[str, List[str]] = index_network_by_line(self.all_lines)
        self.switches_per_line: Dict[str, List[str]] = find_all_switches(self.all_lines, self.lines_per_station)
        #self.all_routes = {}
        #for start in self.all_stations:
        #    for dest in self.all_stations:
        #        route = self.find_route(start,dest)
        #        self.all_routes[start + " | " + dest] = route
    


    def find_route(self, start: str, dest: str):
        route: List[str] = []
        start_lines: List[str] = self.lines_per_station[start]
        dest_lines: List[str] = self.lines_per_station[dest]
        common_lines: Set[str] = set(start_lines).intersection(set(dest_lines))
        if len(common_lines) > 0:
            routes: List[str] = []
            for common_line in common_lines:
                routes.append( accumulate_stations(self.all_lines[common_line], start, dest) )
            routes.sort(key=lambda x : len(x))
            return routes[0]
        
        for start_line in start_lines:
            for dest_line in dest_lines:
                start_switches: List[str] = self.switches_per_line[start_line]
                dest_switches: List[str] = self.switches_per_line[dest_line]
                common_switches: Set[str] = set(start_switches).intersection(set(dest_switches))
                if len(common_switches) > 0:
                    routes: List[str] = []
                    for common_switch in common_switches:
                        routes.append( [self.find_route(start, common_switch), self.find_route(common_switch, dest)] )
                    # erst sortieren wir nach der Länge der  Gesamtstrecke und dann nach der Länge des ersten Abschnitts
                    routes.sort(key=lambda x : (len(x[0]) + len(x[1]), len(x[0])) )
                    return routes[0][0] + routes[0][1]
        return route        
        # Falls zwei Stationen nicht mit einmal Umsteigen erreicht werden können, muss noch was gemacht werden
        #for start_line in start_lines:
        #    for dest_line in dest_lines:
        #        start_switches = self.switches_per_line[start_line]
        #        dest_switches = self.switches_per_line[dest_line]

class Config:
    def __init__(self, tie_line: bool):
        self.tie_line: bool = tie_line

class Simulation:
    def __init__(self, network: Network, config: Config, nb_subway: int = 4, nb_sbahn: int = 8):
        self.network: Network = network
        self.config: Config = config
        self.time: int = 0
        self.read_all_stations()
        self.read_all_lines()
        self.read_trains(nb_subway, nb_sbahn)

    def read_all_stations(self):
        self.all_stations: Dict[str, Station] = {}
        for station in self.network.all_stations:
            self.all_stations[station] = Station(station, self)

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

    def read_trains(self, nb_subway: int, nb_sbahn: int):
        self.trains: List[Train] = []
        nb_trains: int = 0
        for line in self.all_lines:
            stations: List[Station] = line.all_stations
            direction: int = 1
            nb_skip: int = nb_sbahn
            if line.is_subway:
                nb_skip = nb_subway
            for i in range(0,len(stations), nb_skip):
                train = Train(self.config, line, stations[i], direction, nb_trains)
                line.add_train(train)
                train.update()
                nb_trains += 1
                self.trains.append(train)
            direction = -1
            for i in range(len(stations) -1, 0, -nb_skip):
                train = Train(self.config, line, stations[i], direction, nb_trains)
                line.add_train(train)
                train.update()
                nb_trains += 1
                self.trains.append(train)

    def update(self):
        self.time += 1
        for t in self.trains:
            t.reset()
        for t in self.trains:
            t.update()

    def run(self):
        for _ in range(0,24*60):
            self.update()
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

class Station:
    def __init__(self, name: str, sim: Simulation):
        self.name: str = name
        self.sim: Simulation = sim
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
        relevant_lines: List[str] = self.lanes[train.current_station.name]
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

class Route:
    def __init__(self, from_station: Station, to_station: Station, linename: str):
        self.linename: str = linename
        self.from_station: Station = from_station
        self.to_station: Station = to_station

    def __eq__(self, other):
        return self.from_station == other.from_station and self.to_station == other.to_station
    def __hash__(self):
        return hash(str(self.from_station) + str(self.to_station))
    def __str__(self):
        return str(self.from_station) + ' -> ' + str(self.to_station)

def find_subline(stations: List[Station], route: Route, linename: str):
    ret: List[Station] = []
    from_index:int = find_index_in_list(stations, route.from_station)
    to_index: int = find_index_in_list(stations, route.to_station)
    if from_index < 0 or to_index < 0:
        raise ValueError(str(route) + " not found in line " + linename)
    if from_index < to_index:
        for i in range(from_index, to_index+1):
            ret.append(stations[i])
    else:
        for i in range(from_index, to_index-1, -1):
            ret.append(stations[i])
    return ret

def find_sublines(all_stations: List[Station], routes: List[Route], linename: str):
    sublines: Dict[Route, List[Station]] = {}
    for route in routes:
        sublines[route] = find_subline(all_stations, route, linename)
    return sublines

def find_routes(switches: List[Station], stations: List[Station], linename: str):
    routes: List[Route] = []
    if len(switches) == 0:
        return [Route(stations[0], stations[-1], linename)]
    for begin in switches:
        for end in switches:
            if begin != end:
                route = Route(begin, end, linename)
                # nur wenn eine Route durch den Tunnel geht wollen wir von dort nach dort S Bahnen fahren lassen
                subline: List[Station] = find_subline(stations, route, linename)
                subline_names: List[str] = [station.name for station in subline]
                if "Hauptbahnhof" in subline_names:
                    routes.append(route)
    return routes

class Line:
    def __init__(self, name: str, all_stations: List[Station], switches: List[Station]):
        self.name: str = name
        self.is_subway: bool = self.name.startswith('U')
        self.all_stations: List[Station] = all_stations
        self.switches: List[Station] = switches
        # TODO Management von Sublinien einbauen, niedrige Prio
        self.routes: List[Route] = find_routes(self.switches, self.all_stations, self.name)
        self.sublines: Dict[Route, List[Station]] = find_sublines(self.all_stations, self.routes, self.name)
        self.trains: List[Train] = []

    def __str__(self):
        return self.name

    def add_train(self, train):
        t: Train = train
        self.trains.append(t)


def find_next_station(current_station: Station, stations: List[Station], direction: int):
    current_index: int = find_index_in_list(stations, current_station)
    current_index += direction
    if current_index < 0:
        direction *= -1
        current_index += 2
    if current_index >= len(stations):
        direction *= -1
        current_index -= 2
    return stations[current_index], direction

class Train:
    def __init__(self, config: Config, line:Line, starting_station: Station, direction: int, number: int):
        self.number: int = number
        self.config = config
        self.line: Line = line
        self.stations: List[Station] = line.all_stations #todo make subline available here
        self.current_station: Station = starting_station
        self.target_station: Station = starting_station
        self.direction: int = direction
        self.waiting: bool = False # a train will always wait for one update call before leaving the station
        self.delay_per_station = defaultdict(int)
        self.delay_per_minute: List[int] = []
        self.delay = 0
        self.updated = False

    def __str__(self):
        return str(self.number) + ": " + str(self.line) + " " + str(self.current_station) + " -> " + str(self.target_station)

    def arrive(self):
        self.waiting = True
        self.current_station = self.target_station
        self.target_station, self.direction = find_next_station(self.current_station, self.stations, self.direction)
        self.current_station.register_arrival(self)

    def depart(self):
        next_station_free = self.can_depart()
        if next_station_free:
            self.current_station.register_departure(self)
            self.waiting = False
        else:
            self.delay_per_station[self.target_station] += 1
            self.delay += 1

    def can_depart(self):
            return self.target_station.can_arrive(self)

    def update(self):
        if self.updated: # nur einmal pro Minute der Simulation updaten.
            return
        if self.waiting:
            self.depart()
        else:
            self.arrive()
        self.delay_per_minute.append(self.delay)
        self.updated = True

    def reset(self):
        self.updated = False

def find_neighbour(lanes: Dict[str, List[str]], stations: List[str], index, line):
    if index >= 0 and index < len(stations):
        neighbour_station = stations[index]
        if neighbour_station in lanes:
            lanes[neighbour_station].append(line)
        else:
            lanes[neighbour_station] = [line]
    
def find_neighbours(network: Network, station: str):
    lanes: Dict[str, List[str]] = {}
    for line, stations in network.all_lines.items():
        index: int = find_index_in_list(stations, station)
        if index == -1:
            continue
        find_neighbour(lanes, stations, index - 1, line)
        find_neighbour(lanes, stations, index + 1, line)
    return lanes

def main():
    mvg = Network("MUC")
    config = Config(tie_line=True)
    simulation = Simulation(mvg, config, 4, 8)
    simulation.run()

if __name__=="__main__":
    main()