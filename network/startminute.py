from typing import List

def deduce_startminute(minute, start_minute, takt):
    nb_takt = (minute - start_minute) // takt # die Anzahl an bisher vergangenen Takten 
    return start_minute + takt * (nb_takt + 1)

class StartMinute:
    def __init__(self, linename: str, start_minute_p1: int, nb_p1: int, start_minute_m1: int, nb_m1: int, takt: int):
        self.linename:str = linename
        self.start_minute_p1: int = start_minute_p1 # start at minute of the simulation
        self.nb_p1: int = nb_p1                     # number of trains to start at start_minute_p1 + i * takt
        self.start_minute_m1: int = start_minute_m1 # start at minute of the simulation
        self.nb_m1: int = nb_m1                     # number of trains to start at start_minute_m1 + i * takt
        self.takt: int = takt                       # Takt

    def __str__(self):
        return self.linename + ": +1 (start " + str(self.start_minute_p1) + " nb " + str(self.nb_p1) + "); -1 (start " + str(self.start_minute_m1) + " nb " + str(self.nb_m1) + "); takt: " + str(self.takt)
 
    def deduce_start(self, direction: int, minute: int):
        if direction == 1:
            return deduce_startminute(minute, self.start_minute_p1, self.takt)
        elif direction == -1:
            return deduce_startminute(minute, self.start_minute_m1, self.takt)
        else: 
            raise ValueError("direction != {-1,1}")


class TaktOffset:
    def __init__(self, linename: str, ref_station: str, all_stations: List[str], offset: int, takt: int, direction: int):
        self.linename = linename
        self.ref_station = ref_station
        self.all_stations = all_stations
        self.offset = offset
        self.takt = takt
        self.direction = direction

    #def shift_ref_station(self, new_ref_station):

