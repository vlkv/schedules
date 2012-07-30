# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'newscheduledialog.ui'
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

class Ui_NewScheduleDialog(object):
    def setupUi(self, NewScheduleDialog):
        NewScheduleDialog.setObjectName(_fromUtf8("NewScheduleDialog"))
        NewScheduleDialog.resize(395, 251)
        self.gridLayout = QtGui.QGridLayout(NewScheduleDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(NewScheduleDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.spinBoxProcCount = QtGui.QSpinBox(NewScheduleDialog)
        self.spinBoxProcCount.setMinimumSize(QtCore.QSize(75, 0))
        self.spinBoxProcCount.setObjectName(_fromUtf8("spinBoxProcCount"))
        self.gridLayout.addWidget(self.spinBoxProcCount, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel(NewScheduleDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.spinBoxTaskCount = QtGui.QSpinBox(NewScheduleDialog)
        self.spinBoxTaskCount.setMinimumSize(QtCore.QSize(75, 0))
        self.spinBoxTaskCount.setObjectName(_fromUtf8("spinBoxTaskCount"))
        self.gridLayout.addWidget(self.spinBoxTaskCount, 1, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(NewScheduleDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 8, 0, 1, 3)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 7, 0, 1, 1)
        self.groupBox = QtGui.QGroupBox(NewScheduleDialog)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.groupBox.setFont(font)
        self.groupBox.setFlat(True)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_2.setContentsMargins(0, 6, 0, 6)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label_3 = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setWeight(50)
        font.setBold(False)
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_2.addWidget(self.label_3, 1, 1, 1, 1)
        self.doubleSpinBoxResourceMin = QtGui.QDoubleSpinBox(self.groupBox)
        self.doubleSpinBoxResourceMin.setMinimumSize(QtCore.QSize(75, 0))
        font = QtGui.QFont()
        font.setWeight(50)
        font.setBold(False)
        self.doubleSpinBoxResourceMin.setFont(font)
        self.doubleSpinBoxResourceMin.setObjectName(_fromUtf8("doubleSpinBoxResourceMin"))
        self.gridLayout_2.addWidget(self.doubleSpinBoxResourceMin, 1, 2, 1, 1)
        self.label_4 = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setWeight(50)
        font.setBold(False)
        self.label_4.setFont(font)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_2.addWidget(self.label_4, 1, 4, 1, 1)
        self.doubleSpinBoxResourceMax = QtGui.QDoubleSpinBox(self.groupBox)
        self.doubleSpinBoxResourceMax.setMinimumSize(QtCore.QSize(75, 0))
        font = QtGui.QFont()
        font.setWeight(50)
        font.setBold(False)
        self.doubleSpinBoxResourceMax.setFont(font)
        self.doubleSpinBoxResourceMax.setObjectName(_fromUtf8("doubleSpinBoxResourceMax"))
        self.gridLayout_2.addWidget(self.doubleSpinBoxResourceMax, 1, 5, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 1, 6, 1, 1)
        self.label_6 = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setWeight(50)
        font.setBold(False)
        self.label_6.setFont(font)
        self.label_6.setWordWrap(True)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout_2.addWidget(self.label_6, 0, 1, 1, 6)
        spacerItem2 = QtGui.QSpacerItem(9, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem2, 1, 3, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 5, 0, 1, 3)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 0, 2, 1, 1)
        self.checkBoxArrangeTasksRandomly = QtGui.QCheckBox(NewScheduleDialog)
        self.checkBoxArrangeTasksRandomly.setObjectName(_fromUtf8("checkBoxArrangeTasksRandomly"))
        self.gridLayout.addWidget(self.checkBoxArrangeTasksRandomly, 2, 0, 1, 3)

        self.retranslateUi(NewScheduleDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), NewScheduleDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), NewScheduleDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(NewScheduleDialog)

    def retranslateUi(self, NewScheduleDialog):
        NewScheduleDialog.setWindowTitle(QtGui.QApplication.translate("NewScheduleDialog", "Создание расписания", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("NewScheduleDialog", "Кол-во исполнителей:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("NewScheduleDialog", "Кол-во заданий:", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("NewScheduleDialog", "Матрица ресурсов", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("NewScheduleDialog", "от", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("NewScheduleDialog", "до", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("NewScheduleDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Элементы матрицы ресурсов будут псевдослучайными числами с равномерным распределением, принадлежащие интервалу:</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxArrangeTasksRandomly.setText(QtGui.QApplication.translate("NewScheduleDialog", "Распределить задания в случайном порядке", None, QtGui.QApplication.UnicodeUTF8))

