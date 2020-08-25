from tkinter import Tk, Canvas, mainloop, Image

from lib.simulation import Simulation, Config, parse_config
from network.network import Network

def main():
    config=parse_config()
    config.show_net = True
    network = Network(files=config.files)
    simulation = Simulation(network, config)
    simulation.run()

if __name__=="__main__":
    main()