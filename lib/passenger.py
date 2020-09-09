from network.network import find_index_in_list_pred

from typing import List

class Passenger:
    def __init__(self, route: List['Route'], start_minute, number):
        self.route = route
        self.number = number
        self.minute = 0
        self.start_minute = start_minute
        self.current_leg = 0
        self.current_station = self.route[self.current_leg].from_station
        self.in_train = False

    def update(self):
        self.minute += 1
        if self.minute < self.start_minute:
            return
        if not self.in_train:
            # nachschauen ob ein Zug mit dem Liniennamen im Bahnhof ist
            linename = self.route[self.current_leg].linename
            train_index = find_index_in_list_pred(self.current_station.trains, lambda x: x.line.name == linename)
            if train_index != -1:
                train = self.current_station.trains[train_index]
                self.current_station.depart_passenger(self)
                train.enter_passenger(self)