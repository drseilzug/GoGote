#! /usr/bin/env python3


class Player:
    """
    A Player object contains informations on a Player.
    """

    def __init__(self, name="Generic Name", rank="?"):
        if isinstance(name, str) and isinstance(rank, str):
            self.rank = rank
            self.name = name
        else:
            raise TypeError("name and rank have to be strings")

    def set_name(self, name):
        """
        Sets player name.
        """
        if isinstance(name, str):
            self.name = name
        else:
            raise TypeError("name has to be a string")

    def set_rank(self, rank):
        """
        Sets player rank
        """
        if isinstance(rank, str):
            self.rank = rank
        else:
            raise TypeError("rank has to be a string")


# Testing area
if __name__ == "__main__":
    player = Player("John Dow", "4k")
