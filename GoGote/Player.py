#! /usr/bin/env python3


class Player:
    """
    A Player object contains informations on a Player.
    """

    def __init__(self, name="Generic Name", rank="?"):
        self.rank = rank
        self.name = name
