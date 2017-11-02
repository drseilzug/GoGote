#! /usr/bin/env python3
import Board
from GoColor import GoColor
import Player
from sgfmill import sgf
from copy import deepcopy
from GoExceptions import IllegalMoveError, KoError


class Game:
    """
    Fields:
        playerBlack:: a Player object containing Data on the black player
        playerWhite:: a Player object containing Data on the white player
        currentBoard:: a Board object containing the current board statuses
        moveCounter:: an integer for the move count
        sgf :: an sgf_game object to record and save the game
        koHashTable:: a dict with lists of boards that have occured
                        keyed by the board hashes
        consecutivePasses:: counts the number of consecutive passes
    """

    def __init__(self, playerBlack=Player.Player(),
                 playerWhite=Player.Player(), currentBoard=Board.Board(),
                 moveCounter=0,
                 sgfHist=None, koHashTable={}):
        self.playerBlack = playerBlack
        self.playerWhite = playerWhite
        self.currentBoard = currentBoard
        self.moveCounter = moveCounter
        self.setKo = None
        #  Initialize hash table and add starting position
        self.koHashTable = koHashTable
        self.koHashTable[self.currentBoard.boardHash()] = [self.currentBoard]
        #  consecutivePasses always 0 for new board
        self.consecutivePasses = 0

        # create empty sgf_game on default
        self.sgfHist = sgfHist
        if sgfHist is None:
            self.sgfHist = sgf.Sgf_game(self.currentBoard.size)

    def nextMove(self, move, newBoard, passed=False):
        """
        move :: (int, int)
        newBoard :: Board
        passed :: bool

        increments the move
        adds move to sgf
        adds hash to koHashTable
        changes current Player
        updated the currentBoard
        updates consecutivePasses counter
        """
        #  update sgf
        self.addMoveSgf(move)
        #  update board position and moveCounter
        self.currentBoard = newBoard
        self.moveCounter += 1
        #  change player
        self.currentBoard.tooglePlayer()
        # set last move
        self.currentBoard.setLastMove(*move)
        #  add new position to koHashTable
        self.addBoardToHash()
        # check for ko blocked
        if self.setKo:
            if self.koBlockTest(self.setKo):
                self.currentBoard.ko = self.setKo
            else:
                self.currentBoard.ko = None
            self.setKo = None
        else:
            self.currentBoard.ko = None
        #  update/reset passing counter
        if passed:
            self.consecutivePasses += 1
        else:
            self.consecutivePasses = 0

    def addBoardToHash(self):
        """
        Adds self.currentBoard to self.koHashTable
        """
        newHash = self.currentBoard.boardHash()
        boardCopy = deepcopy(self.currentBoard)
        if newHash in self.koHashTable:
            self.koHashTable[newHash].append(boardCopy)
        else:
            self.koHashTable[newHash] = [boardCopy]

    def checkForKo(self, board):
        """
        checks if board is found in koHashTable
        when otherPlayer == True it checks if the board is in the table for
        the Player whos move it is not in board
        TODO: default value for board is self.currentBoard
        returns True if found; False otherwise

        TODO: implement toogle for KO/SUPERKO/no KO
        """
        koStatus = False
        newHash = board.boardHash()
        if newHash in self.koHashTable:
            for koBoard in self.koHashTable[newHash]:
                if koBoard.position == board.position:
                    koStatus = True
        return koStatus

    def koBlockTest(self, potKoMove):
        """
        checks if potKoMove is blocked to play on board due to ko
        and marks it accordingly.
        """
        if not self.currentBoard.isEmpty(*potKoMove):
            return False
        noKo = False
        self.currentBoard.setPosition(*potKoMove, self.currentBoard.player)
        for stone in self.currentBoard.getNeighbours(*potKoMove):
            noKo = noKo or self.currentBoard.isFriend(*stone, *potKoMove)
            noKo = noKo or self.currentBoard.isEmpty(*stone)
        self.currentBoard.setPosition(*potKoMove, GoColor.empty)
        return not noKo

        # tempGame = deepcopy(self)
        # try:
        #     tempGame.playMove(potKoMove)
        # except(KoError):
        #     return True
        # except(IllegalMoveError):
        #     return False
        # return False

    def passMove(self):
        """
        passing
        """
        self.nextMove(None, self.currentBoard, True)

    def playMove(self, x, y):
        """
        plays a move at (x, y)
        """
        #  create temp board
        tempBoard = deepcopy(self.currentBoard)
        kills = set()
        if not tempBoard.isEmpty(x, y):
            raise IllegalMoveError((x, y), "can only play on empty positions")
            return
        #  place stone on temp board
        tempBoard.setPosition(x, y, tempBoard.player)
        neighbours = tempBoard.getNeighbours(x, y)
        #  remove empty field form neighbours
        toRemove = set()
        for stone in neighbours:
            if tempBoard.isEmpty(*stone):
                toRemove.add(stone)
        neighbours -= toRemove
        #  remove friendly stones --> left with enemies
        toRemove = set()
        for stone in neighbours:
            if tempBoard.isFriend(x, y, *stone):
                    toRemove.add(stone)
        neighbours -= toRemove
        #  check and kill neighbouring enemy groups if neccacary
        checked = set()
        for stone in neighbours:
            if stone in checked:
                continue
            groupInfo = tempBoard.getGroupInfo(*stone)
            #  kill dead stones
            if not groupInfo["libs"]:
                for stone in groupInfo["group"]:
                    tempBoard.killStone(*stone)
                    kills.add(stone)
            checked.update(groupInfo["group"])
        #  check if played stone has liberties
        if not tempBoard.getGroupInfo(x, y)["libs"]:
            # tempBoard.setPosition(x, y, GoColor.empty)
            raise IllegalMoveError((x, y), "no liberties")
            return
        elif self.checkForKo(tempBoard):
            # tempBoard.setPosition(x, y, GoColor.empty)
            raise KoError((x, y), "Forbidden due to Ko rule")
            return
        else:
            # check for potential ko
            if len(kills) == 1:
                self.setKo = kills.pop()
            #  move gets played
            self.nextMove((x, y), tempBoard)

    def addMoveSgf(self, move):
        """adds move :: (int, int) to main variation of sgf"""
        # invert row coordinate to fit sgfmill format
        sgfMove = (self.currentBoard.size-1 - move[0], move[1])
        node = self.sgfHist.extend_main_sequence()
        if self.currentBoard.player == GoColor.black:
            node.set_move('b', sgfMove)
        else:
            node.set_move('w', sgfMove)

    def saveSgf(self, pathname):
        """ saves the sgf under pathname """
        with open(pathname, "wb") as f:
            f.write(self.sgfHist.serialise())


# Testing area
if __name__ == "__main__":
    player1 = Player.Player("Max Mustermann", "10k")
    player2 = Player.Player("Marta Musterfrau", "8k")
    testgame = Game(player1, player2)
    testgame.playMove(0, 1)
    testgame.playMove(0, 0)
    testgame.playMove(1, 0)
    testgame.playMove(2, 3)
    testgame.saveSgf("test.sgf")
