from tkinter import Tk, Canvas, mainloop, Image

from network.network import Network

def main():
    network = Network("MUC")
    graph = network.generate_graphviz(line="S2")
    graph.render()
    master = Tk()
    w = Canvas(master, width=700, height=600)
    w.pack()
    mainloop()

if __name__=="__main__":
    main()