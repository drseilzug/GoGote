#! /usr/bin/env python3
class Board:
    """
    Objects of this class represent the state of the go board at
    given move.

    Here be more docstring
    """

    # Aliases
    empty = 0
    black = 1
    white = 2
    ko = 3

    def __init__(self, move_number=0, player=black, size=19,
                 caps_black=0, caps_white=0):
        # Initialize board matrix and other fields
        self.postion = [[0]*size for _ in range(size)]
        self.caps_black = caps_black
        self.caps_white = caps_white
        self.move_number = move_number
        self.size = size

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
                elif col == self.ko:
                    repr += "*"
                else:
                    repr += "."
            repr += "\n"
        return repr

    def get_neighbors(self, x, y):
        """
        Returns a set with the coords of all neighbours of (x,y)
        as tupels
        """
        neighbours = set()
        for (x, y) in [(x+1, y), (x-1, y), (x, y-1), (x, y+1)]:
            if 0 <= x < self.size and 0 <= y < self.size:
                neighbours.add((x, y))
        return neighbours

    def set_field(self, x, y, status):
        """
        sets field (x, y) to status.

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
            print("wrong input")  # TODO ERROR handeling

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
        # empy fields shall be considered friedly to each other, incl ko
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
            neighbours = self.neighbours(*current_stone) - checked
            for stone in neighbours:
                if self.is_friend(*current_stone, *stone):
                    to_check.update(stone)
                elif self.is_empty:
                    libs = True
                    break
            checked.update(current_stone)
        return {'libs': libs, 'group': checked}

    def kill_stone(self, x, y):
        if self.postion[x][y] == self.black:
            self.caps_black += 1
            self.set_field = self.empty
        elif self.postion[x][y] == self.white:
            self.caps_white += 1
            self.set_field = self.empty
        else:
            print("cant kill nonexisting stone")  # TODO: ERROR handeling


# Testing area
testspiel = Board(size=9)

testspiel.set_field(2, 4, testspiel.black)
testspiel.postion[1][4] = 1
testspiel.postion[3][5] = 1
testspiel.postion[3][4] = 1
testspiel.postion[6][6] = 2
testspiel.postion[7][6] = 2
print(testspiel)
