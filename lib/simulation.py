from lib.config import Config
from lib.lane import Lane
from lib.line import Line
from lib.passenger import Passenger
from lib.route import find_route
from lib.station import Station
from lib.train import Train
from network.schedule import Schedule, StartMinute

from typing import Dict, List
from collections import defaultdict    

def interpolate(from_pos, to_pos, t):
    return from_pos + t * (to_pos-from_pos)

def is_visible(position, xlim, ylim):
    visible_x = xlim[0] <= position[0] and position[0] <= xlim[1]
    visible_y = ylim[0] <= position[1] and position[1] <= ylim[1]
    return visible_x and visible_y

class Simulation:
    def __init__(self, network: 'Network', config: Config):
        self.network: 'Network' = network
        self.config: Config = config
        self.time: int = 0
        self.read_all_stations()
        self.read_all_lines()
        self.deduce_lanes()
        self.trains: List[Train] = []
        self.start_minutes = {}
        if not self.config.deduce_schedule:
            self.read_trains()
        else:
            self.deduce_trains(True)
            self.deduce_trains(False)
        self.all_routes = []
        self.passengers = []
        if config.num_passengers_per_route > 0:
            self.create_passengers()
        self.graph = None
        self.positions = None
        self.xlim = None
        self.ylim = None
        self.minute = -1

    def read_all_stations(self):
        self.all_stations: Dict[str, Station] = {}
        for station in self.network.all_stations:
            self.all_stations[station] = Station(station)

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
    
    def deduce_lanes(self):
        for _, station in self.all_stations.items():
            station.deduce_lanes(self.network, self.all_stations, self.all_lines)
        self.all_lanes: List[Lane] = []
        for _, station in self.all_stations.items():
            self.all_lanes.extend([lane for _, lane in station.lanes.items()])
        # Test der Integrität des Netzwerks:
        set_lanes = set(self.all_lanes)
        if len(set_lanes) != len(self.all_lanes):
            raise Exception("Nicht einzigartige Lanes im Netzwerk vorhanden.")


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

    def deduce_trains(self, is_subway):
        dict_of_lines = {}
        dict_of_lines = {line.name: line.all_stations for line in self.all_lines if line.is_subway == is_subway} 
        self.schedule = Schedule(dict_of_lines)
        self.start_minutes.update(self.schedule.calc())
        nb_trains = 0
        for line in [ line for line in self.all_lines if line.is_subway == is_subway]:
            start_minute = self.start_minutes[line.name]
            line.set_start_minute(start_minute)
            for i in range(0, start_minute.taktoffset_p1.nb_trains()):
                self.add_train(0, line, 1, nb_trains, start_minute.taktoffset_p1.offset + i*start_minute.taktoffset_p1.takt)
                nb_trains += 1
            for i in range(0, start_minute.taktoffset_m1.nb_trains()):
                self.add_train(-1, line, -1, nb_trains, start_minute.taktoffset_m1.offset + i*start_minute.taktoffset_m1.takt)
                nb_trains += 1           

    def find_all_routes(self):
        all_routes: List[List['Route']]
        for _, from_station in self.all_stations.items():
            for _, to_station in self.all_stations.items():
                route = find_route(from_station, to_station, self.all_lines)
                all_routes.append(route)
        return all_routes

    def create_passengers(self):
        self.all_routes = self.find_all_routes()
        self.passengers: List[Passenger] = []
        passenger_number = 0
        for route in self.all_routes:
            for i in range(self.config.num_passengers_per_route):
                self.passengers.append(Passenger(route, passenger_number))
                passenger_number += 1

    def update(self):
        self.time += 1
        for t in self.trains:
            t.reset()
        for t in self.trains:
            t.update()
        for p in self.passengers:
            p.update()
        if self.config.show_net:
            self.print_net()

    def run(self):
        if self.config.show_net:
            import matplotlib.pyplot as plt
            plt.ion()
            plt.show()
            print("show plot")
        for self.minute in range(0, self.config.minutes):
            self.update()
        if self.config.verbosity >= 1:
            self.print_stats()

    def print_stats(self):
        self.delay_per_train()
        self.delay_per_station()
        import json
        print([str(s) for _, s in self.start_minutes.items()])
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

    def get_colors_of_lines(self):
        import matplotlib
        cmap = matplotlib.cm.get_cmap('Spectral')
        colors = {}
        i = 0
        for line in self.all_lines:
            colors[line.name] = cmap(i*1.0/len(self.all_lines))
            i += 1
        return colors

    def get_colors_of_trains(self):
        colors = self.get_colors_of_lines()
        colors_of_trains = {}
        for train in self.trains:
            color = colors[train.line.name]
            if color in colors_of_trains:
                colors_of_trains[color].append(train.line.name + "(" + str(train.number) + ")")
            else:
                colors_of_trains[color] = [train.line.name + "(" + str(train.number) + ")"]
        return colors_of_trains
        
    def print_net(self):
        import matplotlib.pyplot as plt
        from matplotlib.axes._axes import _log as matplotlib_axes_logger
        matplotlib_axes_logger.setLevel('ERROR')
        import networkx as nx
        if self.graph is None:
            self.graph = self.network.generate_networkx()
            self.positions = nx.spring_layout(self.graph)
            for train in self.trains:
                self.graph.add_node(train.line.name + "(" + str(train.number) + ")", label=train.line.name)
                self.positions[train.line.name + "(" + str(train.number) + ")"] = (0,0)
        colors_of_trains = self.get_colors_of_trains()
        for i in range(20):
            # draw the trains linearly interpolated with respect to their from and to stations
            for train in self.trains:
                if train.minutes >= train.start_minute and not train.waiting:
                    from_pos = self.positions[train.current_station.name]
                    to_pos = self.positions[train.target_station.name]
                    interpolated_pos = interpolate(from_pos, to_pos, i*1.0 / 20.0)
                    self.positions[train.line.name + "(" + str(train.number) + ")"] = interpolated_pos
            axes = plt.gca()
            plt.cla()
            with_labels=False
            visible_nodes = None
            if self.xlim and self.ylim: # to preserve the zoom and translations of the user
                axes.set_xlim(self.xlim)
                axes.set_ylim(self.ylim)
                # draw labels if it is zoomed in a lot
                delta_x = self.xlim[1] - self.xlim[0]
                delta_y = self.ylim[1] - self.ylim[0]
                if delta_x*delta_y < 0.25:
                    with_labels = True
                visible_nodes = []
                for nodename, position in self.positions.items():
                    if is_visible(position, self.xlim, self.ylim):
                        visible_nodes.append(nodename)
            if visible_nodes:
                nx.draw_networkx(self.graph, self.positions, nodelist=visible_nodes, with_labels=with_labels)
            else:
                nx.draw_networkx(self.graph, self.positions, with_labels=with_labels)
            for color, stations in colors_of_trains.items():
                nx.draw_networkx_nodes(self.graph, self.positions, nodelist=stations, node_color=color)
           
            plt.title('Graph Representation of Rail Map', size=15)
            plt.draw()
            plt.pause(0.001)
            self.ylim = axes.get_ylim()
            self.xlim = axes.get_xlim()