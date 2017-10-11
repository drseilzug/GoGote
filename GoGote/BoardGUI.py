#! /usr/bin/env python3
import sys

from PyQt5.QtWidgets import (QGraphicsScene, QGraphicsObject, QGraphicsItemGroup,
                             QApplication, QWidget, QGraphicsView, QHBoxLayout,
                             QGraphicsSimpleTextItem)
from PyQt5.QtGui import QPen, QBrush, QColor  # ,QPainter
from PyQt5.QtCore import QRectF, Qt, pyqtSignal
from Game import Game
from GoColor import GoColor, GoMarks


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

        self.showCoords = True
        self.scene = QGraphicsScene()

        # grid containing coordinates for the scene
        self.grid = []
        self.drawGrid()

        # initialize and set layout + view
        self.view = QGraphicsView(self.scene)
        self.view.setMouseTracking(True)
        self.view.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setMouseTracking(True)
        box = QHBoxLayout()
        box.addWidget(self.view)
        self.setLayout(box)

        # stones for all positions are created and listed in self.pos dict
        self.createPosition()
        self.makeCoords()  # has to be called after drawGrid!

    def resizeEvent(self, e):
        self.view.fitInView(self.view.scene().sceneRect(), Qt.KeepAspectRatio)

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

        leftOffset = 0.5*baseWidth  # (self.contentsRect().width()-self.boardWidth())/2
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

    def makeCoords(self):
        """ draws Coordinates """
        xLabels = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        yLabels = list(range(1, 26))
        botGrid = []
        leftGrid = []
        # generate pixel coordinates grids
        for n in range(self.board.size):
            (xBot, yBot) = self.grid[self.board.size-1][n]
            yBot += self.baseWidth*0.4/self.baseRectRatio
            xBot -= self.baseWidth*0.1
            botGrid.append((xBot, yBot))
            (xLeft, yLeft) = self.grid[n][0]
            xLeft -= self.baseWidth*1.2
            yLeft -= self.baseWidth*0.3/self.baseRectRatio
            leftGrid.append((xLeft, yLeft))
        # generate Text items and add them to group
        self.coordGroup = QGraphicsItemGroup()
        for n in range(self.board.size):
            leftText = QGraphicsSimpleTextItem(str(yLabels[n]))
            leftText.setPos(*leftGrid[n])
            self.coordGroup.addToGroup(leftText)
            bottomText = QGraphicsSimpleTextItem(xLabels[n])
            bottomText.setPos(*botGrid[n])
            self.coordGroup.addToGroup(bottomText)
        # draw coordinates and update visibility according to self.showCoords
        self.scene.addItem(self.coordGroup)
        self.updateCoords()

    def updateCoords(self):
        """ slot that updates the visibility os the coordiantes. """
        self.coordGroup.setVisible(self.showCoords)

    def setCoordVis(self, visibility):
        """ set the self.showCoords boolean """
        self.showCoords = visibility
        self.updateCoords()

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
            self.pos[(x, y)].setMark(None)
            self.pos[(x, y)].setColor(color)
        lastMove = self.game.currentBoard.lastMove
        if lastMove:
            self.pos[lastMove].setMark(GoMarks.circel)
        ko = self.game.currentBoard.ko
        if ko:
            self.pos[ko].setMark(GoMarks.square)

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
    """

    # signal
    clicked = pyqtSignal()

    def __init__(self, x, y, rad, color=GoColor.empty):
        super().__init__()

        self.rad = rad
        self.color = color
        self.setPos(x, y)
        self.hover = False
        self.mark = None

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
        elif self.color == GoColor.empty or self.color == GoColor.ko:
            if self.hover:
                painter.setBrush(QColor(150, 150, 150))
                self.setOpacity(0.4)
            else:
                self.setOpacity(0.001)
        else:
            return
        if self.mark != GoMarks.square:
            painter.drawEllipse(self.boundingRect())

        # draw Marker
        if self.color == GoColor.black:
            painter.setPen(QColor(200, 200, 200))
        elif self.color == GoColor.white:
            painter.setPen(QColor(0, 0, 0))
        painter.setBrush(Qt.NoBrush)
        if self.mark == GoMarks.circel:
            painter.drawEllipse(-self.rad*0.65, -self.rad*0.65,
                                1.3*self.rad, 1.3*self.rad)
        if self.mark == GoMarks.square:
            self.setOpacity(1)
            painter.drawRect(-self.rad*0.6, -self.rad*0.6,
                             self.rad*1.2, self.rad*1.2)
        else:
            return

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

    def setMark(self, mark=None):
        """ sets a stone marked flag """
        self.mark = mark


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
    board.setCoordVis(True)

    win.show()
    sys.exit(app.exec_())
