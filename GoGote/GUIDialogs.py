#! /usr/bin/env python3
from PyQt5.QtWidgets import (QDialog, QPushButton, QLineEdit, QHBoxLayout,
                             QVBoxLayout, QSpinBox, QComboBox, QLabel)
from PyQt5.QtCore import pyqtSignal
from Player import Player


class NewGameDialog(QDialog):
    """ dialog for creating a new game """
    createGame = pyqtSignal(int, Player, Player)

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.playerB = Player("Black Player")
        self.playerW = Player("White Player")
        self.size = 19

        self.setModal(True)

        # buttons
        okBtn = QPushButton('Ok')
        okBtn.clicked.connect(self.okSlot)
        okBtn.clicked.connect(self.close)
        cancelBtn = QPushButton('Cancel')
        cancelBtn.clicked.connect(self.close)

        # LineEdits
        nameBField = QLineEdit("Black Player")
        nameBField.textChanged.connect(self.setBlackName)
        nameWField = QLineEdit("White Player")
        nameWField.textChanged.connect(self.setWhiteName)

        # Spin Box
        sizeBox = QSpinBox()
        sizeBox.setRange(2, 25)
        sizeBox.setValue(19)
        sizeBox.valueChanged.connect(self.setSize)

        # rank boxes
        ranks = ['?']
        for kyu in range(20, 0, -1):
            ranks.append(str(kyu)+'k')
        for dan in range(1, 9):
            ranks.append(str(dan)+'d')
        rankB = QComboBox()
        rankB.addItems(ranks)
        rankB.currentTextChanged.connect(self.setBlackRank)
        rankW = QComboBox()
        rankW.addItems(ranks)
        rankW.currentTextChanged.connect(self.setWhiteRank)

        # Layout
        hbox = QHBoxLayout()
        self.setLayout(hbox)

        vboxL = QVBoxLayout()
        vboxR = QVBoxLayout()
        hbox.addLayout(vboxL)
        hbox.addLayout(vboxR)

        vboxL.addWidget(QLabel("Board Size"))
        vboxR.addWidget(sizeBox)

        vboxL.addWidget(QLabel("Black Player Name: "))
        vboxR.addWidget(nameBField)

        vboxL.addWidget(QLabel("Black Player Rank:"))
        vboxR.addWidget(rankB)

        vboxL.addWidget(QLabel("White Player Name: "))
        vboxR.addWidget(nameWField)

        vboxL.addWidget(QLabel("White Player Rank:"))
        vboxR.addWidget(rankW)

        vboxL.addWidget(cancelBtn)
        vboxR.addWidget(okBtn)

    def setSize(self, size):
        self.size = size

    def setBlackName(self, string):
        self.playerB.set_name(string)

    def setWhiteName(self, string):
        self.playerW.set_name(string)

    def setWhiteRank(self, string):
        self.playerW.set_rank(string)

    def setBlackRank(self, string):
        self.playerB.set_rank(string)

    def okSlot(self):
        self.createGame.emit(self.size, self.playerB, self.playerW)


# Testing area
if __name__ == "__main__":
    pass
