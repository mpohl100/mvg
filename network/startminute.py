from network.network import find_index_in_list

from typing import List

class TaktOffset:
    def __init__(self, linename: str, ref_station: str, all_stations: List[str], offset: int, takt: int, direction: int):
        self.linename = linename
        self.ref_station = ref_station
        self.all_stations = all_stations
        self.offset = offset
        self.takt = takt
        self.direction = direction

    def shift_ref_station(self, new_ref_station):
        current_ref_index = find_index_in_list(self.all_stations, self.ref_station)
        new_ref_index = find_index_in_list(self.all_stations, new_ref_station)
        #TODO use real distances between stations
        self.offset += (new_ref_index - current_ref_index) * 2
        self.ref_station = new_ref_station

    def shift_to_zero(self):
        if self.offset < 0:
            self.offset += self.takt * (-self.offset // self.takt + 1)
        elif self.offset >= self.takt:
            self.offset -= (self.offset // self.takt) * self.takt

    def nb_trains(self):
        return len(self.all_stations) // (self.takt // 2)

    def __str__(self):
        return self.linename + ' ' + self.ref_station.name + ': ' + str(self.direction) + ' ' + str(self.offset) + ' (' + str(self.takt) + ')' 

def deduce_startminute(minute, start_minute, takt):
    nb_takt = (minute - start_minute) // takt # die Anzahl an bisher vergangenen Takten 
    return start_minute + takt * (nb_takt + 1)

class StartMinute:
    def __init__(self, taktoffset_p1: TaktOffset, taktoffset_m1: TaktOffset):
        self.taktoffset_p1 = taktoffset_p1
        self.taktoffset_m1 = taktoffset_m1

    def __str__(self):
        return str(self.taktoffset_p1) + " " + str(self.taktoffset_m1)
 
    def deduce_start(self, direction: int, minute: int):
        if direction == 1:
            return deduce_startminute(minute, self.taktoffset_p1.offset, self.taktoffset_p1.takt)
        elif direction == -1:
            return deduce_startminute(minute, self.taktoffset_m1.offset, self.taktoffset_m1.takt)
        else: 
            raise ValueError("direction != {-1,1}")


