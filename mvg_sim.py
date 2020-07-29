import json

class Station:
    def __init__(self, name: str):
        self.name = name

class Line:
    def __init__(self, lineName):
        self.name = lineName
        self.stations = []

class Network:
    def __init__(self):
        self.lines = []

def read_network():
    network_raw = {}
    # read U-Bahn
    with open('UBahn.txt', 'r') as infile:
        ubahn_data = json.load(infile)
        network_raw = ubahn_data
    # read S-Bahn
    with open('SBahn.txt', 'r') as infile:
        sbahn_data = json.load(infile)
        for lineName, stations in sbahn_data.items():
            network_raw[lineName] = stations
    return network_raw


def main():
    network = read_network()
    print(json.dumps(network))

if __name__=="__main__":
    main()