#! /usr/bin/env python3
import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication, QAction, qApp,
                             QWidget, QPushButton, QHBoxLayout, QVBoxLayout,
                             QLabel)
from PyQt5.QtGui import QIcon, QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QPointF  # , pyqtSignal
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
        self.game.playMove(1, 0)
        self.game.playMove(0, 0)
        self.game.playMove(0, 1)
        self.game.playMove(1, 1)
        # self.update()
        print("test")


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


class Board_GUI(QWidget):
    """cointain the grafical representation of the Board"""

    # ratio of boardersize compared to the size of one base square
    borderRatio = 0.8
    baseRectRatio = 14/15  # 12/13 for normal ratio but looks weird
    stoneScale = 0.467

    def __init__(self, parent, board):
        super().__init__()

        self.initUI(board)

    def initUI(self, board):
        self.board = board
        self.grid = []
        # moustracking to highlight position
        self.setMouseTracking(True)
        self.showCoords = False  # TODO

    def boardWidth(self):
        """returns the max width fitting into widget"""
        width = self.contentsRect().width()
        height = self.contentsRect().height()

        return min(width, height*self.baseRectRatio)

    def boardHeight(self):
        """returns the max width fitting into widget """
        return self.boardWidth()*(1/self.baseRectRatio)

    def makeGrid(self):
        """returns coords for the Grid according to current window mesures"""
        # 0.8*baserectangle size for each border
        denom = self.board.size + 2*self.borderRatio
        baseWidth = self.boardWidth() / denom
        baseHeight = self.boardHeight() / denom

        leftOffset = (self.contentsRect().width()-self.boardWidth())/2
        topOffset = (self.contentsRect().height()-self.boardHeight())/2

        partionWidth = [leftOffset+(self.borderRatio+x)*baseWidth
                        for x in range(self.board.size)]
        partionHeight = [topOffset+(self.borderRatio+x)*baseHeight
                         for x in range(self.board.size)]

        grid = [[QPointF(x, y) for x in partionWidth] for y in partionHeight]
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
        self.drawPosition(painter)

    def drawHoshis(self, painter):
        """ Draws Hoshi dots"""
        hoshis = []
        pen = QPen()
        pen.setWidth(8)
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)

        for (x, y) in self.board.getHoshis():
            hoshis.append(self.grid[x][y])
        for point in hoshis:
            painter.drawPoint(point)
        painter.setPen(QPen())

    def drawPosition(self, painter):
        """draws the positionon onto the Grid"""
        for x in range(self.board.size):
            for y in range(self.board.size):
                self.drawStone(painter, self.grid[x][y],
                               self.board.postion[x][y])

    def drawStone(self, painter, targetPoint, color):
        """draws a Stone of color at position"""
        unit = (self.grid[0][0]-self.grid[0][1]).manhattanLength()
        radius = unit * self.stoneScale
        if color == self.board.black:
            stoneColor = QColor(255, 255, 255)
        elif color == self.board.white:
            stoneColor = QColor(0, 0, 0)
        else:
            return
        painter.setBrush(stoneColor)
        painter.drawEllipse(targetPoint, radius, radius)

    def drawLastMove(self, painter):
        """draws a square on the last placed stone"""
        pass  # TODO


# Testing area
if __name__ == "__main__":
    print(sys.version)

    app = QApplication(sys.argv)
    win = MainWin()
    win.show()

    sys.exit(app.exec_())
