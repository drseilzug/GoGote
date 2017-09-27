#! /usr/bin/env python3
from enum import Enum


class GoColor(Enum):
    """
    Enums for the different statuses on the go board and playerColors
    empty, e :: 0
    black, b :: 1
    white, w :: 2
    ko, k :: 3
    """
    empty = 0
    e = 0
    black = 1
    b = 1
    white = 2
    w = 2
    ko = 3
    k = 3


# Testing area
if __name__ == "__main__":
    pass
