from typing import List

KB = 1024


class RAM:
    def __init__(self):
        # TODO byte vs int?
        self.memory = [0]*KB*2  # type: List[int]

    def get_byte(self, position):
        return self.memory[position]

    def set_byte(self, position, byte):
        self.memory[position] = byte
