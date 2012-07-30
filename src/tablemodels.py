# -*- coding: utf-8 -*-
'''
Created on 04.09.2011

@author: vlkv
'''
import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
from PyQt4.QtCore import Qt
import errors


class ScheduleTableModel(QtCore.QAbstractTableModel):
    
    def __init__(self, schedule):
        super(ScheduleTableModel, self).__init__()
        self.__schedule = schedule
    
    COL_FREE_TASKS = 0
    COL_PROC_BEGIN = 1
    
    ROW_PROC_LOAD = 0
    ROW_PROC_LOAD_DEFICIT = 1
    ROW_MAX_FIXED_ROW = ROW_PROC_LOAD_DEFICIT 
    
    ROLE_TASK_RESOURCE = Qt.UserRole
    ROLE_TASK = Qt.UserRole + 1
    ROLE_PROC = Qt.UserRole + 2
    ROLE_IS_BOLD_FONT = Qt.UserRole + 3
    
    
    
    def scheduleBeginRow(self):
        return ScheduleTableModel.ROW_MAX_FIXED_ROW + 1
    
    def scheduleEndRow(self):
        return self.scheduleBeginRow() \
            + self.__schedule.maxTaskCountOfProcessor()
            
    def resMatrixBeginRow(self):
        return self.scheduleEndRow()
    
    def resMatrixEndRow(self):
        return self.resMatrixBeginRow() + self.__schedule.taskCount()
    
    def rowCount(self, index=QtCore.QModelIndex()):
        return self.resMatrixEndRow()
    
#    def _tasksRowCount(self):
#        return max(len(self.__schedule.detachedTasks()), \
#                   self.__schedule.maxTaskCountOfProcessor())
#    
    def columnCount(self, index=QtCore.QModelIndex()):
        return self.__schedule.processorCount() + 1
    
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                if section >= 1:
                    try:
                        proc = self.__schedule.processor(section - 1)
                        return proc.shortName()
                    except errors.IndexOutOfRangeError:
                        return None
                else:
                    return u"Свободные"
        
        elif orientation == Qt.Vertical:
            if role == Qt.DisplayRole:
                if section == ScheduleTableModel.ROW_PROC_LOAD:
                    return u"Загруженность"
                elif section == ScheduleTableModel.ROW_PROC_LOAD_DEFICIT:
                    return u"Дефицит загр."
                elif section < self.scheduleEndRow():
                    return section - self.scheduleBeginRow() + 1
                elif section < self.resMatrixEndRow():
                    return section - self.resMatrixBeginRow() + 1
            elif role == Qt.TextAlignmentRole:
                return int(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        
        return None
    
    
    def indexForTask(self, task):
        assert(self.__schedule.contains(task))
        row, col = None, None
        for j in xrange(self.__schedule.processorCount()):
            proc = self.__schedule.processor(j)
            for i in xrange(proc.taskCount()):
                if proc.task(i) == task:
                    row = i + self.scheduleBeginRow()
                    col = j + ScheduleTableModel.COL_PROC_BEGIN
        
        if row is None or col is None:
            row = self.__schedule.detachedTasks().index(task) + self.resMatrixBeginRow()
            col = ScheduleTableModel.COL_FREE_TASKS
        
        return self.createIndex(row, col)
        
    def canBeDragged(self, row, col):
        '''
        Начать перетаскивать мышью можно:
        1) задания уже назначенные на процессоры из области расписания
        2) свободные задания из первой колонки области матрицы ресурсов
        '''
        if self.scheduleBeginRow() <= row and row < self.scheduleEndRow():
            try:
                proc = self.__schedule.processor(col - ScheduleTableModel.COL_PROC_BEGIN)
                task = proc.task(row - self.scheduleBeginRow())
            except errors.IndexOutOfRangeError:
                return False
            return True
        elif self.resMatrixBeginRow() <= row and row < self.resMatrixEndRow():
            if col == ScheduleTableModel.COL_FREE_TASKS:
                task = self.__schedule.task(row - self.resMatrixBeginRow())
                return task in self.__schedule.detachedTasks()
        return False
    
    def canBeDroppedAt(self, row, col):
        '''
        Бросить перетаскиваемый обхект (задание) можно на
        1) область расписания - тогда задание (пере-)привяжется к процессору
        2) область матрицы ресурсов - тогда задание отвяжется от процессора        
        '''
        if self.scheduleBeginRow() <= row and row < self.scheduleEndRow():
            return col >= ScheduleTableModel.COL_PROC_BEGIN
        elif self.resMatrixBeginRow() <= row and row < self.resMatrixEndRow():
            return True
        else:
            return False
    
    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None
        
        row = index.row()
        col = index.column()
        
        #Special case: we must return proc object
        if role == ScheduleTableModel.ROLE_PROC \
        and col >= ScheduleTableModel.COL_PROC_BEGIN:
            proc = self.__schedule.processor(col - ScheduleTableModel.COL_PROC_BEGIN)
            return proc
        
        if row == ScheduleTableModel.ROW_PROC_LOAD:
            if col >= ScheduleTableModel.COL_PROC_BEGIN:
                proc = self.__schedule.processor(col - ScheduleTableModel.COL_PROC_BEGIN)
                if role == ScheduleTableModel.ROLE_TASK_RESOURCE:
                    return proc.load()
                if role == Qt.ToolTipRole:
                    return u"Загруженность %s" % proc.shortName()
            else:
                return None
            
        elif row == ScheduleTableModel.ROW_PROC_LOAD_DEFICIT:
            if col >= ScheduleTableModel.COL_PROC_BEGIN:
                proc = self.__schedule.processor(col - ScheduleTableModel.COL_PROC_BEGIN)
                if role == ScheduleTableModel.ROLE_TASK_RESOURCE:
                    return self.__schedule.procLoadDeficite(proc)
                if role == Qt.ToolTipRole:
                    return u"Дефицит загруженности %s" % proc.shortName()
            else:
                return None
            
        elif row < self.scheduleEndRow():
            if col >= ScheduleTableModel.COL_PROC_BEGIN:
                proc = self.__schedule.processor(col - ScheduleTableModel.COL_PROC_BEGIN)
                try:
                    task = proc.task(row - self.scheduleBeginRow())
                except errors.IndexOutOfRangeError:
                    return None
                
                if role == QtCore.Qt.DisplayRole:
                    return task.id()
                if role == ScheduleTableModel.ROLE_TASK_RESOURCE:
                    return task.resource(proc.id())                
                if role == ScheduleTableModel.ROLE_TASK:
                    return task
                if role == Qt.ToolTipRole:
                    return unicode(task)
                if role == ScheduleTableModel.ROLE_IS_BOLD_FONT:
                    return True
            else:
                return None
        elif row < self.resMatrixEndRow():
            task = self.__schedule.task(row - self.resMatrixBeginRow())
            if col == ScheduleTableModel.COL_FREE_TASKS:
                if role == QtCore.Qt.DisplayRole:
                    return task.id()
                if role == ScheduleTableModel.ROLE_TASK_RESOURCE:
                    return None #The is no processor in the column with index 0
                if role == ScheduleTableModel.ROLE_TASK:
                    return task
                if role == ScheduleTableModel.ROLE_PROC:
                    return None #The is no processor in the column with index 0
                if role == Qt.ToolTipRole:
                    return unicode(task)
                if role == ScheduleTableModel.ROLE_IS_BOLD_FONT:
                    if task in self.__schedule.detachedTasks():
                        return True
            else:
                proc = self.__schedule.processor(col - ScheduleTableModel.COL_PROC_BEGIN)
                if role == ScheduleTableModel.ROLE_TASK_RESOURCE:
                    return task.resource(proc.id())
        
        if role == QtCore.Qt.TextAlignmentRole:
            return int(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        
        if role == ScheduleTableModel.ROLE_IS_BOLD_FONT:
            return False
    
        #Во всех остальных случаях возвращаем None    
        return None
    
        
    
    def flags(self, index):
        defaultFlags = super(ScheduleTableModel, self).flags(index)
        return defaultFlags
    


