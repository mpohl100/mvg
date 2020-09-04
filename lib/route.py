from network.network import find_index_in_list

from typing import List, Dict, Tuple

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
        return str(self.from_station) + ' -> ' + str(self.to_station)

def find_subline(stations: List['Station'], route: Route, linename: str):
    ret: List['Station'] = []
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

def find_sublines(all_stations: List['Station'], routes: List[Route], linename: str):
    sublines: Dict[Route, List['Station']] = {}
    for route in routes:
        sublines[route] = find_subline(all_stations, route, linename)
    return sublines

def find_routes(switches: List['Station'], stations: List['Station'], linename: str):
    routes: List[Route] = []
    if len(switches) == 0:
        return [Route(stations[0], stations[-1], linename)]
    for begin in switches:
        for end in switches:
            if begin != end:
                route = Route(begin, end, linename)
                # nur wenn eine Route durch den Tunnel geht wollen wir von dort nach dort S Bahnen fahren lassen
                subline: List['Station'] = find_subline(stations, route, linename)
                subline_names: List[str] = [station.name for station in subline]
                if "Hauptbahnhof" in subline_names:
                    routes.append(route)
    return routes

def find_lines(all_lines: List['Line'], station: 'Station'):
    return [line for line in all_lines if station in line.all_stations]

def find_all_possible_switches(lines: List['Line'], already_visited: List['Line']):
    ret: List[Tuple['Line', 'Station']]
    return ret

class RouteFinder: 
    def __init__(self, all_lines: List['Line'], from_station: 'Station', to_station: 'Station', route: List[Route] = [], already_visited: List['Line'] = []):
        self.all_lines = all_lines
        self.from_station = from_station
        self.to_station = to_station
        self.route: List[Route] = route
        self.already_visited = already_visited
        self.find_route()

    def find_route(self):
        from_lines = find_lines(self.all_lines, self.from_station)
        to_lines = find_lines(self.all_lines, self.to_station)
        common_lines = set(from_lines).intersection(set(to_lines))
        if len(common_lines) > 0:
            self.route.append(Route(self.from_station, self.to_station, list(common_lines)[0].name))
            return # wenn wir hier ankommen sind wir fertig 
        #TODO implement find_all_possible_switches
        possible_switches = List[Tuple['Line', 'Station']] = find_all_possible_switches(from_lines, self.already_visited)
        for line, station in possible_switches:
            self.already_visited.append(line)
            self.route.append(Route(self.from_station, station, line.name))
            new_route_finder = RouteFinder(self.all_lines, station, self.to_station, self.route, self.already_visited)
            if len(new_route_finder.route) > 0: # es wurde eine Route gefunden
                self.route.extend(new_route_finder.route)
                return
            else: # es wurde keine Route gefunden, weitermachen
                del self.route[-1]
        
        
