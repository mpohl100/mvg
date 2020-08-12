from typing import List

class Lane:
    def __init__(self, from_station: 'Station', to_station: 'Station', lines: List[str]):
        self.from_station: 'Station' = from_station
        self.to_station: 'Station' = to_station
        self.lines: List[str] = lines
        self.is_double: bool = True # Doppelgleis