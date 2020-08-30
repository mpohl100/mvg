from network.network import find_index_in_list, find_index_in_list_pred
from network.startminute import StartMinute, TaktOffset

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


def is_connected(line1: Tuple[str, List[str]], line2: Tuple[str, List[str]]):
    stations1 = set(line1[1])
    stations2 = set(line2[1])
    return len(stations1.intersection(stations2)) >= 2

def find_subnetworks(lines: List[Tuple[str, List[str]]]):
    if len(lines) == 0:
        return [] # base case of recursion
    belongs_to_graph = [lines[0]]
    to_be_examined = []
    for line in lines[1:]:
        if is_connected(belongs_to_graph[0], line):
            belongs_to_graph.append(line)
        else:
            to_be_examined.append(line)
    ret = [belongs_to_graph]
    other_graphs = find_subnetworks(to_be_examined)
    if len(other_graphs) > 0:
        ret = ret + other_graphs
    return ret


class Schedule:
    def __init__(self, lines: Dict[str, List[str]]):
        list_of_lines = [(line,stations) for line, stations in lines.items()]
        self.subnetworks = find_subnetworks(list_of_lines)
        self.subnetworks = [{line:stations for line, stations in subnet} for subnet in self.subnetworks]
        self.subschedules = [SubSchedule(subnet) for subnet in self.subnetworks]

    def calc(self):
        ret: Dict[str, StartMinute] = {}
        for subschedule in self.subschedules:
            subminutes = subschedule.calc()
            ret = {**ret, **subminutes}
        return ret

class SubSchedule:
    def __init__(self, lines: Dict[str, List[str]]):
        self.lines = lines
        self.occurences = defaultdict(int)
        for _, line in self.lines.items():
            for station in line:
                self.occurences[station] += 1
        self.main_station_occurence = max(self.occurences.items(), key=itemgetter(1))

    def calc(self):
        start_minutes: Dict[str, StartMinute] = {}
        main_station = self.main_station_occurence[0]
        takt = self.main_station_occurence[1]
        #offsets = get_offsets(len(self.lines))
        i = 0
        p1_offsets: List[TaktOffset] = []
        for linename, line in self.lines.items():
            takt_offset_p1 = TaktOffset(linename, main_station, line, i*2, takt, +1) 
            i += 1
            takt_offset_p1.shift_ref_station(takt_offset_p1.all_stations[0])
            takt_offset_p1.shift_to_zero()
            p1_offsets.append(takt_offset_p1)
        i = 0
        m1_offsets: List[TaktOffset] = []
        for linename, line in self.lines.items():
            takt_offset_m1 = TaktOffset(linename, main_station, line, i*2, takt, -1) 
            i += 1
            takt_offset_m1.shift_ref_station(takt_offset_p1.all_stations[-1])
            takt_offset_m1.shift_to_zero()
            m1_offsets.append(takt_offset_m1)

        start_minutes: Dict[str, StartMinute] = {}
        for p1,m1 in zip(p1_offsets, m1_offsets):
            start_minutes[p1.linename] = StartMinute(p1,m1)
        print(start_minutes)
        return start_minutes
            # main_index = find_index_in_list(line, main_station)
            # offset = offsets[i]
            # i += 1
            # #print(line[main_index])
            # #print(offset)
            # positive_range = list(range(main_index + offset, len(line), +takt))
            # negative_range = list(range(main_index + offset, -len(line), -takt))
            # #print(positive_range)
            # #print(negative_range)
            # indeces = set(positive_range + negative_range)
            # indeces = sorted(indeces, key=lambda x: abs(x))
            # indeces = list(indeces)
            # #print(indeces)
            # #print([line[i] + ' ' + str(int(i / abs(i)) if i != 0 else str(0))  for i in indeces])
            # index_plus_one = -100000
            # for j in indeces:
            #     if j >= 0:
            #         index_plus_one = j
            #         break
            # index_minus_one = -1000000
            # for j in indeces:
            #     if j < 0:
            #         index_minus_one = j
            #         break
            # # zum Zeitpunkt null wollen wir, dass unsere Bahnen an den indizierten Bahnhöfen sind 
            # start_minute_plus_one = -index_plus_one*2
            # if start_minute_plus_one < 0:
            #     start_minute_plus_one += takt*2 
            # start_minute_minus_one = (index_minus_one+1)*2
            # if start_minute_minus_one < 0:
            #     start_minute_minus_one += takt*2

            # nb_plus_one = sum(map(lambda x: x >= 0, indeces))
            # nb_minus_one = sum(map(lambda x: x < 0, indeces))
            # #print(indeces)
            # #print(index_minus_one)
            # #print(nb_minus_one)
            # #print(index_plus_one)
            # #print(nb_plus_one) 
            # start_minutes[linename] = StartMinute(linename, start_minute_plus_one, nb_plus_one, start_minute_minus_one, nb_minus_one, takt*2)
        return start_minutes
        
        
def longest_common(all_stations1: List[str], all_stations2: List[str]):
    stations1 = set(all_stations1)
    stations2 = set(all_stations2)
    #TODO hier muss man auf Routen aufpassen, die sich zweimal überschneiden
    common_route = list(stations1.intersection(stations2))
    return common_route

def deduce_longest_common_lines(lines):
    from collections import namedtuple
    Key = namedtuple("Key", ["line1", "line2"])
    ret = {}
    for line1, all_stations1 in lines.items():
        for line2, all_stations2 in lines.items():
            if line1 != line2:
                longest_common_route = longest_common(all_stations1, all_stations2)
                if len(longest_common_route) >= 2:
                    key = Key(line1=line1, line2=line2)
                    ret[key] = longest_common_route
    #print(ret)
    return {k: v for k,v in sorted(ret.items(), key=lambda x: len(x[1]), reverse=True)}


def deduce_schedule(lines: Dict[str, List[str]]):
    #ret = {line: StartMinute(line.name,0,1,0,1,2) for line in lines.keys()}
    print('deduce_schedule')
    if len(lines) <= 1:
        return
    longest_common_lines = deduce_longest_common_lines(lines)
    already_merged_lines = set()
    new_lines = {}
    for key, stations in longest_common_lines.items():
        #print(str(key) + ' ' + str(len(stations)) )
        if key.line1 in already_merged_lines or key.line2 in already_merged_lines:
            continue
        already_merged_lines.add(key.line1)
        already_merged_lines.add(key.line2)
        line1 = lines[key.line1]
        line2 = lines[key.line2]
        scheduler = SubSchedule({key.line1: line1, key.line2: line2})
        start_minutes = scheduler.calc()
        print()
        for line, start_minute in start_minutes.items():
            #print(line)
            print(str(start_minute))
        new_lines[key.line1+';'+key.line2] = stations
    print()
    for line, stations in lines.items():
        if not line in already_merged_lines:
            new_lines[line] = stations
    deduce_schedule(new_lines)
    