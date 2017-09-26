#! /usr/bin/env python3
import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication, QAction, qApp,
                             QWidget, QPushButton, QHBoxLayout, QVBoxLayout,
                             QLabel)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal
# from PyQt5 import Qt

from GoExceptions import IllegalMoveError
from Game import Game
from BoardGUI import BoardGUI


class MainWin(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # statusbar
        self.statusB = self.statusBar()
        self.statusB.showMessage('Ready')

        # setup window
        self.setGeometry(50, 50, 800, 600)
        self.setWindowTitle('GoGote')
        self.setWindowIcon(QIcon('png/icon.png'))

        # Initialize central Game Widget
        newGame = Game()
        gameW = GameWidget(self, newGame)
        self.setCentralWidget(gameW)
        # self.statusB.showMessage(self.statusText())

        # define Action to quit programm
        exitAct = QAction('&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit GoGote')
        exitAct.triggered.connect(qApp.quit)

        # define other Actions
        viewCoordsAct = QAction('View Coordinates', self, checkable=True)
        viewCoordsAct.setChecked(True)
        viewCoordsAct.triggered.connect(self.toggleCoords)

        # create a menubar
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAct)

        viewMenu = menubar.addMenu('&View')
        viewMenu.setStatusTip('Viewmenu')
        viewMenu.addAction(viewCoordsAct)

    def toggleCoords(self, state):
        """
        toogles showing coordinates
        """
        # TODO implement coordinates. atm shows/hides statusbar for testing
        if state:
            self.statusB.show()
        else:
            self.statusB.hide()

    def statusText(self):
        """ generates statusbar Text"""
        status = ""
        status += "Move: " + str(self.game.moveCounter) + ". "
        playerStr = ""
        if self.board.player == self.board.black:
            playerStr = "Black"
        elif self.board.player == self.board.white:
            playerStr = "White"
        status += playerStr + " to play."
        return status


class GameWidget(QWidget):
    """
    A Widget that contains everything for a game
    Game is supposed the be a child of a QMainWindow
    """

    # Signal send when a change to the Game has occured
    updateSignal = pyqtSignal()

    def __init__(self, parent, game):
        super().__init__()
        self.initGame(game)

    def initGame(self, game):
        self.game = game
        self.board = self.game.currentBoard

        # create child Widgets
        boardW = BoardGUI(self, self.board)
        controleW = ControleWidget(self, self.game)
        infoW = InfoWidget(self, self.game)

        # create Layout
        hbox = QHBoxLayout()
        hbox.addWidget(boardW, stretch=1)

        vbox = QVBoxLayout()
        vbox.addWidget(infoW)
        vbox.addWidget(controleW, stretch=1)
        hbox.addLayout(vbox)

        self.setLayout(hbox)

        # binding signals
        self.updateSignal.connect(boardW.updatePostion)
        boardW.stoneClicked.connect(self.playSlot)

    def playSlot(self, pos):
        """
        expects an pos :: (int, int)
        Slot that playes the move recived
        """
        try:
            self.game.playMove(*pos)
        except(IllegalMoveError):
            print("Illegal Move")
        self.updateSignal.emit()
        # DEBUG
        print(self.game.currentBoard)


class InfoWidget(QWidget):
    """ Widget desplays information on the game"""
    def __init__(self, parent, game):
        super().__init__()
        self.initUI(game)

    def initUI(self, game):
        testlabel = QLabel()
        testlabel.setText("Placeholder")

        # Layout
        hbox = QHBoxLayout()
        hbox.addWidget(testlabel)
        self.setLayout(hbox)


class ControleWidget(QWidget):
    """contains the controle elements for the game"""
    # msg2StatusB = pyqtSignal(str)
    def __init__(self, parent, game):
        super().__init__()
        self.initControle(game)

    def initControle(self, game):
        self.game = game

        passBtn = QPushButton('Pass')
        passBtn.clicked.connect(self.game.passMove)

        vbox = QVBoxLayout()
        vbox.addWidget(passBtn)

        self.setLayout(vbox)


# Testing area
if __name__ == "__main__":
    print(sys.version)

    app = QApplication(sys.argv)
    win = MainWin()
    win.show()

    sys.exit(app.exec_())
