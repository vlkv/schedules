# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(719, 516)
        MainWindow.setDockOptions(QtGui.QMainWindow.AllowNestedDocks|QtGui.QMainWindow.AllowTabbedDocks|QtGui.QMainWindow.AnimatedDocks)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 719, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menu = QtGui.QMenu(self.menubar)
        self.menu.setObjectName(_fromUtf8("menu"))
        self.menu_2 = QtGui.QMenu(self.menubar)
        self.menu_2.setObjectName(_fromUtf8("menu_2"))
        self.menu_3 = QtGui.QMenu(self.menubar)
        self.menu_3.setObjectName(_fromUtf8("menu_3"))
        self.menu_4 = QtGui.QMenu(self.menubar)
        self.menu_4.setObjectName(_fromUtf8("menu_4"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionNewSchedule = QtGui.QAction(MainWindow)
        self.actionNewSchedule.setObjectName(_fromUtf8("actionNewSchedule"))
        self.actionSaveSchedule = QtGui.QAction(MainWindow)
        self.actionSaveSchedule.setObjectName(_fromUtf8("actionSaveSchedule"))
        self.actionOpenSchedule = QtGui.QAction(MainWindow)
        self.actionOpenSchedule.setObjectName(_fromUtf8("actionOpenSchedule"))
        self.actionUndoChange = QtGui.QAction(MainWindow)
        self.actionUndoChange.setObjectName(_fromUtf8("actionUndoChange"))
        self.actionRedoChange = QtGui.QAction(MainWindow)
        self.actionRedoChange.setObjectName(_fromUtf8("actionRedoChange"))
        self.actionStartAlekseev = QtGui.QAction(MainWindow)
        self.actionStartAlekseev.setObjectName(_fromUtf8("actionStartAlekseev"))
        self.actionDetachAllTasks = QtGui.QAction(MainWindow)
        self.actionDetachAllTasks.setObjectName(_fromUtf8("actionDetachAllTasks"))
        self.actionAboutThisProgram = QtGui.QAction(MainWindow)
        self.actionAboutThisProgram.setObjectName(_fromUtf8("actionAboutThisProgram"))
        self.menu.addAction(self.actionNewSchedule)
        self.menu.addAction(self.actionSaveSchedule)
        self.menu.addAction(self.actionOpenSchedule)
        self.menu_2.addAction(self.actionUndoChange)
        self.menu_2.addAction(self.actionRedoChange)
        self.menu_2.addAction(self.actionDetachAllTasks)
        self.menu_3.addAction(self.actionStartAlekseev)
        self.menu_4.addAction(self.actionAboutThisProgram)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())
        self.menubar.addAction(self.menu_4.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Теория расписаний", None, QtGui.QApplication.UnicodeUTF8))
        self.menu.setTitle(QtGui.QApplication.translate("MainWindow", "Расписание", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_2.setTitle(QtGui.QApplication.translate("MainWindow", "Правка", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_3.setTitle(QtGui.QApplication.translate("MainWindow", "Алгоритм", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_4.setTitle(QtGui.QApplication.translate("MainWindow", "Справка", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNewSchedule.setText(QtGui.QApplication.translate("MainWindow", "Создать", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNewSchedule.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+N", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSaveSchedule.setText(QtGui.QApplication.translate("MainWindow", "Сохранить", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSaveSchedule.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+S", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpenSchedule.setText(QtGui.QApplication.translate("MainWindow", "Загрузить", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpenSchedule.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+O", None, QtGui.QApplication.UnicodeUTF8))
        self.actionUndoChange.setText(QtGui.QApplication.translate("MainWindow", "Отменить действие", None, QtGui.QApplication.UnicodeUTF8))
        self.actionUndoChange.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Z", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRedoChange.setText(QtGui.QApplication.translate("MainWindow", "Повторить действие", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRedoChange.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Y", None, QtGui.QApplication.UnicodeUTF8))
        self.actionStartAlekseev.setText(QtGui.QApplication.translate("MainWindow", "Запуск алгоритма Алексеева", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDetachAllTasks.setText(QtGui.QApplication.translate("MainWindow", "Разгрузить всех исполнителей", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAboutThisProgram.setText(QtGui.QApplication.translate("MainWindow", "О программе", None, QtGui.QApplication.UnicodeUTF8))

