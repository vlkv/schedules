# -*- coding: utf-8 -*-

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
from PyQt4.QtCore import Qt
import gui.mainwindow
import sys
import logging

if __name__ == '__main__':
 
    logger = logging.getLogger("")
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s: %(message)s')
    
    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(logging.DEBUG)
    consoleHandler.setFormatter(formatter)
    logger.addHandler(consoleHandler)
    
    app = QtGui.QApplication(sys.argv)
    mf = gui.mainwindow.MainWindow()
    mf.show()
    app.exec_()