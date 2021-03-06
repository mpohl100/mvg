from network.networkdb import find_index_in_list

from collections import defaultdict
from typing import Dict, List

def find_next_station(current_station: 'Station', stations: List['Station'], direction: int):
    current_index: int = find_index_in_list(stations, current_station)
    current_index += direction
    if current_index < 0:
        direction *= -1
        current_index += 2
    if current_index >= len(stations):
        direction *= -1
        current_index -= 2
    return stations[current_index], direction, stations[-1 if direction == 1 else 0]

class Train:
    def __init__(self, config: 'Config', line:'Line', starting_station: 'Station', direction: int, number: int, start_minute:int):
        self.number: int = number
        self.config = config
        self.line: 'Line' = line
        self.stations: List['Station'] = line.all_stations #todo make subline available here
        self.current_station: 'Station' = starting_station
        self.target_station: 'Station' = starting_station
        self.direction: int = direction
        self.end_station = self.stations[-1 if self.direction == 1 else 0]
        self.waiting: bool = False # a train will always wait for one update call before leaving the station
        self.delay_per_station = defaultdict(int)
        self.delay_per_minute: List[int] = []
        self.delay = 0
        self.updated = False
        self.start_minute = start_minute
        self.minutes = 0
        self.passengers: List['Passenger'] = []

    def __str__(self):
        return str(self.number) + ": " + str(self.line) + " " + str(self.end_station) + " (" + str(self.current_station) + ")"

    def arrive(self):
        if not self.target_station.can_arrive(self):
            self.delay_per_station[self.target_station] += 1
            self.delay += 1
            return         
        # Am Anfang der Simulation sind die current und die target station die Selben, deswegen gibt es in diesem Fall noch keine Lane   
        if self.current_station.name in self.target_station.lanes:
            lane = self.target_station.lanes[self.current_station.name]
            lane.register_departure(self)
        self.waiting = True
        self.current_station = self.target_station
        prev_direction = self.direction
        self.target_station, self.direction, self.end_station = find_next_station(self.current_station, self.stations, self.direction)
        if self.line.start_minute and prev_direction != self.direction:
            self.start_minute = self.line.start_minute.deduce_start(self.direction, self.minutes)
            #print(self.line.name + " " + str(self.number) + " minute " + str(self.minutes))
            #print("new start at " + str(self.start_minute))
        self.current_station.register_arrival(self)

    def depart(self):
        next_station_free = self.can_depart()
        if next_station_free:
            self.current_station.register_departure(self)
            lane = self.target_station.lanes[self.current_station.name]
            lane.register_arrival(self)
            self.waiting = False
        else:
            self.delay_per_station[self.target_station] += 1
            self.delay += 1

    def can_depart(self):
            lane = self.target_station.lanes[self.current_station.name]
            return lane.is_free_for(self)

    def update(self):
        if self.updated: # nur einmal pro Minute der Simulation updaten.
            return
        if self.minutes >= self.start_minute: 
            if self.waiting:
                self.depart()
            else:
                self.arrive()
        self.delay_per_minute.append(self.delay)
        self.updated = True
        self.minutes += 1

    def reset(self):
        self.updated = False

    def enter_passenger(self, passenger: 'Passenger'):
        self.passengers.append(passenger)

    def depart_passenger(self, passenger: 'Passenger'):
        passenger_index = find_index_in_list(self.passengers, passenger)
        if passenger_index == -1:
            raise ValueError("Passenger not found in train.")
        del self.passengers[passenger_index]

    def get_end_station_index(self):
        return len(self.stations)-1 if self.direction == 1 else 0

    def get_station_index(self, station: 'Station'):
        station_index = find_index_in_list(self.stations, station)
        #print(station)
        if station_index == -1:
            raise ValueError("Station " + str(station) + " not found in stations of train (" + str([str(stat) for stat in self.stations]) + ")")
        return station_index