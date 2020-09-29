from lib.config import Config, parse_config
from lib.simulation import Simulation
from network.network import Network

def main():
    config = parse_config()
    network = Network(files=config.files)
    simulation = Simulation(network, config)
    simulation.run()

if __name__=="__main__":
    main()