#! /usr/bin/env python3
class Board:
    """
    Objects of this class represent the state of the go board at
    given move.

    Here be more docstring
    """

    # Aliases
    empty = 0
    black = 1
    white = 2

    def __init__(self, move_number=0, player=black, size=19,
                 caps_black=0, caps_white=0):
        # Initialize board matrix and other fields
        self.postion = [[0]*size for _ in range(size)]
        self.caps_black = caps_black
        self.caps_white = caps_white
        self.move_number = move_number

    def get_neighbors(self, x, y):
        """
        Returns a set with the coords of all neighbours of (x,y)
        """
        neighbours = set()
        for (x, y) in [(x+1, y), (x-1, y), (x, y-1), (x, y+1)]:
            if x <= self.size and y <= self.size:
                neighbours.add((x, y))
        return neighbours

# Testing area
