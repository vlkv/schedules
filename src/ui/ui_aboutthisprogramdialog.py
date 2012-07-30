# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'aboutthisprogramdialog.ui'
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

class Ui_AboutThisProgramDialog(object):
    def setupUi(self, AboutThisProgramDialog):
        AboutThisProgramDialog.setObjectName(_fromUtf8("AboutThisProgramDialog"))
        AboutThisProgramDialog.resize(280, 175)
        self.verticalLayout = QtGui.QVBoxLayout(AboutThisProgramDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.textEdit = QtGui.QTextEdit(AboutThisProgramDialog)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.verticalLayout.addWidget(self.textEdit)
        self.buttonBox = QtGui.QDialogButtonBox(AboutThisProgramDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(AboutThisProgramDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), AboutThisProgramDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), AboutThisProgramDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AboutThisProgramDialog)

    def retranslateUi(self, AboutThisProgramDialog):
        AboutThisProgramDialog.setWindowTitle(QtGui.QApplication.translate("AboutThisProgramDialog", "О программе", None, QtGui.QApplication.UnicodeUTF8))
        self.textEdit.setHtml(QtGui.QApplication.translate("AboutThisProgramDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-weight:600;\">Schedules</span><span style=\" font-size:8pt;\"> - программа для исследования алгоритмов решения задач теории расписаний.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Автор: </span><span style=\" font-size:8pt; font-weight:600;\">Волков Виталий</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Контакты: </span><span style=\" font-size:8pt; font-weight:600;\">vitvlkv@gmail.com</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt; font-weight:600;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">2011 г.</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))

