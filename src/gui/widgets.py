# -*- coding: utf-8 -*-
'''
Created on 04.09.2011

@author: vlkv
'''

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
from PyQt4.QtCore import Qt
import ui.ui_schedulewidget
import ui.ui_totals
import tablemodels
from tablemodels import ScheduleTableModel
import common

class TotalsWidget(QtGui.QDockWidget):
    '''
    Плавающее окно для отображения различных общих итоговых
    данных о текущем расписании.
    '''
    def __init__(self, parent=None):
        super(TotalsWidget, self).__init__(parent)
        self.ui = ui.ui_totals.Ui_TotalsWidget()
        self.ui.setupUi(self)
        self.__schedule = None
    
    def setSchedule(self, schedule=None):
        if self.__schedule is not None:
            self.__schedule.removeGuiListener(self)
        
        self.__schedule = schedule
        if schedule is not None:
            self.__schedule.addGuiListener(self)
        
        self.updateUi()
    
    def processEvent(self):
        self.updateUi()
    
    def updateUi(self):
        if self.__schedule is not None:
            self.ui.lineEdit_minLoad.setText("%d" % self.__schedule.minProcLoad())
            self.ui.lineEdit_avgLoad.setText("%d" % self.__schedule.averageProcLoad())
            self.ui.lineEdit_maxLoad.setText("%d" % self.__schedule.maxProcLoad())
            self.ui.lineEdit_treeLeavesCount.setText("%d" % self.__schedule.treeLeavesCount())
            self.ui.lineEdit_treeNodesCount.setText("%d" % self.__schedule.treeNodesCount())
        else:
            self.ui.lineEdit_minLoad.setText()
            self.ui.lineEdit_avgLoad.setText()
            self.ui.lineEdit_maxLoad.setText()
            self.ui.lineEdit_treeLeavesCount.setText()
            self.ui.lineEdit_treeNodesCount.setText()

class ScheduleWidget(QtGui.QDockWidget):
    '''
    Плавающее окно для отображения расписания.
    '''
    
    def __init__(self, parent=None):
        super(ScheduleWidget, self).__init__(parent)
        self.ui = ui.ui_schedulewidget.Ui_ScheduleWidget()
        self.ui.setupUi(self)
        self.ui.scheduleTableView.setItemDelegate(TaskDelegate())
        self.ui.scheduleTableView.viewport().installEventFilter(self)
        self.__schedule = None
        self.__model = None
        
       
    def setSchedule(self, schedule):
        if self.__schedule is not None:
            self.__schedule.removeGuiListener(self)
        
        self.__schedule = schedule
        self.__model = tablemodels.ScheduleTableModel(schedule)
        if schedule is not None:
            self.__schedule.addGuiListener(self)
        
        self.ui.scheduleTableView.setModel(self.__model)
        self.ui.scheduleTableView.resizeRowsToContents()
    
    def processEvent(self):
        self.updateUi()
        
    def updateUi(self):
        if self.__schedule is not None:
            self.__model.reset()
            self.ui.scheduleTableView.resizeRowsToContents()
        
    def event(self, event):
#        print type(event).__name__ + " " + str(event.type())
        return True
    
    def eventFilter(self, watchedObj, event):
        #print type(event).__name__ + " " + str(event.type())
        if event.type() == QtCore.QEvent.MouseButtonPress and \
        event.button() == Qt.LeftButton:
            row = self.ui.scheduleTableView.rowAt(event.pos().y())
            col = self.ui.scheduleTableView.columnAt(event.pos().x())
            model = self.ui.scheduleTableView.model()
            if row <> -1 and col <> -1 \
            and model.canBeDragged(row, col):
                drag = QtGui.QDrag(self)
                mimeData = QtCore.QMimeData()
                mimeData.setText("%d, %d" % (row, col))
                drag.setMimeData(mimeData)
                drag.exec_()
            
        elif event.type() == QtCore.QEvent.DragEnter:
            event.acceptProposedAction()
        
        elif event.type() == QtCore.QEvent.DragMove:
            row = self.ui.scheduleTableView.rowAt(event.pos().y())
            col = self.ui.scheduleTableView.columnAt(event.pos().x())
            if row <> -1 and col <> -1:
                event.acceptProposedAction()
            else:
                event.ignore()
                
        elif event.type() == QtCore.QEvent.Drop:
            row = self.ui.scheduleTableView.rowAt(event.pos().y())
            col = self.ui.scheduleTableView.columnAt(event.pos().x())
            data = event.mimeData().text().split(",")
            srcRow = int(data[0])
            srcCol = int(data[1])
            model = self.ui.scheduleTableView.model()
            if row <> -1 and col <> -1 \
            and model.canBeDroppedAt(row, col) \
            and not (row == srcRow and col == srcCol):
#                print "Drag from (%d, %d), drop to (%d, %d)" % \
#                (srcRow, srcCol, row, col)
                self.trySwapCells((srcRow, srcCol), (row, col))
            
        return False
        
    def trySwapCells(self, cellFrom, cellTo):
        indexFrom = self.__model.createIndex(cellFrom[0], cellFrom[1])
        indexTo = self.__model.createIndex(cellTo[0], cellTo[1])
        taskFrom = self.__model.data(indexFrom, QtCore.Qt.UserRole + 1)
        procFrom = self.__model.data(indexFrom, QtCore.Qt.UserRole + 2)
        taskTo = self.__model.data(indexTo, QtCore.Qt.UserRole + 1)
        procTo = self.__model.data(indexTo, QtCore.Qt.UserRole + 2)
        #print "t_%s from p_%s to p_%s" % (str(taskFrom.id()), str(procFrom.id()), str(procTo.id()))
        
        
        if taskFrom is not None:
            self.__schedule.rebindTaskWithUndo(taskFrom, \
                    procFrom.id() if procFrom is not None else None, \
                    procTo.id() if procTo is not None else None, \
                    procTo.indexForTask(taskTo) if (taskTo is not None and procTo is not None) else None)
            self.updateUi()
            self.__indexTo = self.__model.indexForTask(taskFrom)
            QtCore.QTimer.singleShot(0, self.selectCell)
            

    def selectCell(self):
        self.ui.scheduleTableView.selectionModel().clearSelection()
        if self.__indexTo is not None:
            self.ui.scheduleTableView.selectionModel().select(self.__indexTo, \
                QtGui.QItemSelectionModel.Select)
            self.__indexTo = None
  
        
class TaskDelegate(QtGui.QStyledItemDelegate):
    '''Делегат, для отображения одного задания в таблице.'''

    formatTaskAndRes = '''<html>
     <style type="text/css">
        p {
        margin: 0px;        
        }  
    </style>
    <p align="center"><font size="+1">t_%s</font></p>
    <p align="right">%s</p>
    </html>'''
    
    formatTaskOnly = '''<html>
     <style type="text/css">
        p {
        margin: 0px;        
        }  
    </style>
    <p align="center"><font size="+1">t_%s</font></p>
    </html>'''
    
    formatResOnly = '''<html>
     <style type="text/css">
        p {
        margin: 0px;        
        }  
    </style>
    <p align="right">%s</p>
    </html>'''
    
    def __init__(self, parent=None):
        super(TaskDelegate, self).__init__(parent)
        
    def __makeRawText(self, taskNum, res):
        assert(taskNum is not None)
        assert(res is not None)
        numStr = taskNum.toString() if taskNum.isValid() else ""
        resStr = res.toString() if res.isValid() else ""
        raw_text = ""
        if len(numStr) > 0 and len(resStr) > 0:
            raw_text = TaskDelegate.formatTaskAndRes % (numStr, resStr)
        elif len(numStr) > 0:
            raw_text = TaskDelegate.formatTaskOnly % (numStr)
        elif len(resStr) > 0:
            raw_text = TaskDelegate.formatResOnly % (resStr)
        else:
            assert(False)
        return raw_text
        
    def sizeHint(self, option, index):
        num = index.data(Qt.DisplayRole)
        res = index.data(ScheduleTableModel.ROLE_TASK_RESOURCE)
        
        num = QtCore.QVariant() if num is None else num
        res = QtCore.QVariant() if res is None else res
        
        if num.isValid() or res.isValid():
            raw_text = self.__makeRawText(num, res)
            doc = QtGui.QTextDocument()
            doc.setTextWidth(option.rect.width())
            doc.setDefaultFont(option.font)
            doc.setHtml(raw_text)
            return QtCore.QSize(doc.size().width(), doc.size().height())
        else:
            return super(TaskDelegate, self).sizeHint(option, index) #Работает в PyQt начиная с 4.8.1
        
    def __isDataValid(self, dataResult):
        return dataResult is not None and dataResult.isValid()

    def paint(self, painter, option, index):
        
        palette = QtGui.QApplication.palette()
        
        non_selected_bg_color = palette.base().color() \
        if index.row() % 2 == 0 else palette.alternateBase().color()
        
        bg_color = palette.highlight().color() \
            if option.state & QtGui.QStyle.State_Selected \
            else non_selected_bg_color
            
        text_color = palette.highlightedText().color() \
            if option.state & QtGui.QStyle.State_Selected \
            else palette.text().color()
        
        num = index.data(Qt.DisplayRole)
        res = index.data(ScheduleTableModel.ROLE_TASK_RESOURCE)
        isBold = index.data(ScheduleTableModel.ROLE_IS_BOLD_FONT)
        
        num = QtCore.QVariant() if num is None else num
        res = QtCore.QVariant() if res is None else res
        
        if num.isValid() or res.isValid():
            raw_text = self.__makeRawText(num, res)
            doc = QtGui.QTextDocument()
            doc.setTextWidth(option.rect.width())
            option.font.setBold(isBold.toBool())
            doc.setDefaultFont(option.font)
            doc.setHtml(raw_text)
            
            cursor = QtGui.QTextCursor(doc)
            format = QtGui.QTextCharFormat()
            format.setForeground(QtGui.QBrush(text_color))
            cursor.movePosition(QtGui.QTextCursor.Start)
            cursor.movePosition(QtGui.QTextCursor.End, QtGui.QTextCursor.KeepAnchor)
            cursor.mergeCharFormat(format)
                    
            painter.save()
            painter.fillRect(option.rect, bg_color)
            painter.translate(option.rect.x(), option.rect.y())
            doc.drawContents(painter, QtCore.QRectF(0 ,0, option.rect.width(), option.rect.height()))            
            painter.restore()
    
        else:
            super(TaskDelegate, self).paint(painter, option, index)
    
#class NumberDelegate(QtGui.QStyledItemDelegate):
#    '''Делегат, для отображения одного числа в ячейке таблицы.'''
#
#    def __init__(self, parent=None):
#        super(NumberDelegate, self).__init__(parent)
#        
#    def sizeHint(self, option, index):
#        return super(NumberDelegate, self).sizeHint(option, index)
#            
#    def paint(self, painter, option, index):
#        super(NumberDelegate, self).paint(painter, option, index) #Работает в PyQt начиная с 4.8.1
    

    