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
        #  update board position and move_counter
        self.current_board = new_board
        self.move_counter += 1
        #  change player
        if self.current_board.player == self.current_board.black:
            self.current_board.player = self.current_board.white
        elif self.current_board.player == self.current_board.white:
            self.current_board.player = self.current_board.black
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

    def play_move(self, x, y):
        """
        plays a move at (x, y)
        """
        #  create temp board
        temp_board = copy(self.current_board)
        if not temp_board.is_empty(x, y):
            #  TODO define IllegalMoveError
            raise ValueError("can only play on empty positions")
        #  place stone on temp board
        temp_board.set_position(x, y, temp_board.player)
        neighbours = temp_board.get_neighbours(x, y)
        #  remove empty field form neighbours
        to_remove = set()
        for stone in neighbours:
            if temp_board.is_empty(*stone):
                to_remove.add(stone)
        neighbours -= to_remove
        #  remove friendly stones --> left with enemies
        to_remove = set()
        for stone in neighbours:
            if temp_board.is_friend(x, y, *stone):
                    to_remove.add(stone)
        neighbours -= to_remove
        #  check and kill neighbouring enemy groups if neccacary
        checked = set()
        for stone in neighbours:
            print("STONE:", stone, "checked:", checked)
            if stone in checked:
                continue
            group_info = temp_board.get_group_info(*stone)
            print("group_info", group_info["libs"])
            #  kill dead stones
            if not group_info["libs"]:
                for stone in group_info["group"]:
                    temp_board.kill_stone(*stone)
            checked.union(group_info["group"])
        #  check if played stone has liberties
        # group_info = temp_board.get_group_info(x, y)
        if not temp_board.get_group_info(x, y)["libs"]:
            raise ValueError("IllegalMoveError: no liberties")
        else:
            #  move gets played
            self.next_move((x, y), temp_board)

    # Methods to implement
        # def make_move(self, x, y):
        # def check_ko(self):


# Testing area
if __name__ == "__main__":
    player1 = Player.Player("Max Mustermann", "10k")
    player2 = Player.Player("Marta Musterfrau", "8k")
    testgame = Game(player1, player2)
    testgame.play_move(0, 1)
    print("--")
    testgame.play_move(0, 0)
    print("------------------------------------")
    testgame.play_move(1, 0)
    testgame.play_move(0, 0)
    print(testgame.current_board)
