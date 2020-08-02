import json
import copy

def read_network():
    network_raw = {}
    # read U-Bahn
    with open('data/UBahn.txt', 'r') as infile:
        ubahn_data = json.load(infile)
        network_raw = ubahn_data
    # read S-Bahn
    with open('data/SBahn.txt', 'r') as infile:
        sbahn_data = json.load(infile)
        for lineName, stations in sbahn_data.items():
            network_raw[lineName] = stations
    return network_raw

def find_all_stations(network):
    all_stations = []
    for line, stations in network.items():
        all_stations.extend(stations)
    return set(all_stations)

def index_network_by_line(network):
    lines_per_station = {}
    for line, stations in network.items():
        for s in stations:
            if s in lines_per_station:
                lines_per_station[s].append(line)
            else:
                lines_per_station[s] = [line]
    return lines_per_station


def find_possible_switch_stations(lines_per_station, line):
    ret = []
    for station, lines in lines_per_station.items():
        if line in lines and len(lines) >= 2:
            ret.append(station)
    return ret

def find_all_switches(network, lines_per_station):
    ret = {}
    for line, stations in network.items():
        ret[line] = find_possible_switch_stations(lines_per_station, line)
    return ret

def find_index_in_list(lst, el):
    for i, e in enumerate(lst):
        if e == el:
            return i
    return -1

def accumulate_stations(stations, start, dest):
    start_index = find_index_in_list(stations, start)
    dest_index = find_index_in_list(stations, dest)
    assert start_index >= 0
    assert dest_index >= 0
    ret = []
    indeces = []
    if start_index < dest_index:
        indeces = range(start_index, dest_index + 1)
    else:
        indeces = range(start_index, dest_index - 1, -1)
    for i in indeces:
        ret.append(stations[i])
    return ret

class Network:
    def __init__(self):
        self.all_lines = read_network()
        self.all_stations = find_all_stations(self.all_lines)
        self.lines_per_station = index_network_by_line(self.all_lines)
        self.switches_per_line = find_all_switches(self.all_lines, self.lines_per_station)
        self.all_routes = {}
        #for start in self.all_stations:
        #    for dest in self.all_stations:
        #        route = self.find_route(start,dest)
        #        self.all_routes[start + " | " + dest] = route
    


    def find_route(self, start, dest):
        route = []
        start_lines = self.lines_per_station[start]
        dest_lines = self.lines_per_station[dest]
        common_lines = set(start_lines).intersection(set(dest_lines))
        if len(common_lines) > 0:
            routes = []
            for common_line in common_lines:
                routes.append( accumulate_stations(self.all_lines[common_line], start, dest) )
            routes.sort(key=lambda x : len(x))
            return routes[0]
        
        for start_line in start_lines:
            for dest_line in dest_lines:
                start_switches = self.switches_per_line[start_line]
                dest_switches = self.switches_per_line[dest_line]
                common_switches = set(start_switches).intersection(set(dest_switches))
                if len(common_switches) > 0:
                    routes = []
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

def find_next_station(current_station, stations, direction):
    current_index = find_index_in_list(stations, current_station)
    current_index += direction
    if current_index < 0:
        direction *= -1
        current_index += 2
    if current_index >= len(stations):
        direction *= -1
        current_index -= 2
    return stations[current_index]

class Train:
    def __init__(self, network, line, starting_station, direction):
        self.line = line
        self.stations = network.all_lines[line]
        self.current_station = starting_station
        self.taget_station = starting_station
        self.direction = direction
        self.waiting = True # a train will always wait for one update call before leaving the station
        self.network = network
        self.passengers = []

    def arrive(self):
        self.waiting = True
        self.current_station = self.target_station
        for passenger in self.passengers:
            passenger.leave(self.current_station)

    def leave(self):
        self.waiting = False
        self.target_station = find_next_station(self.current_station, self.stations, self.direction)

    def update(self):
        if self.waiting:
            self.leave()
        else:
            self.arrive()

def find_neighbours(network, station):
    ret = {}
    for line, stations in network.all_lines.items():
        index = find_index_in_list(stations, station)
        if index == -1:
            continue
        first_neighbour_index = index - 1
        if first_neighbour_index >= 0:
            first_neighbour = stations[first_neighbour_index]
            if first_neighbour in ret:
                ret[first_neighbour].append(line)
            else:
                ret[first_neighbour] = [line]
        second_neighbour_index = index + 1
        if second_neighbour_index < len(stations):
            second_neighbour = stations[second_neighbour_index]
            if second_neighbour in ret:
                ret[second_neighbour].append(line)
            else:
                ret[second_neighbour] = [line]
    return ret

class Station:
    def __init__(self, name, network: Network):
        self.name = name
        self.network = network
        self.lanes = find_neighbours(self.network, name)
        self.trains = []

    def register_arrival(self, train):
        pass

    def register_departure(self, train):
        pass

class Simulation:
    def __init__(self, network: Network):
        self.network = network
        self.trains = []
        self.time = 0
        for line, stations in self.network.all_lines.items():
            direction = 1
            for i in range(0,len(stations), 10):
                self.trains.append(Train(self.network,line, stations[i],direction))
            direction = -1
            for i in range(len(stations) -1, 0, -10):
                self.trains.append(Train(self.network,line, stations[i],direction))
        self.stations = []
        for station in self.network.all_stations:
            self.stations.append(Station(station, self.network))


    def update(self):
        self.time += 1
        for t in self.trains:
            t.update()

    def run(self):
        for i in range(0,24*60):
            print(self.time)
            self.update()




def main():
    mvg = Network()
    simulation = Simulation(mvg)
    simulation.run()

if __name__=="__main__":
    main()