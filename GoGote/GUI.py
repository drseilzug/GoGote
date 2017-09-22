#! /usr/bin/env python3
import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication, QAction, qApp,
                             QWidget)
from PyQt5.QtGui import QIcon, QPainter, QPen
from PyQt5.QtCore import QPoint
from PyQt5 import Qt

from Game import Game


class MainWin(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # statusbar
        self.statusbar = self.statusBar()
        self.statusbar.showMessage('Ready')

        # setup window
        self.setGeometry(50, 50, 800, 600)
        self.setWindowTitle('GoGote')
        self.setWindowIcon(QIcon('png/icon.png'))

        # Initialize a Game and Board_GUI
        game = Game()
        theBoard = Board_GUI(self, game.currentBoard)
        self.setCentralWidget(theBoard)

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
            self.statusbar.show()
            self.statusbar.showMessage('Ready')
        else:
            self.statusbar.hide()


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

    def drawHoshis(self, painter):
        """ Draws Hoshi dots"""
        hoshis = []
        pen = QPen()
        pen.setWidth(8)
        painter.setPen(pen)

        for (x, y) in self.board.getHoshis():
            hoshis.append(self.grid[x][y])
        for point in hoshis:
            painter.drawPoint(point)

    def drawPosition(self, painter):
        """draws the positionon the Grid"""
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
