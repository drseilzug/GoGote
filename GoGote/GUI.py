#! /usr/bin/env python3
import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication, QAction, qApp,
                             QWidget, QPushButton, QHBoxLayout, QVBoxLayout,
                             QLabel, QFileDialog)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal
# from PyQt5 import Qt

from GoExceptions import IllegalMoveError, KoError
from Game import Game
from Board import Board
from Player import Player
from GoColor import GoColor
from BoardGUI import BoardGUI
from GUIDialogs import NewGameDialog


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

        # Initialize central Game Widget and make a new Game
        initialGame = Game()
        self.gameW = GameWidget(self, initialGame)
        self.setCentralWidget(self.gameW)
        # self.statusB.showMessage(self.statusText())

        # define Actions
        exitAct = QAction('&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit GoGote')
        exitAct.triggered.connect(qApp.quit)

        newGameAct = QAction('&New Game', self)
        newGameAct.setShortcut('Ctrl+N')
        newGameAct.setStatusTip('Start a new Game')
        newGameAct.triggered.connect(self.newGameD)

        closeGameAct = QAction('&Close Game', self)
        closeGameAct.setShortcut('Ctrl+C')
        closeGameAct.setStatusTip('Close current Game')
        closeGameAct.triggered.connect(self.closeGame)

        saveSgfAct = QAction('&Save Game SGF', self)
        saveSgfAct.setShortcut('Ctrl+S')
        saveSgfAct.setStatusTip('Save current game as SGF.')
        saveSgfAct.triggered.connect(self.saveFileDialog)

        viewCoordsAct = QAction('View Coordinates', self, checkable=True)
        viewCoordsAct.setChecked(True)
        viewCoordsAct.triggered.connect(self.gameW.toggleCoords)

        # create a menubar
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(newGameAct)
        fileMenu.addAction(closeGameAct)
        fileMenu.addSeparator()
        fileMenu.addAction(saveSgfAct)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAct)

        viewMenu = menubar.addMenu('&View')
        viewMenu.setStatusTip('Viewmenu')
        viewMenu.addAction(viewCoordsAct)

    def closeGame(self):
        """closes the current Game"""
        self.gameW.close()

    def saveFileDialog(self):
        saveDialog = QFileDialog()
        saveDialog.setAcceptMode(QFileDialog.AcceptSave)
        saveDialog.setFileMode(QFileDialog.AnyFile)
        saveDialog.setDefaultSuffix('sgf')  # TODO this does not work
        fileName, _ = saveDialog.getSaveFileName(
                self, "Save Game SGF",
                "", "Smart Game Files (*.sgf)",)
        if fileName:
            self.gameW.save(fileName)

    def makeNewGame(self, size=19, playerB=Player(), playerW=Player(), hc=0):
        """Starts a new Game"""
        newGame = Game(playerB, playerW, Board(size))
        newGame.currentBoard.setHC(hc)
        self.closeGame()
        self.gameW = GameWidget(self, newGame)
        self.setCentralWidget(self.gameW)

    def newGameD(self):
        """ opens a NewGameDialog """
        newGame = NewGameDialog()
        newGame.createGame.connect(self.makeNewGame)
        newGame.exec_()


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
        # self.board = self.game.currentBoard

        # create child Widgets
        self.boardW = BoardGUI(self, self.game)
        controleW = ControleWidget(self, self.game)
        infoW = InfoWidget(self, self.game)

        # create Layout
        hbox = QHBoxLayout()
        hbox.addWidget(self.boardW, stretch=1)

        vbox = QVBoxLayout()
        vbox.addWidget(infoW)
        vbox.addWidget(controleW, stretch=1)
        hbox.addLayout(vbox)

        self.setLayout(hbox)

        # binding signals
        self.updateSignal.connect(self.boardW.updatePosition)
        self.boardW.stoneClicked.connect(self.playSlot)

    def playSlot(self, pos):
        """
        expects an pos :: (int, int)
        Slot that playes the move recived
        """
        try:
            self.game.playMove(*pos)
        except(IllegalMoveError):
            print("Illegal Move")
        except(KoError):
            print('Ko!')
        self.updateSignal.emit()
        # DEBUG
        # print(self.game.currentBoard)

    def statusText(self):
        """ generates statusbar Text"""
        # TODO: implement this
        status = ""
        status += "Move: " + str(self.game.moveCounter) + ". "
        playerStr = ""
        if self.board.player == GoColor.black:
            playerStr = "Black"
        elif self.board.player == GoColor.white:
            playerStr = "White"
        status += playerStr + " to play."
        return status

    def toggleCoords(self, state):
        """
        toogles showing coordinates
        """
        self.boardW.setCoordVis(state)

    def save(self, pathname):
        """ saves the current game as an sgf """
        self.game.saveSgf(pathname)


class InfoWidget(QWidget):
    """ Widget desplays information on the game"""
    def __init__(self, parent, game):
        super().__init__()
        self.initUI(parent, game)

    def initUI(self, parent, game):
        self.game = game
        # Layout

        # table Head
        hboxHead = QHBoxLayout()
        self.blackHeadL = QLabel("Black")
        hboxHead.addWidget(self.blackHeadL)
        hboxHead.addSpacing(10)
        self.whiteHeadL = QLabel("White")
        hboxHead.addWidget(self.whiteHeadL)

        # Player names and rank row
        hboxPlayers = QHBoxLayout()
        blackLabel = QLabel()
        blackLabel.setText(game.playerBlack.name +
                           " (" + game.playerBlack.rank + ")")
        hboxPlayers.addWidget(blackLabel)
        hboxPlayers.addSpacing(10)
        whiteLabel = QLabel()
        whiteLabel.setText(game.playerWhite.name +
                           " (" + game.playerWhite.rank + ")")
        hboxPlayers.addWidget(whiteLabel)

        # Captures row
        hboxCaps = QHBoxLayout()
        self.blackCapsL = QLabel("Caps: "
                                 + str(self.game.currentBoard.capsBlack))
        self.whiteCapsL = QLabel("Caps: "
                                 + str(self.game.currentBoard.capsWhite))
        hboxCaps.addWidget(self.blackCapsL)
        hboxCaps.addWidget(self.whiteCapsL)

        vbox = QVBoxLayout()  # Main Vertical Box Layout
        vbox.addLayout(hboxHead)
        vbox.addLayout(hboxPlayers)
        vbox.addLayout(hboxCaps)

        self.setLayout(vbox)

        # initial update
        self.updateSlot()

        # signals
        parent.updateSignal.connect(self.updateSlot)

    def updateSlot(self):
        """ slot that gets called to induce an update of the relevant data"""
        # Capures update
        self.blackCapsL.setText("Caps: "+str(self.game.currentBoard.capsBlack))
        self.whiteCapsL.setText("Caps: "+str(self.game.currentBoard.capsWhite))
        # player indication
        if self.game.currentBoard.player == GoColor.black:
            self.blackHeadL.setText("<b>Black</b>")
            self.whiteHeadL.setText("White")
        else:
            self.blackHeadL.setText("Black")
            self.whiteHeadL.setText("<b>White</b>")


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
