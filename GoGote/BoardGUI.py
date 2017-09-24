#! /usr/bin/env python3
import sys
from PyQt5.QtWidgets import (QGraphicsScene, QGraphicsItem,
                             QApplication, QWidget, QGraphicsView, QHBoxLayout)
from PyQt5.QtGui import QPen, QBrush  # ,QPainter
from PyQt5.QtCore import QRectF, Qt
from Game import Game


class BoardGUIx(QWidget):
    """cointain the grafical representation of the Board"""

    # ratio of boardersize compared to the size of one base square
    borderRatio = 0.8
    baseRectRatio = 14/15  # 12/13 for normal ratio but looks weird
    stoneScale = 0.95

    def __init__(self, parent, board):
        super().__init__()

        self.initUI(board)

    def initUI(self, board):
        self.board = board

        self.showCoords = False  # TODO
        self.scene = QGraphicsScene()

        self.grid = []
        # Grid is drawn whenever resizeEvent is called, including on init

        self.view = QGraphicsView(self.scene)
        box = QHBoxLayout()
        box.addWidget(self.view)
        self.setLayout(box)

    def resizeEvent(self, e):
        self.scene.clear()
        self.drawGrid()

        stoneRad = self.baseWidth*self.stoneScale
        teststone = Stone(*self.grid[3][3], stoneRad, 1)
        self.scene.addItem(teststone)
        # teststone.setPos(*self.grid[3][3])
        self.scene.addLine(*self.grid[3][3], *self.grid[4][4])

    def boardWidth(self):
        """returns the max width fitting into widget"""
        width = self.contentsRect().width()*0.95
        height = self.contentsRect().height()*0.95

        return min(width, height*self.baseRectRatio)

    def boardHeight(self):
        """returns the max width fitting into widget """
        return self.boardWidth()*(1/self.baseRectRatio)

    def makeGrid(self):
        """
        returns coords [[(x, y)]] for the Grid according
         to current window mesures
        """
        # set scenesize to window size
        self.scene.setSceneRect(0, 0, self.boardWidth(), self.boardHeight())
        # 0.8*baserectangle size for each border
        denom = self.board.size + 2*self.borderRatio
        baseWidth = self.boardWidth() / denom
        baseHeight = self.boardHeight() / denom

        leftOffset = 0  # (self.contentsRect().width()-self.boardWidth())/2
        topOffset = 0  # (self.contentsRect().height()-self.boardHeight())/2

        partionWidth = [leftOffset+(self.borderRatio+x)*baseWidth
                        for x in range(self.board.size)]
        partionHeight = [topOffset+(self.borderRatio+x)*baseHeight
                         for x in range(self.board.size)]

        grid = [[(x, y) for x in partionWidth] for y in partionHeight]
        self.grid = grid
        self.baseWidth = baseWidth

    def drawGrid(self):
        """draws the background grid"""
        self.makeGrid()
        print("entered draw grid")
        for line in self.grid:
            self.scene.addLine(*line[0], *line[-1])
        for (pointT, pointB) in zip(self.grid[0], self.grid[-1]):
            self.scene.addLine(*pointT, *pointB)
        self.drawHoshis()

    def drawHoshis(self):
        """ Draws Hoshi dots"""
        hoshis = []
        rad = self.baseWidth*0.15
        for (x, y) in self.board.getHoshis():
            hoshis.append(self.grid[x][y])
        for point in hoshis:
            (x, y) = point
            self.scene.addEllipse(x-rad, y-rad, rad*2.0, rad*2.0,
                                  QPen(), QBrush(Qt.SolidPattern))


class Stone(QGraphicsItem):
    """
    A Go stone QGraphicsItem
    x, y :: center Coords of Stone
    rad :: radius
    color:: the stone type
        0, self.empty :: empty
        1, self.black :: black
        2, self.white :: white
    """
    empty = 0
    black = 1
    white = 2

    def __init__(self, x, y, rad, color):
        super().__init__()

        self.x = x
        self.y = y
        self.rad = rad
        self.color = color
        self.setPos(x, y)

    def boundingRect(self):
        rect = QRectF(-self.rad, -self.rad,
                      -self.rad, self.rad)
        return rect

    def paint(self, painter, *args, **kwargs):
        painter.drawEllipse(self.boundingRect())


# Testing area
if __name__ == "__main__":
    print(sys.version)

    from PyQt5.QtWidgets import QMainWindow
    app = QApplication(sys.argv)

    game = Game()
    win = QMainWindow()
    win.setGeometry(100, 100, 600, 800)
    board = BoardGUIx(win, game.currentBoard)
    win.setCentralWidget(board)

    win.show()
    sys.exit(app.exec_())
