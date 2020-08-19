from network.network import Network
from network.schedule import StartMinute
from lib.simulation import Simulation, Config

import copy
import matplotlib.pyplot as plt


def brute_force_schedule():
    mvg = Network("MUC")
    config = Config(5,10,500,0,True)
    simulation = Simulation(mvg, config)
    # Die automatisch erzeugten Startminuten merken
    start_minutes = simulation.start_minutes
    start_minutes_copy = copy.copy(start_minutes)
    results: Dict[int, Simulation] = {}
    for start_minute in start_minutes_copy:
        start_minute.start_minute_p1 = 0
        sim = Simulation(mvg, config, start_minutes_copy)
        sim.run()
        gesamt_delay = sum([t.delay for t in sim.trains])
        results[gesamt_delay] = sim
    


def main():
    mvg = Network("MUC")
    minutes = list(range(60, 1440, 60))
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