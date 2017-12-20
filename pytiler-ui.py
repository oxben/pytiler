#!/usr/bin/env python

# Qt5 UI for PyTiler
#
# Author: Oxben <oxben@free.fr>

from __future__ import print_function

import sys
from PyQt5 import QtWidgets, QtGui, QtCore


TILE_WIDTH_MAX  = 1024
TILE_HEIGHT_MAX = 1024
OUT_WIDTH_MAX   = 4096
OUT_HEIGHT_MAX  = 4096

class PyTilerSignals(QtCore.QObject):
    '''Signals'''
    inputNameChanged = QtCore.pyqtSignal(str)
    outputNameChanged = QtCore.pyqtSignal(str)
    tileWidthChanged = QtCore.pyqtSignal(int)
    tileHeightChanged = QtCore.pyqtSignal(int)
    outWidthChanged = QtCore.pyqtSignal(int)
    outHeightChanged = QtCore.pyqtSignal(int)


class PyTilerWin(QtWidgets.QWidget):

    '''PyTiler window'''
    def __init__(self):
        super(PyTilerWin, self).__init__()
        self.sig = PyTilerSignals()
        self.initUI()
        self.show()

    def tileSizeChanged(self, size):
        if size.lower() != 'custom':
            self.sig.tileWidthChanged.emit(int(size.split('x')[0]))
            self.sig.tileHeightChanged.emit(int(size.split('x')[1]))

    def outSizeChanged(self, size):
        if size.lower() != 'custom':
            self.sig.outWidthChanged.emit(int(size.split('x')[0]))
            self.sig.outHeightChanged.emit(int(size.split('x')[1]))

    def chooseInputFilename(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Choose input file...')
        if filename:
            print(filename)
            self.sig.inputNameChanged.emit(filename)

    def chooseOutputFilename(self):
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Choose output file...')
        if filename:
            print(filename)
            self.sig.outputNameChanged.emit(filename)

    def initUI(self):
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('PyTiler')
        self.setWindowIcon(QtGui.QIcon('PatternBrick.png'))

        vbox = QtWidgets.QVBoxLayout()

        #
        # Input
        #
        gbox = QtWidgets.QGroupBox('Input')
        innervbox = QtWidgets.QVBoxLayout()
        gbox.setLayout(innervbox)
        vbox.addWidget(gbox)
        # Filename
        hbox = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel("Filename:")
        hbox.addWidget(label)
        edit = QtWidgets.QLineEdit()
        hbox.addWidget(edit)
        button = QtWidgets.QPushButton('...')
        button.clicked.connect(self.chooseInputFilename)
        self.sig.inputNameChanged.connect(edit.setText)
        hbox.addWidget(button)
        hbox.addStretch()
        innervbox.addLayout(hbox)

        #
        # Tiles
        #
        gbox = QtWidgets.QGroupBox('Tiles')
        innervbox = QtWidgets.QVBoxLayout()
        gbox.setLayout(innervbox)
        vbox.addWidget(gbox)
        # Size
        hbox = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel("Width:")
        hbox.addWidget(label)
        spin = QtWidgets.QSpinBox()
        spin.setMaximum(TILE_HEIGHT_MAX)
        self.sig.tileWidthChanged.connect(spin.setValue)
        hbox.addWidget(spin)
        label = QtWidgets.QLabel("Height:")
        hbox.addWidget(label)
        spin = QtWidgets.QSpinBox()
        spin.setMaximum(TILE_WIDTH_MAX)
        self.sig.tileHeightChanged.connect(spin.setValue)
        hbox.addWidget(spin)
        combo = QtWidgets.QComboBox()
        combo.addItem('Custom', 0)
        combo.addItem('16x16', 16)
        combo.addItem('32x32', 32)
        combo.addItem('64x64', 64)
        combo.addItem('128x128', 128)
        combo.currentIndexChanged[str].connect(self.tileSizeChanged)
        hbox.addWidget(combo)
        hbox.addStretch()
        innervbox.addLayout(hbox)
        # Size
        hbox = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel("Border Width:")
        hbox.addWidget(label)
        spin = QtWidgets.QSpinBox()
        hbox.addWidget(spin)
        hbox.addStretch()
        innervbox.addLayout(hbox)
        # Auto-generate tiles
        hbox = QtWidgets.QHBoxLayout()
        check = QtWidgets.QCheckBox('Auto-generate')
        hbox.addWidget(check)
        # Brick Layout
        check = QtWidgets.QCheckBox('Brick Layout')
        hbox.addWidget(check)
        innervbox.addLayout(hbox)

        #
        # Output
        #
        gbox = QtWidgets.QGroupBox('Output')
        innervbox = QtWidgets.QVBoxLayout()
        gbox.setLayout(innervbox)
        vbox.addWidget(gbox)
        # Size
        hbox = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel("Width:")
        hbox.addWidget(label)
        spin = QtWidgets.QSpinBox()
        spin.setMaximum(OUT_WIDTH_MAX)
        self.sig.outWidthChanged.connect(spin.setValue)
        hbox.addWidget(spin)
        label = QtWidgets.QLabel("Height:")
        hbox.addWidget(label)
        spin = QtWidgets.QSpinBox()
        spin.setMaximum(OUT_HEIGHT_MAX)
        self.sig.outHeightChanged.connect(spin.setValue)
        hbox.addWidget(spin)
        combo = QtWidgets.QComboBox()
        combo.addItem('Custom', 0)
        combo.addItem('256x256', 256)
        combo.addItem('512x512', 512)
        combo.addItem('1024x1024', 1024)
        combo.addItem('2048x2048', 2048)
        combo.currentIndexChanged[str].connect(self.outSizeChanged)
        hbox.addWidget(combo)
        hbox.addStretch()
        innervbox.addLayout(hbox)
        # Filename
        hbox = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel("Filename:")
        hbox.addWidget(label)
        edit = QtWidgets.QLineEdit()
        hbox.addWidget(edit)
        button =QtWidgets.QPushButton('...')
        button.clicked.connect(self.chooseOutputFilename)
        self.sig.outputNameChanged.connect(edit.setText)
        hbox.addWidget(button)
        hbox.addStretch()
        innervbox.addLayout(hbox)

        #
        # Render/Randomize
        #
        button = QtWidgets.QPushButton('Render')
        vbox.addWidget(button)

        vbox.addStretch()
        self.setLayout(vbox)


def main():
    app = QtWidgets.QApplication(sys.argv)
    w = PyTilerWin()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
