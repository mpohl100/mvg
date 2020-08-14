from network import find_index_in_list

from collections import defaultdict
from operator import itemgetter
from typing import List

def get_offsets(nb: int):
    offsets = []
    for i in range(0, int(nb / 2 ) + 1):
        if i == 0:
            offsets.append(i)
        else:
            offsets.append(i)
            offsets.append(-i)
    return offsets

class Schedule:
    def __init__(self, lines: List[List[str]]):
        self.lines = lines
        self.occurences = defaultdict(int)
        for line in self.lines:
            for station in line:
                self.occurences[station] += 1
        self.main_station_occurence = max(self.occurences.items(), key=itemgetter(1))

    def calc(self):
        main_station = self.main_station_occurence[0]
        takt = self.main_station_occurence[1]
        offsets = get_offsets(len(self.lines))
        for i, line in enumerate(self.lines):
            main_index = find_index_in_list(line, main_station)
            offset = offsets[i]
            print(line[main_index])
            print(offset)
            positive_range = list(range(main_index + offset, len(line), +takt))
            negative_range = list(range(main_index + offset, -len(line), -takt))
            print(positive_range)
            print(negative_range)



if __name__=="__main__":
    from network import Network
    network = [
        ["Ostbahnhof","Leuchtenbergring", "BergamLaim", "Riem", "Feldkirchen"],
        ["Leuchtenbergring", "BergamLaim", "Gronsdorf", "Haar"],
        ["Ostabhnhof","Leuchtenbergring", "BergamLaim", "Fantasie", "Land", "Trudering"]
    ]
    schedule = Schedule(network)
    schedule.calc()
        
        