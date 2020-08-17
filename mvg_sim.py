from network.network import Network
from lib.simulation import Simulation, Config

import matplotlib.pyplot as plt

def main():
    mvg = Network("MUC")
    minutes = list(range(60, 120, 60))
    delays = []
    for minute in minutes:
        config = Config(5,10, minute, 1, True)
        simulation = Simulation(mvg, config)
        simulation.run()
        delays.append(simulation.sum_delay())
    plt.plot(minutes, delays, color='blue')
    plt.show()



if __name__=="__main__":
    main()