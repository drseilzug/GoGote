#! /usr/bin/env python3
import Board
import Player


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
        self.ko_hash_table[self.move_counter] = hash(current_board.postion)
        #  somehow implement an argument to choose current player.
        self.current_player = self.current_board.black

    def next_move(self, move, new_board):
        """
        increments the move
        adds move to game_history
        adds hash to ko_hash_table
        changes current_player
        updated the current_board
        """
        #  update game and hash table
        self.game_history[self.move_counter] = move
        #  change player
        if self.current_player == self.current_board.black:
            self.current_player = self.current_board.white
        elif self.current_player == self.current_board.white:
            self.current_player = self.current_board.black
        #  update board position and move_counter
        self.current_board = new_board
        self.move_counter += 1
        #  add new position to ko_hash_table
        self.ko_hash_table[self.move_counter] = \
            hash(self.current_board.postion)
        #  TODO: here check for ko and update accordingly

    # Methods to implement
    # def make_move(self, x, y):
    # def pass(self):
    # def check_ko(self):


# Testing area
if __name__ == "__main__":
    player1 = Player.Player("Max Mustermann", "10k")
    player2 = Player.Player("Marta Musterfrau", "8k")
    testgame = Game(player1, player2)
    new_position=self.current_board.position
    testgame.next_move((4,4), )
