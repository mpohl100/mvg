from lib.config import Config, parse_config
from lib.simulation import Simulation
from network.networkdb import NetworkDb

def main():
    config = parse_config()
    networkdb = NetworkDb(files=config.files)
    simulation = Simulation(networkdb, config)
    simulation.run()

if __name__=="__main__":
    main()