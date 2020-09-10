from network.network import find_index_in_list_pred

from typing import List

class Passenger:
    def __init__(self, route: List['Route'], start_minute, number):
        self.route = route
        self.number = number
        self.minute = 0
        self.start_minute = start_minute
        self.current_leg = 0
        self.current_station = None
        self.current_train = None
        self.in_train = False

    def update(self):
        self.minute += 1
        if self.minute < self.start_minute or self.current_leg == len(self.route):
            return
        if not self.current_station:
            self.current_station = self.route[self.current_leg].from_station
            self.current_station.enter_passenger(self)
        if not self.in_train:
            # nachschauen ob ein Zug mit dem Liniennamen im Bahnhof ist
            linename = self.route[self.current_leg].linename
            train_index = find_index_in_list_pred(self.current_station.trains, lambda x: x.line.name == linename)
            if train_index != -1: 
                #noch überprüfen, dass es die richtige Richtung ist
                end_station_index = self.current_station.trains[train_index].get_end_station_index()
                target_station_index = self.current_station.trains[train_index].get_station_index(self.route[self.current_leg].to_station)
                current_station_index = self.current_station.trains[train_index].get_station_index(self.route[self.current_leg].from_station)
                if float(target_station_index - current_station_index) / float(end_station_index - current_station_index) > 0:
                    self.current_train = self.current_station.trains[train_index]
                    self.current_station.depart_passenger(self)
                    self.current_train.enter_passenger(self)
                    self.in_train = True
        else:
            target_station = self.route[self.current_leg].to_station
            if self.current_train.current_station == target_station:
                self.current_train.depart_passenger(self)
                target_station.enter_passenger(self)
                self.current_leg += 1
                self.in_train = False
                self.current_station = target_station





