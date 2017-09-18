#! /usr/bin/env python3
import Board
import Player


class Game:
    """
    here be dragons
    """

    def __init__(self, player_black=Player.Player(),
                 player_white=Player.Player(), starting_board=Board.Board()):
        self.player_black = player_black
        self.player_white = player_white
        self.current_board = starting_board

    # Methods to implement
    # def make_move(self, x, y):
    # def pass(self):
    # def check_ko(self):


# Testing area
if __name__ == "__main__":
    player1 = Player.Player("Max Mustermann", "10k")
    player2 = Player.Player("Marta Musterfrau", "8k")
