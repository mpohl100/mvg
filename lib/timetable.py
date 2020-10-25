from network.networkdb import find_index_in_list_pred
from network.startminute import TaktOffset, StartMinute

from typing import List, Dict
from copy import copy
from collections import defaultdict
from operator import itemgetter

class MergeType:
    BEFORE = 1
    ZIP_BEFORE = 2
    ZIP_AFTER = 3
    AFTER = 4

def deduce_local_centers(line_centers, merge_type: MergeType):
    all_centers = []
    for line1 in line_centers:
        for line2 in line_centers:
            if line1 == line2:
                continue
            new_center = list(set(line1['center']).intersection(set(line2['center'])))
            # bisher ist das nur MergeType.BEFORE
            new_lines = []
            if merge_type == MergeType.BEFORE:
                new_lines = copy(line1['lines'])
                new_lines.extend(copy(line2['lines']))
            elif merge_type == MergeType.AFTER:
                new_lines = copy(line2['lines'])
                new_lines.extend(copy(line1['lines'])) 
            elif merge_type == MergeType.ZIP_BEFORE:
                for i in range(max(len(line1['lines']), len(line2['lines']))):
                    if i < len(line1['lines']):
                        new_lines.append(line1['lines'][i])
                    if i < len(line2['lines']):
                        new_lines.append(line2['lines'][i])
            elif merge_type == MergeType.ZIP_AFTER:
                for i in range(max(len(line1['lines']), len(line2['lines']))):
                    if i < len(line2['lines']):
                        new_lines.append(line2['lines'][i])
                    if i < len(line1['lines']):
                        new_lines.append(line1['lines'][i])
            all_centers.append({'lines': new_lines, 'center': new_center})

    result = []
    already_inserted_lines = set()
    for line_center in sorted(all_centers, key=lambda el: len(el['center']), reverse=True):
        already_treated = already_inserted_lines.intersection(set(line_center['lines']))
        if len(already_treated) > 0:
            continue
        for line in line_center['lines']:
            already_inserted_lines.add(line)
        result.append(line_center)

    for line_center in line_centers:
        already_treated = already_inserted_lines.intersection(set(line_center['lines']))
        if len(already_treated) > 0:
            continue
        result.append(line_center)

    return result

class TimeTable:
    def __init__(self, lines: List['Line'], merge_type: MergeType):
        # it is assumed that all the input lines have a common center
        self.lines = lines
        self.merge_type = merge_type
        self.find_center()
        self.sort()

    def filter_lines(self):
        self.center_lines = []
        self.other_lines = []
        for line in self.lines:
            index = find_index_in_list_pred(line.all_stations, lambda el: el.name == self.main_station.name)
            if index == -1:
                self.other_lines.append(line)
            else:
                self.center_lines.append(line)

    def find_center(self):
        occurences = defaultdict(int)
        for line in self.lines:
            for station in line.all_stations:
                occurences[station] += 1
        main_station_occurence = max(occurences.items(), key=itemgetter(1))
        self.main_station = main_station_occurence[0]
        self.filter_lines()

    def sort(self):
        self.result = [{'lines': [line], 'center': line.all_stations } for line in self.center_lines]
        prev_size = len(self.result)*2
        while len(self.result) >= 1 and prev_size != len(self.result):
            for r in self.result:
                print([line.name for line in r['lines']])
                print(len(r['center']))
            print()
            prev_size = len(self.result)
            self.result = deduce_local_centers(self.result, self.merge_type)
       

    def get_startminutes(self):
        start_minutes: Dict[str, StartMinute] = {}
        main_station = self.main_station
        takt = 2 * len(self.center_lines)
        i = 0
        p1_offsets: List[TaktOffset] = []
        for line in self.result[0]['lines']:
            stations = line.all_stations
            takt_offset_p1 = TaktOffset(line.name, main_station, stations, i*2, takt, +1) 
            i += 1
            takt_offset_p1.shift_ref_station(takt_offset_p1.all_stations[0])
            takt_offset_p1.shift_to_zero()
            p1_offsets.append(takt_offset_p1)
        i = 0
        m1_offsets: List[TaktOffset] = []
        for line in self.result[0]['lines']:
            stations = line.all_stations
            takt_offset_m1 = TaktOffset(line.name, main_station, stations, i*2, takt, -1) 
            i += 1
            takt_offset_m1.shift_ref_station(takt_offset_m1.all_stations[-1])
            takt_offset_m1.shift_to_zero()
            m1_offsets.append(takt_offset_m1)

        start_minutes: Dict[str, StartMinute] = {}
        for p1,m1 in zip(p1_offsets, m1_offsets):
            start_minutes[p1.linename] = StartMinute(p1,m1)
        #print(start_minutes)
        return start_minutes
            