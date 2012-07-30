# -*- coding: utf-8 -*-
'''
Created on 17.07.2011

@author: vlkv
'''

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
from PyQt4.QtCore import Qt
import ui.ui_mainwindow
import ui.ui_newscheduledialog
import ui.ui_aboutthisprogramdialog
import gui.widgets
from helpers import *
import common
import errors
import serializer
import algorithm

import os
import logging


class MainWindow(QtGui.QMainWindow):
    
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = ui.ui_mainwindow.Ui_MainWindow()
        self.ui.setupUi(self)
        self.setCentralWidget(None)
        self.setupUi()
        
        self.__schedule = None
        
        self.connect(self.ui.actionNewSchedule, QtCore.SIGNAL("triggered()"), \
                self.actionNewSchedule)
        self.connect(self.ui.actionSaveSchedule, QtCore.SIGNAL("triggered()"), \
                self.actionSaveSchedule)
        self.connect(self.ui.actionOpenSchedule, QtCore.SIGNAL("triggered()"), \
                self.actionOpenSchedule)
        self.connect(self.ui.actionUndoChange, QtCore.SIGNAL("triggered()"), \
                self.actionUndoChange)
        self.connect(self.ui.actionRedoChange, QtCore.SIGNAL("triggered()"), \
                self.actionRedoChange)
        self.connect(self.ui.actionDetachAllTasks, QtCore.SIGNAL("triggered()"), \
                self.actionDetachAllTasks)
        self.connect(self.ui.actionStartAlekseev, QtCore.SIGNAL("triggered()"), \
                self.actionStartAlekseev)
        self.connect(self.ui.actionAboutThisProgram, QtCore.SIGNAL("triggered()"), \
                self.actionAboutThisProgram)
        
        
    
    def setupUi(self):
        self.__schWidget = gui.widgets.ScheduleWidget(self)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.__schWidget)
        
        self.__totalsWidget = gui.widgets.TotalsWidget(self)
        self.addDockWidget(Qt.RightDockWidgetArea, self.__totalsWidget)
        
        geom = UserConfig().get("MainWindowGeometry")
        if geom is not None:
            self.setGeometry(QtCore.QRect(geom[0], geom[1], geom[2], geom[3]))

        state = UserConfig().get("MainWindowState")
        if state is not None:
            state = eval(state)
            self.restoreState(state)
            
        
    
    def closeEvent(self, event):
        
        stateByteArr = self.saveState()
        UserConfig().set("MainWindowState", repr(stateByteArr.data()))
        UserConfig().set("MainWindowGeometry", \
            [self.geometry().x(), self.geometry().y(), \
             self.geometry().width(), self.geometry().height()])        
    
    
    def actionNewSchedule(self):
        
        dialog = NewScheduleDialog(self)
        if dialog.exec_():
            sch = common.ScheduleFactory.createSchedule(
                dialog.procCount, 
                dialog.taskCount, 
                (dialog.resourceMin, dialog.resourceMax))
            if dialog.arrangeTasksRandomly:
                sch.arrangeTasksRandomly()
            self.__schedule = sch
            self.__schWidget.setSchedule(sch)
            self.__totalsWidget.setSchedule(sch)
        
    def actionSaveSchedule(self):
        try:    
            sch = self.__schedule
            if sch is None:
                raise errors.MessageError(u"Расписание не существует.")
            
            fileName = QtGui.QFileDialog.getSaveFileName(self, \
                u"Сохранить расписание", \
                UserConfig().get("FileDialogDirectoryDefault", "."))
            if fileName:
                fileNameWin = unicode(fileName).encode("cp1251")
                jsonStr = serializer.CustomEncoder(indent=4, sort_keys=True).encode(sch)
                file = open(fileNameWin, "w")
                file.write(jsonStr)
                file.close()
                UserConfig().set("FileDialogDirectoryDefault", \
                                 os.path.dirname(unicode(fileName)))
                            
        except Exception as ex:
            showExcInfo(self, ex)
        
    def actionOpenSchedule(self):
        try:
            fileName = QtGui.QFileDialog.getOpenFileName(self, \
                u"Загрузить расписание", \
                UserConfig().get("FileDialogDirectoryDefault", "."))
            if fileName:
                fileNameWin = unicode(fileName).encode("cp1251")
                file = open(fileNameWin, "r")
                jsonStr = file.read()
                sch = serializer.CustomDecoder().decode(jsonStr)
                self.__schedule = sch
                self.__schWidget.setSchedule(sch)
                self.__totalsWidget.setSchedule(sch)
                UserConfig().set("FileDialogDirectoryDefault", \
                                 os.path.dirname(unicode(fileName)))
            
        except Exception as ex:
            showExcInfo(self, ex)
    
    def actionUndoChange(self):
        self.__schedule.undoChange()
    
    def actionRedoChange(self):
        self.__schedule.redoChange()
        
    def actionDetachAllTasks(self):
        self.__schedule.detachTasksFromProcessorsWithUndo()
    
    def addFileLoggingHandler(self, filename):
        logger = logging.getLogger("")
        self.__fileHandler = logging.FileHandler("log.txt", "w", "utf8")
        self.__fileHandler.setLevel(logging.DEBUG)
        self.__fileHandler.setFormatter(logging.Formatter('%(asctime)s %(name)s %(levelname)s: %(message)s'))
        logger.addHandler(self.__fileHandler)
    
    def removeFileLoggingHandler(self):
        logger = logging.getLogger("")
        logger.removeHandler(self.__fileHandler)
    
    def actionStartAlekseev(self):
        assert(self.__schedule is not None)
        self.addFileLoggingHandler("log.txt")
        algThread = algorithm.AlekseevThread(self.__schedule, self)
        self.connect(algThread, QtCore.SIGNAL("candidateFound"), self.onAlgorithmFoundCandidate)
        self.connect(algThread, QtCore.SIGNAL("finished"), self.onAlgorithmFinished)
        #algThread.start()
        algThread.run()
        
        
    def onAlgorithmFoundCandidate(self, scheduleResultCandidate):
        self.__schedule = scheduleResultCandidate
        self.__schWidget.setSchedule(scheduleResultCandidate)
        self.__totalsWidget.setSchedule(scheduleResultCandidate)
        
    def onAlgorithmFinished(self, algThread):
        self.removeFileLoggingHandler()
        sch = algThread.result()
        self.__schedule = sch
        self.__schWidget.setSchedule(sch)
        self.__totalsWidget.setSchedule(sch)
        
    
    def actionAboutThisProgram(self):
        aboutDialog = QtGui.QDialog(self)
        aboutDialog.ui = ui.ui_aboutthisprogramdialog.Ui_AboutThisProgramDialog()
        aboutDialog.ui.setupUi(aboutDialog)
        aboutDialog.exec_()
        
        
class NewScheduleDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        super(NewScheduleDialog, self).__init__(parent)
        self.ui = ui.ui_newscheduledialog.Ui_NewScheduleDialog()
        self.ui.setupUi(self)
        
        procCount = int(UserConfig().get("ProcessorCountDefault", 3))
        self.ui.spinBoxProcCount.setValue(procCount)
        
        taskCount = int(UserConfig().get("TaskCountDefault", 8))
        self.ui.spinBoxTaskCount.setValue(taskCount)
        
        arrangeTasksRandomly = bool(UserConfig().get("ArrangeTasksRandomlyDefault", True))
        self.ui.checkBoxArrangeTasksRandomly.setChecked(arrangeTasksRandomly)
        
        resourceMin = float(UserConfig().get("ResourceMinDefault", 20.0))
        self.ui.doubleSpinBoxResourceMin.setValue(resourceMin)
        
        resourceMax = float(UserConfig().get("ResourceMaxDefault", 40.0))
        self.ui.doubleSpinBoxResourceMax.setValue(resourceMax)
        
        self.connect(self.ui.buttonBox, QtCore.SIGNAL("accepted()"), \
                self.acceptedButton)
        self.connect(self.ui.buttonBox, QtCore.SIGNAL("rejected()"), \
                self.rejectedButton)
    
    def acceptedButton(self):
        self.procCount = self.ui.spinBoxProcCount.value()
        self.taskCount = self.ui.spinBoxTaskCount.value()
        self.arrangeTasksRandomly = self.ui.checkBoxArrangeTasksRandomly.isChecked()
        self.resourceMin = self.ui.doubleSpinBoxResourceMin.value()
        self.resourceMax = self.ui.doubleSpinBoxResourceMax.value()
        
        UserConfig().set("ProcessorCountDefault", self.procCount)
        UserConfig().set("TaskCountDefault", self.taskCount)
        UserConfig().set("ArrangeTasksRandomlyDefault", self.arrangeTasksRandomly)
        UserConfig().set("ResourceMinDefault", self.resourceMin)
        UserConfig().set("ResourceMaxDefault", self.resourceMax)
        
        self.accept()
    
    def rejectedButton(self):
        self.reject()
    
    
    
    
    
    
    
    