#! /usr/bin/env python3


class Player:
    """
    A Player object contains informations on a Player.
    """

    def __init__(self, name="Generic Name", rank="?"):
        self.rank = rank
        self.name = name

    # TODO: Error handling for non sting inputs
    def set_name(self, name):
        """
        Sets player name.
        """
        self.name = name

    def set_rank(self, rank):
        """
        Sets player rank
        """
        self.rank = rank


# Testing area
if __name__ == "__main__":
    pass
