from network.network import find_index_in_list, find_index_in_list_pred

import copy
from queue import Queue
from typing import List, Dict, Tuple, Set

class Route:
    def __init__(self, from_station: 'Station', to_station: 'Station', linename: str):
        self.linename: str = linename
        self.from_station: 'Station' = from_station
        self.to_station: 'Station' = to_station

    def __eq__(self, other):
        return self.from_station == other.from_station and self.to_station == other.to_station
    def __hash__(self):
        return hash(str(self.from_station) + str(self.to_station))
    def __str__(self):
        return str(self.from_station) + ' -> ' + str(self.to_station) + ' via line ' + str(self.linename)

def find_lines(all_lines: List['Line'], station: 'Station'):
    return [line for line in all_lines if station in line.all_stations]


class StationSwitch:
    def __init__(self, from_line: 'Line', station: 'Station', into_line: 'Line'):
        self.from_line = from_line
        self.station = station
        self.into_line = into_line

def find_all_possible_switches_per_line(line: 'Line', already_visited: List['Line'], starting_station: 'Station'):
    ret: List[StationSwitch] = []
    starting_index = find_index_in_list(line.all_stations, starting_station)
    indeces = []
    for i in range(1, len(line.all_stations)):
        indeces.append(i)
        indeces.append(-i)
    for i in indeces:
        if starting_index + i >= 0 and starting_index + i < len(line.all_stations):
            switch_lines = line.all_stations[starting_index + i].get_switch_lines()
            for switch_line in switch_lines:
                if not switch_line in already_visited:
                    ret.append(StationSwitch(from_line=line, station=line.all_stations[starting_index + i], into_line=switch_line))
                    already_visited.append(switch_line)
    return ret

def find_all_possible_switches(lines: List['Line'], already_visited: List['Line'], starting_station: 'Station'):
    ret: List[StationSwitch] = []
    for line in lines:
        ret.extend(find_all_possible_switches_per_line(line, already_visited, starting_station))
    return ret

class RouteFinder: 
    def __init__(self, all_lines: List['Line'], from_station: 'Station', to_station: 'Station', already_visited: List['Line'] = []):
        self.all_lines = all_lines
        self.from_station = from_station
        self.to_station = to_station
        self.current_route: List[Route] = []
        self.routes: List[List[Route]] = []
        self.already_visited = already_visited
        self.find_route()

    def find_route(self):
        from_lines = find_lines(self.all_lines, self.from_station)
        to_lines = find_lines(self.all_lines, self.to_station)
        common_lines = set(from_lines).intersection(set(to_lines))
        if len(common_lines) > 0:
            self.current_route.append(Route(self.from_station, self.to_station, list(common_lines)[0].name))
            self.routes.append(copy.copy(self.current_route))
            return # wenn wir hier ankommen sind wir fertig mit der Route
        possible_switches: List[StationSwitch] = find_all_possible_switches(from_lines, copy.copy(self.already_visited), self.from_station)
        for station_switch in possible_switches:
            self.already_visited.append(station_switch.into_line)
            self.current_route.append(Route(self.from_station, station_switch.station, station_switch.from_line.name))
            new_route_finder = RouteFinder(self.all_lines, station_switch.station, self.to_station, self.already_visited)
            if len(new_route_finder.routes) > 0: # es wurde eine Route gefunden
                for route in new_route_finder.routes:
                    self.routes.append(copy.copy(self.current_route) + copy.copy(route))
            # es wurden alle Routen zu dem Anfang in current_route gefunden, weitermachen
            del self.current_route[-1]
        
def find_route(from_station: 'Station', to_station: 'Station', all_lines: List['Line']):
    route_finder = RouteFinder(all_lines, from_station, to_station, [])
    routes = list(sorted(route_finder.routes, key=lambda x: len(x)))
    if len(routes) > 0:
        return routes[0]
    return [Route(from_station, to_station, 'no line')]     

class AdjacencyList:
    def __init__(self, all_lines: List['Line']):
        self.all_stations: Set['Station'] = set()
        for line in all_lines:
            for station in line.all_stations:
                self.all_stations.add(station)
        self.all_stations: List['Station'] = list(self.all_stations)
        self.graph = []
        for station in self.all_stations:
            neighbours = []
            for neighbour_station, _ in station.lanes.items():
                index = find_index_in_list_pred(self.all_stations, lambda x: x.name == neighbour_station)
                neighbours.append(index)
            self.graph.append(neighbours)

    def get_index(self, station: 'Station'):
        return find_index_in_list(self.all_stations, station)

    def N(self):
        return len(self.all_stations)

def solve_bfs(from_station: 'Station', adjacency_list: AdjacencyList):
    first_station_index = adjacency_list.get_index(from_station)
    queue = Queue()
    queue.put(first_station_index)
    visited = [False] * adjacency_list.N()
    visited[first_station_index] = True
    prev = [None] * adjacency_list.N()
    while not queue.empty():
        node = queue.get()
        neighbours = adjacency_list.graph[node]
        for neighbour in neighbours:
            if not visited[neighbour]:
                queue.put(neighbour)
                visited[neighbour] = True
                prev[neighbour] = node
    return prev
        
def reconstruct_path(prev, from_station: 'Station', to_station: 'Station', adjacency_list: AdjacencyList):
    to_index = adjacency_list.get_index(to_station)
    path_index = [to_index]
    at = prev[to_index]
    while at != None:
        path_index.append(at)
        at = prev[at]
    path: List['Station'] = []
    for path_i in reversed(path_index):
        path.append(adjacency_list.all_stations[path_i])
    if path[0] == from_station:
        return path
    return []

def deduce_longest_route(path: List['Station']):
    if len(path) == 1:
        raise ValueError("path must have at least two members")
    potential_lines: Set[str] = set(['dummy'])
    index = 0
    route = Route(path[index], path[index], '')
    while(len(potential_lines) > 0 and index < len(path) - 1):
        if index == 0:
            potential_lines = set(path[index].lanes[path[index+1].name].lines)
        else:
            potential_lines = potential_lines.intersection(set(path[index].lanes[path[index+1].name].lines))
        if len(potential_lines) > 0:
            route.to_station = path[index+1]
            route.linename = list(potential_lines)[0].name
            index += 1
    return route, index
    

def deduce_shortest_lines(path: List['Station']):
    ret: List['Route'] = []
    next_index = 0
    while(next_index < len(path) - 1):
        route, offset = deduce_longest_route(path[next_index:])
        next_index += offset
        ret.append(route)
    return ret

prev_cache: Dict['Station', List[int]] = {}

def find_route_adj(from_station: 'Station', to_station: 'Station', adj: 'AdjacencyList'):
    if not from_station in prev_cache:
        prev = solve_bfs(from_station, adj)
        prev_cache[from_station] = prev
    path = reconstruct_path(prev_cache[from_station], from_station, to_station, adj)
    return deduce_shortest_lines(path)

def find_route_bfs(from_station: 'Station', to_station: 'Station', all_lines: List['Line']):
    adjacency_list = AdjacencyList(all_lines)
    return find_route_adj(from_station, to_station, adjacency_list)