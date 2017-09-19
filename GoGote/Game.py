#! /usr/bin/env python3
import Board
import Player


class Game:
    """
    here be dragons
    """

    def __init__(self, player_black=Player.Player(),
                 player_white=Player.Player(), current_board=Board.Board(),
                 move_counter=0,
                 game_history={}, ko_hash_table={}):
        self.player_black = player_black
        self.player_white = player_white
        self.current_board = current_board
        self.move_counter = move_counter
        self.ko_hash_table = ko_hash_table
        self.game_history = game_history
        #  somehow implement an argument to choose current player.
        self.current_player = self.current_board.black

    def next_move(self, move, new_position):
        """
        increments the move
        adds move to game_history
        adds hash to ko_hash_table
        changes current_player
        initialzes new board with propper data
        """
        #  update game and hash table
        self.game_history[self.move_counter] = move
        self.ko_hash_table[self.move_counter] = hash(self.postion)
        #  change player
        if self.current_player == self.current_board.black:
            self.current_player = self.current_board.white
        elif self.current_player == self.current_board.white:
            self.current_player = self.current_board.black
        #  TODO: here check for ko and update accordingly
        #  update board position and move
        self.current_board.postion = new_position
        self.move_counter += 1


    # Methods to implement
    # def make_move(self, x, y):
    # def pass(self):
    # def check_ko(self):


# Testing area
if __name__ == "__main__":
    player1 = Player.Player("Max Mustermann", "10k")
    player2 = Player.Player("Marta Musterfrau", "8k")
    testgame = Game(player1, player2)
