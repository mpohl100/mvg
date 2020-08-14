from collections import defaultdict
from operator import itemgetter
from typing import List

class Schedule:
    def __init__(self, lines: List[List[str]]):
        self.lines = lines
        self.occurences = defaultdict(int)
        for line in self.lines:
            for station in line:
                self.occurences[station] += 1
        self.takt = max(self.occurences.items(), key=itemgetter(1))

    def calc(self):
        


if __name__=="__main__":
    from network import Network
    network = [
        ["Leuchtenbergring", "BergamLaim", "Riem", "Feldkirchen"],
        ["Leuchtenbergring", "BergamLaim", "Gronsdorf", "Haar"]
    ]
    schedule = Schedule(network)
    schedule.calc()
        
        