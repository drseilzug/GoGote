#! /usr/bin/env python3
import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication, QAction, qApp,
                             QWidget, QPushButton, QHBoxLayout, QVBoxLayout,
                             QLabel)
from PyQt5.QtGui import QIcon, QPainter, QPen
from PyQt5.QtCore import QPoint  # , pyqtSignal
# from PyQt5 import Qt

from Game import Game


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
    def __init__(self, parent, game):
        super().__init__()
        self.initGame(game)

    def initGame(self, game):
        self.game = game
        self.board = self.game.currentBoard

        # create child Widgets
        boardW = Board_GUI(self, self.board)
        controleW = Controle_GUI(self, self.game)
        infoW = InfoWidget(self, self.game)

        # create Layout
        hbox = QHBoxLayout()
        hbox.addWidget(boardW, stretch=1)

        vbox = QVBoxLayout()
        vbox.addWidget(infoW)
        vbox.addWidget(controleW, stretch=1)
        hbox.addLayout(vbox)

        self.setLayout(hbox)


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


class Controle_GUI(QWidget):
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


class Board_GUI(QWidget):
    """cointain the grafical representation of the Board"""
    def __init__(self, parent, board):
        super().__init__()

        self.initBoard(board)

    def initBoard(self, board):
        self.board = board
        self.grid = []
        # moustracking to highlight position
        self.setMouseTracking(True)
        self.showCoords = False  # TODO
        self.update()
        self.update()
        # TESTING TESTING TESTING:

    def boardWidth(self):
        """returns the max width fitting into widget"""
        width = self.contentsRect().width()
        height = self.contentsRect().height()

        return min(width, height*12/13)

    def boardHeight(self):
        """returns the max width fitting into widget """
        return self.boardWidth()*(13/12)

    def makeGrid(self):
        """returns coords for the Grid according to current window mesures"""
        # 0.8*baserectangle size for each border
        denom = self.board.size + 1.6
        baseWidth = self.boardWidth() / denom
        baseHeight = self.boardHeight() / denom

        partionWidth = [(0.8+x)*baseWidth for x in range(self.board.size)]
        partionHeight = [(0.8+x)*baseHeight for x in range(self.board.size)]

        grid = [[QPoint(x, y) for x in partionWidth] for y in partionHeight]
        self.grid = grid

    def paintEvent(self, event):
        """draws the whole board using the other draw methods"""
        painter = QPainter(self)
        self.makeGrid()
        self.drawGrid(painter)

    def drawGrid(self, painter):
        """draws the background grid"""
        for line in self.grid:
            painter.drawLine(line[0], line[-1])
        for (pointT, pointB) in zip(self.grid[0], self.grid[-1]):
            painter.drawLine(pointT, pointB)
        self.drawHoshis(painter)
        # Test TODO
        self.drawStone(painter, (6, 6), self.board.black)

    def drawHoshis(self, painter):
        """ Draws Hoshi dots"""
        hoshis = []
        pen = QPen()
        pen.setWidth(8)
        pen.setCapStyle(0x20)
        painter.setPen(pen)

        for (x, y) in self.board.getHoshis():
            hoshis.append(self.grid[x][y])
        for point in hoshis:
            painter.drawPoint(point)

    def drawPosition(self, painter):
        """draws the positionon onto the Grid"""
        pass  # TODO

    def drawStone(self, painter, positionon, color):
        """draws a Stone of color at position"""
        pass  # TODO


# Testing area
if __name__ == "__main__":
    print(sys.version)

    app = QApplication(sys.argv)
    win = MainWin()
    win.show()

    sys.exit(app.exec_())
