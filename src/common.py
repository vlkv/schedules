# -*- coding: utf-8 -*-
'''
Created on 31.07.2011

@author: vlkv
'''
import errors
import random
import serializer
import PyQt4.QtCore as QtCore
import copy
from fontTools.ttx import process

class Processor(serializer.Serializable):
    '''Процессор (или исполнитель) заданий.
    Очень важно, чтобы процессоры нумеровались с 1.
    '''
    
    __id = 1;

    def __init__(self, id=None):
        if id is None:
            self.__id = Processor.__id
            Processor.__id += 1
        else:
            self._setId(id)
        
        self.__tasks = []
        
    def id(self):
        return self.__id
    
    def _setId(self, id):
        self.__id = id
        if id >= Processor.__id:
            Processor.__id = id + 1

    def taskCount(self):
        return len(self.__tasks)
    
    def task(self, index):
        if index < 0 or index >= len(self.__tasks):
            raise errors.IndexOutOfRangeError()
        return self.__tasks[index]
    
    def taskById(self, taskId):
        index = next((i for i in xrange(len(self.__tasks)) 
                      if self.__tasks[i].id() == taskId), None)
        if index is not None:
            return self.__tasks[index]
        else:
            raise errors.IdNotFoundError()
        
    def indexForTask(self, task):
        '''Возвращает индекс задания в списке исполнителя, либо None, 
        если задания в списке нет.
        '''
        index = next((i for i in xrange(len(self.__tasks))
                     if self.__tasks[i].id() == task.id()), None)
        return index
    
    def load(self):
        '''
        Возвращает загруженность процессора - сумму ресурсов, необходимых
        для выполнения всех заданий, назначенный на данный процессор.
        '''
        return sum(self.task(i).resource(self.id()) for i in xrange(len(self.__tasks)))
    
    def appendTask(self, task):
        if task is None:
            raise errors.CantBeNoneError()
        if task in self.__tasks:
            raise errors.ItemPresentsError()
        self.__tasks.append(task)
                
    def insertTask(self, task, index):        
        self.__tasks.insert(index, task)
    
    def removeTask(self, index):
        if index < 0 or index >= len(self.__tasks):
            raise errors.IndexOutOfRangeError()
        self.__tasks[index].setProcessor(None)
        del self.__tasks[index]
        
    def removeTaskById(self, taskId):
        index = next((i for i in xrange(len(self.__tasks)) 
                      if self.__tasks[i].id() == taskId), None)
        if index is not None:
            del self.__tasks[index]
        else:
            raise errors.IdNotFoundError()

    def removeAllTasks(self):
        del self.__tasks[:]

    def __str__(self):
        tasksStr = "[" + ", ".join(["%s" % t for t in self.__tasks]) + "]"
        return "p_%(id)d %(tasks)s" % \
            {"id": self.__id, \
             "tasks": tasksStr }
    
    def shortName(self):
        return "p_%d" % self.__id
    
    def toJson(self):
        return {"__class__": self.__class__.__name__,
                "id": self.id(),
                "taskIds": list(self.__tasks[i].id() \
                                for i in xrange(len(self.__tasks))) }

class ConstProcessor(Processor):
    '''
    Класс-обёртка для класса Processor, у объектов которого нельзя вызывать
    никакие методы, модифицирующие его состояние.
    '''
    def __init__(self, proc):
        self._setId(proc.id())
        self._Processor__tasks = proc._Processor__tasks
    
    def appendTask(self):
        raise AttributeError()
    
    def insertTask(self):
        raise AttributeError()
    
    def removeTask(self):
        raise AttributeError()
    
    def removeTaskById(self):
        raise AttributeError()
    
    def removeAllTasks(self):
        raise AttributeError()
        
    
class Task(serializer.Serializable):
    '''Задание для выполнения на процессоре.
    Очень важно, чтобы задания нумеровались с 1.
    '''
    
    __id = 1;

    def __init__(self, resource=dict(), id=None):
        '''
        resource - это dict в котором ключ - id исполнителя, значение - 
            количество ресурсов, необходимых для выполнения данного задания на 
            конкретном исполнителе с идентификатором id.
        '''
        if id is None:
            self.__id = Task.__id
            Task.__id += 1
        else:
            self._setId(id)
        
        self.__resource = resource        
        
    def id(self):
        return self.__id
    
    def _setId(self, id):
        self.__id = id
        if id >= Task.__id:
            Task.__id = id + 1
    
    def resource(self, procId):
        '''
        procId - идентификатор исполнителя, для которого необходимо узнать, 
            сколько ресурсов необходимо для выполнения данного задания.
        Возвращает: численное значение ресурса для выполнения данного задания на 
            заданном исполнителе. Если возвращает None - значит данное задание
            не может быть вообще выполнено на данном исполнителе.
        '''
        try:
            res = self.__resource[procId]
        except KeyError:
            res = None
        return res
    
    def minResource(self):
        '''
        Возвращает минимум потребления ресурсов по всем процессорам.
        '''
        (k, v) = min(self.__resource.items(), key=lambda k: k[1])
        return v
        
        
    def __str__(self):
        res ="[" +  ", ".join("p_%d: %d" % (k, v) for k, v in self.__resource.items()) + "]"  
        return u"Задание t_%d, ресурсы=%s" % (self.__id, str(res))
    
    def shortName(self):
        return "t_%d" % self.__id
    
    def toJson(self):
        return {
                "__class__": self.__class__.__name__,
                "__module__": "common",
                "id": self.id(),
                "processorIdToResource": self.__resource
                }
    
    @staticmethod
    def fromJson(objState):
        resource = dict()
        for (procId, res) in objState["processorIdToResource"].items():
            resource[int(procId)] = int(res)
        task = Task(resource, objState["id"])
        return task    
    
class Schedule(serializer.Serializable):
    '''
    Расписание выполнения множества заданий на множестве процессоров.
    '''
    
    class ChangeInfo(object):
        def __init__(self, taskId, procFromId, procToId, insertIndex=None):
            self.taskId = taskId
            self.procFromId = procFromId
            self.procToId = procToId
            
            if procToId is None and insertIndex is not None:
                raise errors.ArgumentValueError()
            self.insertIndex = insertIndex
    
    def __init__(self):
        self.__processors = [] #Все имеющиеся процессоры
        self.__tasks = [] #Все имеющиеся задания
        self.__detachedTasks = [] #Задания, не привязанные к процессору
        
        self.__changeStack = [] #Стек модификаций расписания
        self.__changeStackNewPos = 0
        
        self.__guiListeners = []    #Виджеты, которые нужно оповещать, когда
                                    #расписание изменяется
        
    def __clearChangeUndoStack(self):
        self.__changeStack = []
        self.__changeStackNewPos = 0
        
    def addGuiListener(self, guiListener):
        self.__guiListeners.append(guiListener)
    
    def removeGuiListener(self, guiListener):
        self.__guiListeners.remove(guiListener)
        
    def removeAllGuiListeners(self):
        self.__guiListeners[:] = []
        
    def __notifyGuiListeners(self):
        for i in range(len(self.__guiListeners)):
            self.__guiListeners[i].processEvent()
    
    def __deepcopy__(self, memo):
        sch = Schedule()
        sch.__processors = copy.deepcopy(self.__processors, memo)
        sch.__tasks = copy.deepcopy(self.__tasks, memo)
        sch.__detachedTasks = copy.deepcopy(self.__detachedTasks, memo)
        sch.__changeStack = copy.deepcopy(self.__changeStack, memo)
        sch.__changeStackNewPos = copy.deepcopy(self.__changeStackNewPos, memo)
        #Игнорируем self.__guiListeners
        return sch
    
        
    def detachedTasks(self):
        '''
        Возвращает коллекцию заданий, которые не назначены ни на один процессор.
        '''
        return self.__detachedTasks
        
    def addTask(self, task):
        self.__tasks.append(task)
        self.__detachedTasks.append(task)
        self.__notifyGuiListeners()
        
    def addProcessor(self, proc):
        self.__processors.append(proc)
        self.__notifyGuiListeners()
    
    def processorCount(self):
        return len(self.__processors)

    def processor(self, index):
        if not (0 <= index < len(self.__processors)):
            raise errors.IndexOutOfRangeError()
        return ConstProcessor(self.__processors[index])
    
    def processorById(self, procId):
        index = next((i for i in xrange(len(self.__processors)) 
                      if self.__processors[i].id() == procId), None)
        if index is not None:
            return ConstProcessor(self.__processors[index])
        else:
            raise errors.IdNotFoundError()
    
    def contains(self, obj):
        if isinstance(obj, Task):
            return obj in self.__tasks
        elif isinstance(obj, Processor):
            return obj in self.__processors
        else:
            raise errors.ArgumentTypeError()
            
    
    def procLoadDeficite(self, proc):
        '''
        Разность между загрузкой исполнителя proc и 
        загрузкой максимально загруженного процессора в расписании. 
        '''
        return self.mostLoadedProc().load() - proc.load()

    def mostLoadedProc(self):
        load = None
        proc = None
        for i in range(self.processorCount()):
            procLoad = self.processor(i).load()
            if load is None \
            or procLoad > load:
                load = procLoad
                proc = self.processor(i)
        return ConstProcessor(proc)

    def maxProcLoad(self):
        return self.mostLoadedProc().load()
    
    def treeLeavesCount(self):
        return self.processorCount() ** self.taskCount() 
    
    def treeNodesCount(self):
        result = 0
        for i in range(0, self.taskCount() + 1):
            result += (self.processorCount() ** i)
        return result
        
    def leastLoadedProc(self):
        load = None 
        proc = None
        for i in range(self.processorCount()):
            procLoad = self.processor(i).load()
            if load is None \
            or procLoad < load:
                load = procLoad
                proc = self.processor(i)
        return ConstProcessor(proc)
    
    def minProcLoad(self):
        return self.leastLoadedProc().load()
    
    def averageProcLoad(self):
        load = 0.0
        for i in range(self.processorCount()):
            load += self.processor(i).load()
        load = load / self.processorCount()
        return load
        
    
    def processorForTask(self, task):
        for i in xrange(len(self.__processors)):
            proc = self.__processors[i]
            try:
                t = proc.taskById(task.id())
                return ConstProcessor(proc)
            except errors.IdNotFoundError:
                pass
        return None
    
    def processorForTaskId(self, taskId):
        for i in xrange(len(self.__processors)):
            proc = self.__processors[i]
            try:
                t = proc.taskById(taskId)
                return ConstProcessor(proc)
            except errors.IdNotFoundError:
                pass
        return None
    
    def bindedTaskCount(self):
        '''
        Количество заданий, которые назначенны на процессоры.
        '''
        return sum(self.__processors[i].taskCount() for i in range(len(self.__processors)))
    
    def taskCount(self):
        '''
        Общее количество заданий в расписании (назначенных на процессоры 
        и свободных).
        '''
        return len(self.__tasks)
    
    def task(self, index):
        if not (0 <= index < len(self.__tasks)):
            raise errors.IndexOutOfRangeError()
        return self.__tasks[index]
        
    def taskById(self, taskId):
        index = next((i for i in xrange(len(self.__tasks)) 
                      if self.__tasks[i].id() == taskId), None)
        if index is not None:
            return self.__tasks[index]
        else:
            raise errors.IdNotFoundError()
    
    def processorsWithMaxTaskCount(self):
        '''
        Возвращает список исполнителей, на которые назначено наибольшее
        количество заданий в расписании.
        '''
        processors = []
        maxTaskCount = 0
        for i in xrange(self.processorCount()):
            if self.processor(i).taskCount() > maxTaskCount:
                maxTaskCount = self.processor(i).taskCount()
                del processors[:]
                processors.append(ConstProcessor(self.processor(i)))
            elif self.processor(i).taskCount() == maxTaskCount:
                processors.append(ConstProcessor(self.processor(i)))
        return processors
    
    def maxTaskCountOfProcessor(self):
        '''Возвращает максимальное количество заданий, назначенных на один 
        процессор. Это максимум среди всех процессоров расписания.
        '''
        maxTaskCount = 0
        for i in xrange(self.processorCount()):
            if self.processor(i).taskCount() > maxTaskCount:
                maxTaskCount = self.processor(i).taskCount()
        return maxTaskCount
    
    def detachTaskFromProcessor(self, taskId):
        task = self.taskById(taskId)
        proc = self.processorForTaskId(taskId)
        if proc is None:
            raise errors.ItemNotFoundError(u"Не найден процессор для задания id=%s" % taskId)
        proc.removeTaskById(taskId)
        self.__detachedTasks.append(task)
        self.__notifyGuiListeners()
        self.__clearChangeUndoStack()
        
    
    def detachTasksFromProcessors(self):
        for i in xrange(len(self.__processors)):
            self.__processors[i].removeAllTasks()
        self.__detachedTasks[:] = self.__tasks
        self.__notifyGuiListeners()
        self.__clearChangeUndoStack()
    
    def detachTasksFromProcessorsWithUndo(self):
        for i in range(len(self.__processors)):
            proc = self.__processors[i] 
            for j in reversed(range(proc.taskCount())):
                task = proc.task(j)
                self.rebindTaskWithUndo(task, proc.id(), None)
        self.__notifyGuiListeners()
    
    def arrangeTasksRandomly(self):
        self.detachTasksFromProcessors()
        for i in xrange(len(self.__tasks)):
            procIndex = random.randint(0, self.processorCount() - 1)
            self.__processors[procIndex].appendTask(self.__tasks[i])
            self.__detachedTasks.remove(self.__tasks[i])
        self.__notifyGuiListeners()
        self.__clearChangeUndoStack()
    
    def undoChange(self):
        assert(self.__changeStackNewPos >= 0)
        assert(self.__changeStackNewPos <= len(self.__changeStack))
        if self.__changeStackNewPos > 0:
            self.__changeStackNewPos -= 1
            changeInfo = self.__changeStack[self.__changeStackNewPos]
            task = self.taskById(changeInfo.taskId)
            self.rebindTaskWithUndo(task, changeInfo.procToId, changeInfo.procFromId, \
                            changeInfo.insertIndex, saveThisChange=False)

    def redoChange(self):
        assert(self.__changeStackNewPos >= 0)
        assert(self.__changeStackNewPos <= len(self.__changeStack))
        if self.__changeStackNewPos < len(self.__changeStack):
            changeInfo = self.__changeStack[self.__changeStackNewPos]
            task = self.taskById(changeInfo.taskId)
            self.rebindTaskWithUndo(task, changeInfo.procFromId, changeInfo.procToId, \
                            changeInfo.insertIndex, saveThisChange=False)
            self.__changeStackNewPos += 1

    def getChangeInfo(self, index=0):
        '''index равный 0 соответствует последнему выполненному изменению.'''
        pos = self.__changeStackNewPos - 1 - index
        if (pos >= 0) and (pos < len(self.__changeStack)):
            return self.__changeStack[pos]
        else:
            return None
        

#    Метод заменен rebindTaskWithUndo
#    def bindDetachedTaskToProcWithUndo(self, task, proc, saveThisChange=True):
#        '''
#        Привязывает свободное задание task к процессору proc.
#        '''
#        if not (task in self.__tasks):
#            raise errors.ItemNotFoundError("Task id=%d not in a schedule" % task.id())
#        
#        if not (task in self.__detachedTasks):
#            raise errors.CannotBindTaskTwiceError()
#        
#        proc.appendTask(task)
#        self.__detachedTasks.remove(task)
#        
#        if saveThisChange:
#            self.__changeStack = self.__changeStack[0:self.__changeStackNewPos]
#            self.__changeStack.append(self.ChangeInfo(task.id(), None, proc.id()))
#            self.__changeStackNewPos += 1
        
        
    
    def rebindTaskWithUndo(self, task, procFromId, procToId, insertIndex=None, saveThisChange=True):
        '''Задание task, которое назначено на процессор procFrom
        переназначается на процессор procTo. insertIndex определяет позицию
        в списке заданий процессора procTo, куда будет вставлено задание task.
        Если insertIndex равно None, то task добавляется в конец списка заданий 
        процессора procTo.
        '''
        if not task in self.__tasks:
            raise errors.ItemNotFoundError("Task id=%d not in a schedule" % task.id())

        if procToId is not None:
            procTo = next((self.__processors[i] \
                            for i in xrange(self.processorCount()) \
                            if self.__processors[i].id() == procToId), None)
            if procTo is None:
                raise errors.ItemNotFoundError("Processor id=%d not in a schedule" % procToId)
        else:
            procTo = None

        if procFromId is not None:
            procFrom = next((self.__processors[i] \
                            for i in xrange(self.processorCount()) \
                            if self.__processors[i].id() == procFromId), None)
            if procFrom is None:
                raise errors.ItemNotFoundError("Processor id=%d not in a schedule" % procFromId)
        else:
            procFrom = None

        if procFrom is None and procTo is None:
            raise errors.NotEnoughArgumentsError()
        
        changeProcFromId = procFrom.id() if procFrom is not None else None
        if procFrom is not None:
            procFrom.removeTaskById(task.id())
            if procTo is None:
                self.__detachedTasks.append(task)
        
        changeProcToId = procTo.id() if procTo is not None else None
        changeInsertIndex = insertIndex if insertIndex is not None else None 
        if procTo is not None:
            if insertIndex is None:
                procTo.appendTask(task)
            else:
                procTo.insertTask(task, insertIndex)
        
            if procFrom is None:
                self.__detachedTasks.remove(task)

        if saveThisChange:
            self.__changeStack = self.__changeStack[0:self.__changeStackNewPos]
            self.__changeStack.append(self.ChangeInfo(task.id(), changeProcFromId, \
                                      changeProcToId, changeInsertIndex))
            self.__changeStackNewPos += 1
        self.__notifyGuiListeners()

    def toStrId(self):
        strId = ""
        proc = self.__processors[:]
        proc.sort(key=lambda p: p.id())
        
        strId = ";  ".join("p_" + str(proc[i].id()) + ":" + \
                         ",".join("t_" + str(proc[i].task(j).id()) \
                                  for j in range(proc[i].taskCount())) \
                         for i in range(len(proc)))
        return strId
    
    def fromStrId(self, strId):
        '''
        Восстанавливает свое состояние (размещение заданий по процессорам) 
        по строковому идентификатору (то что возвращает self.toStrId()).
        '''
        self.detachTasksFromProcessors()
        
        procList = strId.split(";")
        for i in range(len(procList)):
            
            tmp = procList[i].split(":")
            if len(tmp) != 2:
                continue

            proc, tasks = tmp[0], tmp[1]
            procNum = int(proc.strip()[2:])
            
            if len(tasks) > 0:
                taskList = tasks.split(",")
                for j in range(len(taskList)):
                    t = self.taskById(int(taskList[j].strip()[2:]))
                    self.rebindTaskWithUndo(t, None, procNum)
        
    
    def toJson(self):
        return {"__class__": self.__class__.__name__,
                "__module__": "common",
                "processors": list(self.__processors[i] for i in xrange(len(self.__processors))),
                "tasks": list(self.__tasks[i] for i in xrange(len(self.__tasks))),
                }
        
    @staticmethod
    def fromJson(objState):
        sch = Schedule()
        for task in objState["tasks"]:
            sch.addTask(task)
            
        for procState in objState["processors"]:
            proc = Processor(procState["id"])
            for taskId in procState["taskIds"]:
                task = sch.taskById(taskId)
                if sch.processorForTask(task) is not None:
                    raise errors.CannotBindTaskTwiceError()
                proc.appendTask(task)
                sch.__detachedTasks.remove(task)
            sch.addProcessor(proc)
        
#        sch._renumberTaskIds()
#        sch._renumberProcessorIds()

        return sch
    
#    def _renumberTaskIds(self):
#        id = 1
#        for i in range(len(self.__tasks)):
#            self.__tasks[i]._setId(id)
#            id += 1
#            
#    def _renumberProcessorIds(self):
#        id = 1
#        for i in range(len(self.__processors)):
#            self.__processors[i]._setId(id)
#            id += 1
        

class ScheduleFactory(object):
    '''
    Генератор случайных расписаний. 
    '''
    @staticmethod
    def createSchedule(procCount, taskCount, taskResourceRange):
        
        sch = Schedule();
        
        #Create processors
        for i in xrange(procCount):
            p = Processor(id=i+1)
            sch.addProcessor(p)
        
        #Create tasks and resource matrix
        minRes = taskResourceRange[0]
        maxRes = taskResourceRange[1]
        for i in xrange(taskCount):
            res = dict()
            for j in xrange(sch.processorCount()):
                res[sch.processor(j).id()] = random.randint(minRes, maxRes)
            t = Task(res, id=i+1)
            sch.addTask(t)

        return sch

#class Model(object):
#    
#    def __init__(self, sch=None):
#        self.__schedule = sch
#    
#    def setSchedule(self, sch):
#        self.__schedule = sch
#    
#    def schedule(self):
#        return self.__schedule
#        
    

    
if __name__ == '__main__':
    
    random.seed()
    sch = ScheduleFactory.createSchedule(3, 10, (100, 200))
    sch.arrangeTasksRandomly()
    print "minResource = %s" % str(sch.taskById(2).minResource())
    print str(sch.taskById(2))
    print str(sch)
    jsonStr = serializer.CustomEncoder(indent=4, sort_keys=True).encode(sch)
    print jsonStr
    obj = serializer.CustomDecoder().decode(jsonStr)
    print obj
    
    

    