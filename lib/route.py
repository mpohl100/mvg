from network.network import find_index_in_list

from typing import List, Dict

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
