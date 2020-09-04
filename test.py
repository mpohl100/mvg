from lib.config import Config, parse_config
from lib.simulation import Simulation
from network.network import Network
from network.schedule import Schedule, deduce_schedule


def test_schedule(network):
    schedule = Schedule(network)
    start_minutes = schedule.calc()
    print([str(s) for _, s in start_minutes.items()])



if __name__=="__main__":
    #test_schedule(net)
    config = parse_config()
    network = Network(files=config.files)
    simulation = Simulation(network, config)
    #simulation.run()
    #all_lines_dict = {line.name: [station.name for station in line.all_stations] for line in simulation.all_lines}
    #del all_lines_dict['S20']
    #start_minutes = deduce_schedule(all_lines_dict)
    from lib.route import RouteFinder
    from lib.station import Station
    from_station = Station("NeuperlachZentrum")
    to_station = Station("Mangfallplatz")
    route_finder = RouteFinder(simulation.all_lines, from_station, to_station)
    print(route_finder)

