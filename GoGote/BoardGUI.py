#! /usr/bin/env python3
import sys
from PyQt5.QtWidgets import (QGraphicsScene, QGraphicsItem,
                             QApplication, QWidget, QGraphicsView, QHBoxLayout)
from PyQt5.QtGui import QPen, QBrush, QColor  # ,QPainter
from PyQt5.QtCore import QRectF, Qt
from Game import Game


class BoardGUIx(QWidget):
    """cointain the grafical representation of the Board"""

    # ratio of boardersize compared to the size of one base square
    borderRatio = 0.8
    baseRectRatio = 14/15  # 12/13 for normal ratio but looks weird
    stoneScale = 0.46

    def __init__(self, parent, board):
        super().__init__()

        self.initUI(board)

    def initUI(self, board):
        self.board = board

        self.showCoords = False  # TODO
        self.scene = QGraphicsScene()

        # grid containing coordinates for the scene
        self.grid = []
        self.drawGrid()

        # stones for all positions are created and listed in self.pos dict
        self.createPosition()

        # initialize and set layout + view
        self.view = QGraphicsView(self.scene)
        self.view.setMouseTracking(True)
        self.setMouseTracking(True)
        box = QHBoxLayout()
        box.addWidget(self.view)
        self.setLayout(box)

    def resizeEvent(self, e):
        self.view.fitInView(self.view.scene().sceneRect(), Qt.KeepAspectRatio)
        # TODO: self.drawGrid()

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

    def updatePostion(self):
        """
        sets the colors for all stones in self.pos according
        to the status in self.board
        """
        for (x, y) in self.pos:
            color = self.board.getPosition(x, y)
            self.pos[(x, y)].setColor(color)

    def createPosition(self):
        """
        Creates the self.pos dictionary containing all possible stones on the
        board initialized as empty stones
        """
        self.pos = {}
        radius = self.stoneScale*self.baseWidth
        for row in range(self.board.size):
            for col in range(self.board.size):
                (x, y) = self.grid[row][col]
                newStone = Stone(x, y, radius)
                self.pos[(row, col)] = newStone
                self.scene.addItem(newStone)
        self.updatePostion()


class Stone(QGraphicsItem):
    """
    A Go stone QGraphicsItem
    x, y :: center Coords of Stone
    rad :: radius
    color:: the stone type
        0, self.empty :: empty *default
        1, self.black :: black
        2, self.white :: white

    Draws an invisible stone if empty
    TODO:
        lastMove Property --> bool
        setLastmove()
        add lastmoveMarker to drawing
    """
    empty = 0
    black = 1
    white = 2

    def __init__(self, x, y, rad, color=0):
        super().__init__()

        self.rad = rad
        self.color = color
        self.setPos(x, y)
        self.hover = False

        self.setAcceptHoverEvents(True)

    def boundingRect(self):
        """ sets the outer rectangle for the QGrpahicsItem"""
        rect = QRectF(-self.rad, -self.rad,
                      2*self.rad, 2*self.rad)
        return rect

    def paint(self, painter, *args, **kwargs):
        """ draws the actual Stone"""
        painter.setBrush(Qt.SolidPattern)
        if self.color == self.black:
            painter.setBrush(QColor(5, 5, 5))
        elif self.color == self.white:
            painter.setBrush(QColor(255, 255, 255))
        elif self.color == self.empty:
            if self.hover:
                painter.setBrush(QColor(150, 150, 150))
                self.setOpacity(0.5)
            else:
                self.setOpacity(0.001)
        else:
            return

        painter.drawEllipse(self.boundingRect())

    def setColor(self, color):
        """Method that sets the stone to color"""
        self.color = color

    def hoverEnterEvent(self, e):
        self.hover = True
        self.update()

    def hoverLeaveEvent(self, e):
        self.hover = False
        self.update()


# Testing area
if __name__ == "__main__":
    print(sys.version)

    from PyQt5.QtWidgets import QMainWindow
    app = QApplication(sys.argv)

    game = Game()
    game.playMove(4, 4)
    game.playMove(2, 2)

    win = QMainWindow()
    win.setGeometry(100, 100, 800, 800)
    board = BoardGUIx(win, game.currentBoard)
    win.setCentralWidget(board)

    win.show()
    sys.exit(app.exec_())
