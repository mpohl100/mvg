from tkinter import Tk, Canvas, mainloop, Image

from network.network import Network

def main():
    network = Network("MUC")
    graph = network.generate_graphviz(filename="MUC1")
    graph.render()
    graph2 = network.generate_graphviz(filename="MUC2")
    graph2.render()

    graph3 = network.generate_networkx()
    import matplotlib.pyplot as plt
    import networkx as nx
    plt.figure(figsize=(8, 6))
    nx.draw(graph3)
    plt.title('Graph Representation of Rail Map', size=15)
    plt.show()
    #master = Tk()
    #w = Canvas(master, width=700, height=600)
    #w.pack()
    #mainloop()

if __name__=="__main__":
    main()