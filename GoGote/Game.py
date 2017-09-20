#! /usr/bin/env python3
import Board
import Player
from copy import copy


class Game:
    """
    Fields:
        playerBlack:: a Player object containing Data on the black player
        playerWhite:: a Player object containing Data on the white player
        currentBoard:: a Board object containing the current board statuses
        moveCounter:: an integer for the move count
        gameHistory:: a dict containing the moves keyed by the moveCounter
        koHashTable:: a dict with lists of boards that have occured
                        keyed by the board hashes
        consecutivePasses:: counts the number of consecutive passes
    """

    def __init__(self, playerBlack=Player.Player(),
                 playerWhite=Player.Player(), currentBoard=Board.Board(),
                 moveCounter=0,
                 gameHistory={}, koHashTable={}):
        self.playerBlack = playerBlack
        self.playerWhite = playerWhite
        self.currentBoard = currentBoard
        self.moveCounter = moveCounter
        self.gameHistory = gameHistory
        #  Initialize hash table and add starting position
        self.koHashTable = koHashTable
        self.koHashTable[self.currentBoard.boardHash()] = [self.currentBoard]
        #  consecutivePasses always 0 for new board
        self.consecutivePasses = 0

    def nextMo(self, move, newBoard, passed=False):
        """
        increments the move
        adds move to gameHistory
        adds hash to koHashTable
        changes current Player
        updated the currentBoard
        updates consecutivePasses counter
        """
        #  update game and hash table
        self.gameHistory[self.moveCounter] = move
        #  update board position and moveCounter
        self.currentBoard = newBoard
        self.moveCounter += 1
        #  change player
        if self.currentBoard.player == self.currentBoard.black:
            self.currentBoard.player = self.currentBoard.white
        elif self.currentBoard.player == self.currentBoard.white:
            self.currentBoard.player = self.currentBoard.black
        #  add new position to koHashTable
        # TODO
        #  TODO: here check for ko and update accordingly
        #  update/reset passing counter
        if passed:
            self.consecutivePasses += 1
        else:
            self.consecutivePasses = 0

    def addBoardToHash(self):
        """
        Adds self.currentBoard to self.koHashTable
        """
        self.koHashTable[self.currentBoard.boardHash()].add(self.currentBoard)

    def checkForKo(self, board):
        """
        checks if board is found in koHashTable
        TODO: default value for board is self.currentBoard
        returns True if found; False otherwise
        """
        for koBoard in self.koHashTable[self.boardHash()]:
            if koBoard.position == board.position \
                    and koBoard.player == board.player:
                return True
            else:
                return False

    def passMove(self):
        """
        passing
        """
        self.nextMov(None, self.currentBoard, True)
        #  TODO: remove Ko block maybe? (prob not)

    def playMove(self, x, y):
        """
        plays a move at (x, y)
        """
        #  create temp board
        tempBoard = copy(self.currentBoard)
        if not tempBoard.isEmpty(x, y):
            #  TODO define IllegalMoveError
            raise ValueError("can only play on empty positions")
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
            print("STONE:", stone, "checked:", checked)
            if stone in checked:
                continue
            groupInfo = tempBoard.getGroupInfo(*stone)
            #  kill dead stones
            if not groupInfo["libs"]:
                for stone in groupInfo["group"]:
                    tempBoard.killStone(*stone)
            checked.union(groupInfo["group"])
        #  check if played stone has liberties
        if not tempBoard.getGroupInfo(x, y)["libs"]:
            raise ValueError("IllegalMoveError: no liberties")
        else:
            #  move gets played
            self.nextMove((x, y), tempBoard)

    # Methods to implement
        # def makeMove(self, x, y):


# Testing area
if __name__ == "__main__":
    player1 = Player.Player("Max Mustermann", "10k")
    player2 = Player.Player("Marta Musterfrau", "8k")
    testgame = Game(player1, player2)
    testgame.playMove(0, 1)
    print("--")
    testgame.playMove(0, 0)
    print("------------------------------------")
    testgame.playMove(1, 0)
    testgame.playMove(0, 5)
    print(testgame.currentBoard)
