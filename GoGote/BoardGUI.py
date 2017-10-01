#! /usr/bin/env python3
import sys

from PyQt5.QtWidgets import (QGraphicsScene, QGraphicsObject,
                             QApplication, QWidget, QGraphicsView, QHBoxLayout)
from PyQt5.QtGui import QPen, QBrush, QColor  # ,QPainter
from PyQt5.QtCore import QRectF, Qt, pyqtSignal
from Game import Game
from GoColor import GoColor


class BoardGUI(QWidget):
    """cointain the graphical representation of the Board"""

    # ratio of bordersize compared to the size of one base square
    borderRatio = 0.8
    baseRectRatio = 14/15  # 12/13 for normal ratio but looks weird
    stoneScale = 0.46

    # siganl
    stoneClicked = pyqtSignal(tuple)

    def __init__(self, parent, game):
        super().__init__()

        self.initUI(game)

    def initUI(self, game):
        self.board = game.currentBoard
        self.game = game

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

    def updatePosition(self):
        """
        sets the colors for all stones in self.pos according
        to the status in self.board
        """
        for (x, y) in self.pos:
            color = self.game.currentBoard.getPosition(x, y)
            self.pos[(x, y)].setColor(color)

    def createPosition(self):
        """
        Creates the self.pos dictionary containing all possible stones on the
        board initialized as empty stones

        also connects a signal form each stone to ???
        """
        self.pos = {}
        radius = self.stoneScale*self.baseWidth
        for row in range(self.board.size):
            for col in range(self.board.size):
                (x, y) = self.grid[row][col]
                newStone = Stone(x, y, radius)
                self.pos[(row, col)] = newStone
                self.scene.addItem(newStone)
        self.updatePosition()
        self.connecting()

    def connecting(self):
        for key in self.pos:
            self.pos[key].clicked.connect(lambda key=key: self.resend(key))

    def resend(self, pos):
        """
        emits the captured signal again,
        with (int, in) parameter for stone clicked
        """
        self.stoneClicked.emit(pos)


class Stone(QGraphicsObject):
    """
    A Go stone QGraphicsItem
    x, y :: center Coords of Stone
    rad :: radius
    color:: the stone type
        0, GoColor.empty :: empty *default
        1, CoColor.black :: black
        2, GoColor.white :: white

    Draws an invisible stone if empty
    TODO:
        lastMove Property --> bool
        setLastmove()
        add lastmoveMarker to drawing
    """

    # signal
    clicked = pyqtSignal()

    def __init__(self, x, y, rad, color=GoColor.empty):
        super().__init__()

        self.rad = rad
        self.color = color
        self.setPos(x, y)
        self.hover = False

        self.setAcceptHoverEvents(True)
        self.setAcceptedMouseButtons(Qt.LeftButton)

    def boundingRect(self):
        """ sets the outer rectangle for the QGrpahicsItem"""
        rect = QRectF(-self.rad, -self.rad,
                      2*self.rad, 2*self.rad)
        return rect

    def paint(self, painter, *args, **kwargs):
        """ draws the actual Stone"""
        painter.setBrush(Qt.SolidPattern)
        if self.color == GoColor.black:
            self.setOpacity(1)
            painter.setBrush(QColor(5, 5, 5))
        elif self.color == GoColor.white:
            self.setOpacity(1)
            painter.setBrush(QColor(255, 255, 255))
        elif self.color == GoColor.empty:
            if self.hover:
                painter.setBrush(QColor(150, 150, 150))
                self.setOpacity(0.4)
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

    def mousePressEvent(self, e):
        self.clicked.emit()


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
    board = BoardGUI(win, game)
    win.setCentralWidget(board)

    win.show()
    sys.exit(app.exec_())
