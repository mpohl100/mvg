from network.network import Network
from lib.simulation import Simulation, Config

def main():
    mvg = Network("MUC")
    config = Config(10,20)
    simulation = Simulation(mvg, config)
    simulation.run()

if __name__=="__main__":
    main()