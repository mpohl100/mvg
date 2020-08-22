from network.network import Network
from network.schedule import Schedule
from lib.simulation import Simulation, Config


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
    test_schedule(net)
    network = Network("TEST", net)
    config = Config(4,8,500,1,True)
    config.show_net = True
    simulation = Simulation(network, config)
    simulation.run()

