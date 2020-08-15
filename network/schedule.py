from network import find_index_in_list

from collections import defaultdict
from operator import itemgetter
from typing import Dict, List, Tuple

def get_offsets(nb: int):
    offsets = []
    for i in range(0, int(nb / 2 ) + 1):
        if i == 0:
            offsets.append(i)
        else:
            offsets.append(i)
            offsets.append(-i)
    return offsets

class StartMinute:
    def __init__(self, linename, start_minute_p1, nb_p1, start_minute_m1, nb_m1):
        self.linename:str = linename
        self.start_minute_p1 = start_minute_p1
        self.nb_p1 = nb_p1
        self.start_minute_m1 = start_minute_m1
        self.nb_m1 = nb_m1

    def __str__(self):
        return self.linename + ": p1 " + str(self.start_minute_p1) + " " + str(self.nb_p1) + "; m1 " + str(self.start_minute_m1) + " " + str(self.nb_m1) 
 

class Schedule:
    def __init__(self, lines: List[List[str]]):
        self.lines = lines
        self.occurences = defaultdict(int)
        for _, line in self.lines.items():
            for station in line:
                self.occurences[station] += 1
        self.main_station_occurence = max(self.occurences.items(), key=itemgetter(1))

    def calc(self):
        start_minutes: Dict[int, Tuple(int, int, int, int)] = {}

        main_station = self.main_station_occurence[0]
        takt = self.main_station_occurence[1]
        offsets = get_offsets(len(self.lines))
        i = 0
        for linename, line in self.lines.items():
            main_index = find_index_in_list(line, main_station)
            offset = offsets[i]
            i += 1
            #print(line[main_index])
            #print(offset)
            positive_range = list(range(main_index + offset, len(line), +takt))
            negative_range = list(range(main_index + offset, -len(line), -takt))
            #print(positive_range)
            #print(negative_range)
            indeces = set(positive_range + negative_range)
            indeces = sorted(indeces, key=lambda x: abs(x))
            indeces = list(indeces)
            #print(indeces)
            #print([line[i] + ' ' + str(int(i / abs(i)) if i != 0 else str(0))  for i in indeces])
            index_plus_one = -100000
            for j in indeces:
                if j >= 0:
                    index_plus_one = j
                    break
            index_minus_one = -1000000
            for j in indeces:
                if j < 0:
                    index_minus_one = j
                    break
            # zum Zeitpunkt null wollen wir, dass unsere Bahnen an den indizierten Bahnhöfen sind 
            start_minute_plus_one = -index_plus_one*2
            if start_minute_plus_one < 0:
                start_minute_plus_one += takt*2 
            start_minute_minus_one = (index_minus_one+1)*2
            if start_minute_minus_one < 0:
                start_minute_minus_one += takt*2

            nb_plus_one = sum(map(lambda x: x >= 0, indeces))
            nb_minus_one = sum(map(lambda x: x < 0, indeces))
            #print(indeces)
            #print(index_minus_one)
            #print(nb_minus_one)
            #print(index_plus_one)
            #print(nb_plus_one) 
            start_minutes[linename] = StartMinute(linename, start_minute_plus_one, nb_plus_one, start_minute_minus_one, nb_minus_one)
        return start_minutes

if __name__=="__main__":
    from network import Network
    network = {
        'S1':["Leuchtenbergring", "BergamLaim", "Riem", "Feldkirchen"],
        'S2': ["Leuchtenbergring", "BergamLaim", "Gronsdorf", "Haar", "Zorneding"],
        'S3': ["Fantasie", "Land", "Trudering", "Ostbahnhof","Leuchtenbergring", "BergamLaim"]
    }
    schedule = Schedule(network)
    start_minutes = schedule.calc()
    print([str(s) for _, s in start_minutes.items()])
        
        