from lib.config import Config, parse_config
from lib.simulation import Simulation
from network.network import Network
from network.schedule import Schedule, deduce_schedule


def test_schedule(network):
    schedule = Schedule(network)
    start_minutes = schedule.calc()
    print([str(s) for _, s in start_minutes.items()])



if __name__=="__main__":
    net = {
        'S1':["e", "Leuchtenbergring", "BergamLaim", "Riem", "Feldkirchen"],
        'S2': ["f", "Leuchtenbergring", "BergamLaim", "Gronsdorf", "Haar", "Zorneding"],
        'S3': ["Fantasie", "Land", "Trudering", "Ostbahnhof","Leuchtenbergring", "BergamLaim", "g"],
        #'S4': ["a", "b", "c", "d", "Fantasie", "Land", "h"],
    }
    #test_schedule(net)
    config = parse_config()
    network = Network(files=config.files)
    simulation = Simulation(network, config)
    #simulation.run()
    all_lines_dict = {line.name: line.all_stations for line in simulation.all_lines}
    start_minutes = deduce_schedule(all_lines_dict)

