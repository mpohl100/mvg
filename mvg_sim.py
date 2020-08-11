from network import Network
from simulation import Simulation, Config

def main():
    mvg = Network("MUC")
    config = Config(tie_line=True)
    simulation = Simulation(mvg, config, 5, 10)
    simulation.run()

if __name__=="__main__":
    main()