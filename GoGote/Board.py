#! /usr/bin/env python3
from GoColor import GoColor


class Board:
    """
    Objects of this class represent the state of the go board at
    given move.

    Object has the following fields:
        size: an integer representing the board size.
        position: an size x size matrix whose values represent the status of
                  the according position.
                  Valid statuses: (int :: enum)
                    0 :: GoColor.empty
                    1 :: GoColor.black
                    2 :: GoColor.white
                    3 :: GoColor.ko
        capsBlack: an integer representing the stones captured by Black
        capsWhite: an integer representing the stones captured by White
        koStatus: boolean indecationg a position blocked by ko
        player: player to move
            1 :: GoColor.black
            2 :: GoColor.white
    """

    def __init__(self, size=19, player=GoColor.black,
                 capsBlack=0, capsWhite=0):
        # Initialize board matrix and other fields
        self.postion = [[GoColor.empty]*size for _ in range(size)]
        self.capsBlack = capsBlack
        self.capsWhite = capsWhite
        self.size = size
        GoColor.koStatus = False
        self.player = player

    def __str__(self):
        """String representation of the board

        TODO: represent last move (maybe italic or smth)
        """
        repr = ""
        for line in self.postion:
            for col in line:
                if col == GoColor.white:
                    repr += "O"
                elif col == GoColor.black:
                    repr += "#"
            # feature removed until non stupid hash function TODO
            #    elif col == GoColor.ko:
            #        repr += "*"
                else:
                    repr += "."
            repr += "\n"
        repr += "\n"
        if self.player == GoColor.black:
            repr += "black to play"
        elif self.player == GoColor.white:
            repr += "white to play"
        return repr

    def getNeighbours(self, x, y):
        """
        Returns a set with the coords of all neighbours of (x,y)
        as tupels
        """
        neighbours = set()
        for (x, y) in [(x+1, y), (x-1, y), (x, y-1), (x, y+1)]:
            if 0 <= x < self.size and 0 <= y < self.size:
                neighbours.add((x, y))
        return neighbours

    def setPosition(self, x, y, status):
        """
        sets position (x, y) to status.

        legal inputs for status are:
            empty: 0, "e", "empty", GoColor.empty
            black: 1, "b", "black", GoColor.black
            white: 2, "w", "white", GoColor.white
            ko:    3, "k", "ko",    GoColor.ko
        """
        if status in (0, "e", "empty", GoColor.empty):
            self.postion[x][y] = GoColor.empty
        elif status in (1, "b", "black", GoColor.black):
            self.postion[x][y] = GoColor.black
        elif status in (2, "w", "white", GoColor.white):
            self.postion[x][y] = GoColor.white
        elif status in (3, "k", "ko", GoColor.ko):
            self.postion[x][y] = GoColor.ko
        else:
            raise ValueError('invalid argument for status')

    def getPosition(self, x, y):
        """Returns the status of stone at (x, y)"""
        return self.postion[x][y]

    def isEmpty(self, x, y):
        """
        checks if (x, y) has no stones on it
        """
        if self.postion[x][y] in [GoColor.empty, GoColor.ko]:
            return True
        else:
            return False

    def isFriend(self, x, y, x2, y2):
        """
        Checks whether (x, y) and (x2, y2) are of the same
        faction.
        """
        status1 = self.postion[x][y]
        status2 = self.postion[x2][y2]
        # empy positions shall be considered friedly to each other, incl ko
        for status in [status1, status2]:
            if status == GoColor.ko:
                status = GoColor.empty
        if status1 == status2:
            return True
        else:
            return False

    def getGroupInfo(self, x, y):
        """
        returns information on the group at (x, y) as a dictonary
            "libs":boolean True if group has liberties
            "group":set contains coordiantes of stones belonging to group
                    only stones that were ckecked until liberty was found.
                    i.e. if libs == False stones contains whole group
        """
        toCheck = {(x, y)}
        checked = set()
        libs = False
        while len(toCheck) > 0:
            currentStone = toCheck.pop()
            neighbours = self.getNeighbours(*currentStone) - checked
            for stone in neighbours:
                if self.isFriend(*currentStone, *stone):
                    toCheck.add(stone)
                elif self.isEmpty(*stone):
                    libs = True
                    checked.add(stone)
                    return {'libs': libs, 'group': checked}
            checked.add(currentStone)
        return {'libs': libs, 'group': checked}

    def checkLegal(self):
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
            if self.postion[x][y] == GoColor.black or GoColor.white:
                groupStatus = self.getGroupInfo(*stone)
                legal = legal and groupStatus["libs"]
                stones -= groupStatus["group"]
        return legal

    def killStone(self, x, y):
        """
        removes stone (x, y) from board and updates captures accordingly
        """
        if self.postion[x][y] == GoColor.white:
            self.capsBlack += 1
            self.setPosition(x, y, GoColor.empty)
        elif self.postion[x][y] == GoColor.black:
            self.capsWhite += 1
            self.setPosition(x, y, GoColor.empty)
        else:
            raise ValueError("cant kill nonexisting stone")

    def changeCaps(self, n, color):
        """
        changes captured of color stones by integer n

        color:
            black :: 1, GoColor.black
            white :: 2, GoColor.white
        """
        # TODO imput error handeling
        if color == GoColor.black:
            self.capsBlack += n
        elif color == GoColor.white:
            self.capsWhite += n
        else:
            raise ValueError("unknow color signature")

    def tooglePlayer(self):
        """toogels the player"""
        if self.player == GoColor.black:
            self.player = GoColor.white
        elif self.player == GoColor.white:
            self.player = GoColor.black

    def boardHash(self):
        """
        returns a hash of the str rep ob the board.
        until i know how to do it..... better....
        """
        return hash(str(self))

    def getHoshis(self):
        """
        returns a set of coordinates for the Hoshis depending on
        boardsize (atm 9, 13, 19)
        TODO: all baord sizes
        """
        if self.size == 9:
            return {(2, 2), (2, 5), (5, 2), (5, 5)}
        elif self.size == 13:
            return {(3, 3), (3, 9), (7, 7), (9, 3), (9, 9)}
        elif self.size == 19:
            return set((a, b) for a in [3, 9, 15] for b in [3, 9, 15])


# Testing area
if __name__ == "__main__":
    testspiel = Board(size=8)

    testspiel.setPosition(2, 4, "b")
    testspiel.postion[1][4] = 1
    testspiel.postion[3][5] = 1
    testspiel.postion[3][4] = 1
    testspiel.postion[6][6] = 2
    testspiel.postion[7][6] = 2
    testspiel.setPosition(1, 0, "b")
    testspiel.setPosition(0, 1, "b")
    testspiel.setPosition(0, 0, "w")
    print(testspiel)
    print("KILL")
    testspiel.killStone(0, 0)
    print(testspiel)
    testspiel2 = Board()
    print(testspiel2.getHoshis())
