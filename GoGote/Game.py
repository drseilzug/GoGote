#! /usr/bin/env python3
import Board
# from GoColor import GoColor
import Player
from copy import deepcopy
from GoExceptions import IllegalMoveError


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

    def nextMove(self, move, newBoard, passed=False):
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
        self.currentBoard.tooglePlayer()
        #  add new position to koHashTable
        self.addBoardToHash()
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
        newHash = self.currentBoard.boardHash()
        boardCopy = deepcopy(self.currentBoard)
        if newHash in self.koHashTable:
            self.koHashTable[newHash].append(boardCopy)
        else:
            self.koHashTable[newHash] = [boardCopy]

    def checkForKo(self, board, otherPlayer=True):
        """
        checks if board is found in koHashTable
        when otherPlayer == True it checks if the board is in the table for
        the Player whos move it is not in board
        TODO: default value for board is self.currentBoard
        returns True if found; False otherwise

        TODO: implement toogle for KO/SUPERKO/no KO
        """
        koStatus = False
        if otherPlayer:
            board.tooglePlayer()
        newHash = board.boardHash()
        if newHash in self.koHashTable:
            for koBoard in self.koHashTable[newHash]:
                if koBoard.position == board.position \
                        and koBoard.player == board.player:
                    koStatus = True
        # toogle back player to set board back to initial state
        if otherPlayer:
            board.tooglePlayer()
        return koStatus

    def passMove(self):
        """
        passing
        """
        self.nextMove(None, self.currentBoard, True)
        #  TODO: remove Ko block maybe? (prob not)

    def playMove(self, x, y):
        """
        plays a move at (x, y)
        """
        #  create temp board
        tempBoard = deepcopy(self.currentBoard)
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
            checked.update(groupInfo["group"])
        #  check if played stone has liberties
        if not tempBoard.getGroupInfo(x, y)["libs"]:
            # tempBoard.setPosition(x, y, GoColor.empty)
            raise IllegalMoveError((x, y), "no liberties")
            return
        elif self.checkForKo(tempBoard):
            # tempBoard.setPosition(x, y, GoColor.empty)
            raise IllegalMoveError((x, y), "Forbidden due to Ko rule")
            return
        else:
            #  move gets played
            self.nextMove((x, y), tempBoard)


# Testing area
if __name__ == "__main__":
    player1 = Player.Player("Max Mustermann", "10k")
    player2 = Player.Player("Marta Musterfrau", "8k")
    testgame = Game(player1, player2)
    testgame.playMove(0, 1)
    testgame.playMove(0, 0)
    testgame.playMove(1, 0)
    testgame.playMove(2, 3)
    print(testgame.currentBoard.capsBlack)
