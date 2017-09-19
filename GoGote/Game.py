#! /usr/bin/env python3
import Board
import Player
from copy import copy as copy


class Game:
    """
    Fields:
        player_black:: a Player object containing Data on the black player
        player_white:: a Player object containing Data on the white player
        current_board:: a Board object containing the current board statuses
        move_counter:: an integer for the move count
        game_history:: a dict containing the moves keyed by the move_counter
        ko_hash_table:: a dict with hashes of the positions that have occured
                        keyed by the move_counter
        current_player:: the player whos move it is
        consecutive_passes:: counts the number of consecutive passes
    """

    def __init__(self, player_black=Player.Player(),
                 player_white=Player.Player(), current_board=Board.Board(),
                 move_counter=0,
                 game_history={}, ko_hash_table={}):
        self.player_black = player_black
        self.player_white = player_white
        self.current_board = current_board
        self.move_counter = move_counter
        self.game_history = game_history
        #  Initialize hash table and add starting position
        self.ko_hash_table = ko_hash_table
        self.ko_hash_table[self.move_counter] = self.current_board.board_hash()
        #  consecutive_passes always 0 for new board
        self.consecutive_passes = 0

    def next_move(self, move, new_board, passed=False):
        """
        increments the move
        adds move to game_history
        adds hash to ko_hash_table
        changes current_player
        updated the current_board
        updates consecutive_passes counter
        """
        #  update game and hash table
        self.game_history[self.move_counter] = move
        #  change player
        if self.current_board.player == self.current_board.black:
            self.current_board.player = self.current_board.white
        elif self.current_board.player == self.current_board.white:
            self.current_board.player = self.current_board.black
        #  update board position and move_counter
        self.current_board = new_board
        self.move_counter += 1
        #  add new position to ko_hash_table
        self.ko_hash_table[self.move_counter] = self.current_board.board_hash()
        #  TODO: here check for ko and update accordingly
        #  update/reset passing counter
        if passed:
            self.consecutive_passes += 1
        else:
            self.consecutive_passes = 0

    def check_for_ko(self, position):
        """
        checks if current_board is found in ko_hash_table

        returns True if found; False otherwise
        """
        return self.current_board.board_hash() in self.ko_hash_table.values

    def pass_move(self):
        """
        passing
        """
        self.next_move(None, self.current_board, True)
        #  TODO: remove Ko block maybe?
    # Methods to implement
    # def make_move(self, x, y):
    # def check_ko(self):


# Testing area
if __name__ == "__main__":
    player1 = Player.Player("Max Mustermann", "10k")
    player2 = Player.Player("Marta Musterfrau", "8k")
    testgame = Game(player1, player2)
    new_board = copy(testgame.current_board)
    new_board.set_position(4, 4, "b")
    testgame.next_move((4, 4), )
