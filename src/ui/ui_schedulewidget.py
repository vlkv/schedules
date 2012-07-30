# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'schedulewidget.ui'
#
# Created: Sat Nov 05 19:07:45 2011
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_ScheduleWidget(object):
    def setupUi(self, ScheduleWidget):
        ScheduleWidget.setObjectName(_fromUtf8("ScheduleWidget"))
        ScheduleWidget.resize(400, 300)
        ScheduleWidget.setFeatures(QtGui.QDockWidget.DockWidgetFloatable|QtGui.QDockWidget.DockWidgetMovable)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.verticalLayout = QtGui.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.scheduleTableView = QtGui.QTableView(self.dockWidgetContents)
        self.scheduleTableView.setDragEnabled(True)
        self.scheduleTableView.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        self.scheduleTableView.setAlternatingRowColors(True)
        self.scheduleTableView.setSelectionMode(QtGui.QAbstractItemView.ContiguousSelection)
        self.scheduleTableView.setObjectName(_fromUtf8("scheduleTableView"))
        self.verticalLayout.addWidget(self.scheduleTableView)
        ScheduleWidget.setWidget(self.dockWidgetContents)

        self.retranslateUi(ScheduleWidget)
        QtCore.QMetaObject.connectSlotsByName(ScheduleWidget)

    def retranslateUi(self, ScheduleWidget):
        ScheduleWidget.setWindowTitle(QtGui.QApplication.translate("ScheduleWidget", "Расписание", None, QtGui.QApplication.UnicodeUTF8))

