#! /usr/bin/env python3
class Board:
    """
    Objects of this class represent the state of the go board at
    given move.

    Object has the following fields:
        size: an integer representing the board size.
        position: an size x size matrix whose values represent the status of
                  the according position.
                  Valid statuses:
                    0 :: empty
                    1 :: black
                    2 :: white
                    3 :: ko
        caps_black: an integer representing the black stones captured
        caps_white: an integer representing the white stones captured
        ko_status: boolean indecationg a position blocked by ko
        last_move: 2-Tuple with ints indicating the coordinates of the
                   last move. None if no last move.
        player: player to move
            1 :: black
            2 :: white
    """

    # Aliases
    empty = 0
    black = 1
    white = 2
    ko = 3

    def __init__(self, size=19, player=1,
                 caps_black=0, caps_white=0):
        # Initialize board matrix and other fields
        self.postion = [[0]*size for _ in range(size)]
        self.caps_black = caps_black
        self.caps_white = caps_white
        self.size = size
        self.ko_status = False
        self.player = player

    def __str__(self):
        """String representation of the board

        TODO: represent last move (maybe italic or smth)
        """
        repr = ""
        for line in self.postion:
            for col in line:
                if col == self.white:
                    repr += "O"
                elif col == self.black:
                    repr += "#"
            # feature removed until non stupid hash function TODO
            #    elif col == self.ko:
            #        repr += "*"
                else:
                    repr += "."
            repr += "\n"
        repr += "\n"
        if self.player == self.black:
            repr += "black to play"
        elif self.player == self.white:
            repr += "white to play"
        return repr

    def get_neighbours(self, x, y):
        """
        Returns a set with the coords of all neighbours of (x,y)
        as tupels
        """
        neighbours = set()
        for (x, y) in [(x+1, y), (x-1, y), (x, y-1), (x, y+1)]:
            if 0 <= x < self.size and 0 <= y < self.size:
                neighbours.add((x, y))
        return neighbours

    def set_position(self, x, y, status):
        """
        sets position (x, y) to status.

        legal inputs for status are:
            empty: 0, "e", "empty", self.empty
            black: 1, "b", "black", self.black
            white: 2, "w", "white", self.white
            ko:    3, "k", "ko",    self.ko
        """
        if status in (0, "e", "empty"):
            self.postion[x][y] = self.empty
        elif status in (1, "b", "black"):
            self.postion[x][y] = self.black
        elif status in (2, "w", "white"):
            self.postion[x][y] = self.white
        elif status in (3, "k", "ko"):
            self.postion[x][y] = self.ko
        else:
            raise ValueError('invalid argument for status')

    def is_empty(self, x, y):
        """
        checks if (x, y) has no stones on it
        """
        if self.postion[x][y] in [self.empty, self.ko]:
            return True
        else:
            return False

    def is_friend(self, x, y, x2, y2):
        """
        Checks whether (x, y) and (x2, y2) are of the same
        faction.
        """
        status1 = self.postion[x][y]
        status2 = self.postion[x2][y2]
        # empy positions shall be considered friedly to each other, incl ko
        for status in [status1, status2]:
            if status == self.ko:
                status = self.empty
        if status1 == status2:
            return True
        else:
            return False

    def get_group_info(self, x, y):
        """
        returns information on the group at (x, y) as a dictonary
            "libs":boolean True if group has liberties
            "stones":set contains coordiantes of stones belonging to group
                    only stones that were ckecked until liberty was found.
                    i.e. if libs == False stones contains whole group
        """
        to_check = {(x, y)}
        checked = set()
        libs = False
        while len(to_check) > 0:
            current_stone = to_check.pop()
            neighbours = self.get_neighbours(*current_stone) - checked
            for stone in neighbours:
                if self.is_friend(*current_stone, *stone):
                    to_check.add(stone)
                elif self.is_empty:
                    libs = True
                    break
            checked.add(current_stone)
        return {'libs': libs, 'group': checked}

    def check_legal(self):  # work in progress
        """
        returns True of Boad is a legal go position
        i.e. every stone belongs to a group with liberties
        False otherwise
        """
        stones = set()
        legal = True
        # get all coordiantes
        for x in range(self.size):
            for y in range(self.size):
                stones.add((x, y))
        # check each stone
        while len(stones) > 0:
            stone = stones.pop()
            (x, y) = stone
            if self.postion[x][y] == self.black or self.white:
                group_status = self.get_group_info(*stone)
                legal = legal and group_status["libs"]
                stones -= group_status["group"]
        return legal

    def kill_stone(self, x, y):
        if self.postion[x][y] == self.black:
            self.caps_black += 1
            self.set_position = self.empty
        elif self.postion[x][y] == self.white:
            self.caps_white += 1
            self.set_position = self.empty
        else:
            raise ValueError("cant kill nonexisting stone")

    def change_caps(self, n, color):
        """
        changes captured of color stones by integer n

        color::
            black: 1, "b", "black", self.black
            white: 2, "w", "white", self.white
        """
        # TODO imput error handeling
        if color in (self.black, "b", "black"):
            self.caps_black += n
        elif color in (self.white, "3", "white"):
            self.caps_white += n
        else:
            print("unknow color signature")  # TODO ERROR HANDELING

    def board_hash(self):
        """
        returns a hash of the str rep ob the board.
        until i know how to do it..... better....
        """
        return hash(str(self))


# Testing area
if __name__ == "__main__":
    testspiel = Board(size=8)

    testspiel.set_position(2, 4, "b")
    testspiel.postion[1][4] = 1
    testspiel.postion[3][5] = 1
    testspiel.postion[3][4] = 1
    testspiel.postion[6][6] = 2
    testspiel.postion[7][6] = 2
    print(testspiel)

    testspiel.check_legal()

    spiel2 = Board(size=1)
    spiel2.set_position(0, 0, 1)
    #  print(spiel2)
    #  spiel2.check_legal()
    print(testspiel.board_hash())
