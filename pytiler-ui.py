#!/usr/bin/env python

# Qt5 UI for PyTiler
#
# Author: Oxben <oxben@free.fr>

from __future__ import print_function

import sys
from PyQt5 import QtWidgets, QtGui


class PyTilerWin(QtWidgets.QWidget):
    '''PyTiler window'''
    def __init__(self):
        super(PyTilerWin, self).__init__()
        self.initUI()
        self.show()

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
        button =QtWidgets.QPushButton('...')
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
        hbox.addWidget(spin)
        label = QtWidgets.QLabel("Height:")
        hbox.addWidget(label)
        spin = QtWidgets.QSpinBox()
        hbox.addWidget(spin)
        combo = QtWidgets.QComboBox()
        combo.addItem('16x16', 16)
        combo.addItem('32x32', 32)
        combo.addItem('64x64', 64)
        combo.addItem('128x128', 128)
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
        hbox.addWidget(spin)
        label = QtWidgets.QLabel("Height:")
        hbox.addWidget(label)
        spin = QtWidgets.QSpinBox()
        hbox.addWidget(spin)
        combo = QtWidgets.QComboBox()
        combo.addItem('256x256', 256)
        combo.addItem('512x512', 512)
        combo.addItem('1024x1024', 1024)
        combo.addItem('2048x2048', 2048)
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
        hbox.addWidget(button)
        hbox.addStretch()
        innervbox.addLayout(hbox)

        vbox.addStretch()
        self.setLayout(vbox)


def main():
    app = QtWidgets.QApplication(sys.argv)
    w = PyTilerWin()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
