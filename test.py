from lib.config import Config, parse_config
from lib.simulation import Simulation
from network.networkdb import NetworkDb
from network.schedule import Schedule, deduce_schedule


def test_schedule(network):
    schedule = Schedule(network)
    start_minutes = schedule.calc()
    print([str(s) for _, s in start_minutes.items()])



if __name__=="__main__":
    #test_schedule(net)
    config = parse_config()
    networkdb = NetworkDb(files=config.files)
    simulation = Simulation(networkdb, config)
    #simulation.run()
    #all_lines_dict = {line.name: [station.name for station in line.all_stations] for line in simulation.all_lines}
    #del all_lines_dict['S20']
    #start_minutes = deduce_schedule(all_lines_dict)
    from lib.route import find_route_bfs, find_route_adj, AdjacencyList
    from lib.station import Station
    from_station = Station("Quiddestraße")
    to_station = Station("Universität")
    route = find_route_bfs(from_station, to_station, simulation.all_lines)
    #print([str(r) for r in route])
    route = find_route_bfs(to_station, from_station, simulation.all_lines)
    #print([str(r) for r in route])
    adj = AdjacencyList(simulation.all_lines)
    for _, from_station in simulation.all_stations.items():
        for _, to_station in simulation.all_stations.items():
            route = find_route_adj(from_station, to_station, adj)
            print('from ' + from_station.name + ' to ' + to_station.name + ':')
            for r in route:
                print('    ' + str(r))

