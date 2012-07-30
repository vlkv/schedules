# -*- coding: utf-8 -*-
'''
Created on 29.09.2011

@author: vlkv
'''
import math
import copy
import errors
import logging
from PyQt4 import QtCore
import time


class Tree(object):
    '''Дерево решений. Это нечто вроде кеша для узлов. '''
    
    def __init__(self, arity, height):
        '''
        arity - это арность дерева. Равна количеству процессоров задачи.
        height - высота дерева (количество уровней). Равно 
            количество_заданий + 1
        '''
        assert(arity >= 2)
        assert(height > 0)
        self.__arity = arity
        self.__height = height
        self.__nodes = dict() #Ключ - это кортеж (z, x)
        
        self.cutNodesCount = 0
        self.seenNodesCount = 0
        self.includedNodesCount = 0
    
    def incNodeCounters(self, seen=0, included=0, cut=0):
        assert(seen >= 0)
        assert(included >= 0)
        assert(cut >= 0)
        self.cutNodesCount += cut
        self.seenNodesCount += seen
        self.includedNodesCount += included
    
    def resetNodeCounters(self):
        self.cutNodesCount = 0
        self.seenNodesCount = 0
        self.includedNodesCount = 0    
    
    def height(self):
        return self.__height
    
    def arity(self):
        return self.__arity
    
    def tasksCount(self):
        return self.height() - 1
    
    def processorsCount(self):
        return self.arity()
    
    def getParent(self, node):
        assert(not node.isRootParent())
        parentZ = node.z() - 1
        parentX = 0 if parentZ <= 0 else int(node.x()) / int(self.__arity)
        if not (parentZ, parentX) in self.__nodes:
            self.__nodes[(parentZ, parentX)] = TreeNode(self, parentZ, parentX)
        return self.__nodes[(parentZ, parentX)]
        
    def getChild(self, node, childX):
        assert(not node.isLeaf())
        assert(childX >= 0)
        assert(childX < self.__arity ** (node.z() + 1))
        childZ = node.z() + 1
        if not (childZ, childX) in self.__nodes:
            self.__nodes[(childZ, childX)] = TreeNode(self, childZ, childX)
        return self.__nodes[(childZ, childX)]

    def getRoot(self):
        return self.getNode(z=0, x=0)
    
    def getRootParent(self):
        return self.getNode(z=-1, x=0)
    
    def getNode(self, z, x):
        index = (z, x)
        if not index in self.__nodes:
            self.__nodes[index] = TreeNode(self, index[0], index[1])
        return self.__nodes[index]
        
    

class TreeNode(object):
    '''Узел дерева решений распределительной задачи.'''
    
    def __init__(self, tree, z=0, x=0):
        '''
        z - уровень, на котором находится узел. Корень находится на уровне 0
            На уровне z = -1 находится фиктивный узел (т.е. узел который выше корня).
        x - позиция узла в пределах его уровня (т.е. это номер среди узлов-братьев).
            На каждом уровне z находится ровно treeArity ** z узлов.
        '''
        assert(z >= -1)
        assert(z < tree.height())
        assert(x >= 0)
        assert((x < tree.arity() ** z) or (x == 0 and z == -1))
        self.__z = z
        self.__x = x
        self.__tree = tree
        self.__lowerBound = None
        self.wasSeen = False
        self.wasIncluded = False
        self.subTreeIncludedNodesCount = None #Кол-во узлов, добавленных в решение (возможно их потом убрали из решения, неважно)
        self.subTreeSeenNodesCount = None #Кол-во узлов, которые только оценивались, но не были добавлены в решение
        #Все Included-узлы являются также и Seen-узлами
    
    def x(self):
        return self.__x
    
    def z(self):
        return self.__z
    
    def taskId(self):
        assert(not self.isRoot()) #Корню не соответствует никакой таск
        return self.__z
        
    def procId(self):
        assert(not self.isRoot()) #Корню не соответствует никакой процессор
        procId = 1 + (int(self.__x) % int(self.__tree.arity()))
        return procId
   
    def isLeaf(self):
        return (self.__z == self.__tree.height() - 1)

    def isRoot(self):
        return (self.__z == 0)
    
    def isRootParent(self):
        '''
        rootParent --- это специальный узел, который находится выше корня.
        Он нужен для удобства обхода дерева.
        '''
        return (self.__z == -1 and self.__x == 0)
    
    def getParent(self):
        return self.__tree.getParent(self)
    
    def getChild(self, childX):
        return self.__tree.getChild(self, childX)
    
    def getChildren(self):
        result = []
        for i in range(self.__tree.arity()):
            result.append(self.__tree.getChild(self, self.x() * self.__tree.arity() + i))
        return result
    
    def subTreeNodesCount(self):
        '''
        Количество узлов в поддереве, корнем которого является данный узел.
        '''
        if (self.isLeaf()):
            return 1
        result = 0
        for i in range(0, self.__tree.tasksCount() - self.__z + 1):
            result += self.__tree.processorsCount() ** i 
        return result
    
    def subTreeCutNodesCount(self):
        return self.subTreeNodesCount() - self.subTreeSeenNodesCount
    
    def toString(self):
        return "TreeNode(z=%d x=%d)" % (self.__z, self.__x)
    
    def toStrId(self):
        '''
        Возвращает уникальный для данного узла дерева строковый идентификатор
        пути от корня до данного узла.
        '''
        
        path = []
        node = self
        while not node.isRoot():
            path.insert(0, node)
            node = node.getParent()
        
        procIdToTaskIdList = dict()
        for procId in range(self.__tree.processorsCount()):
            procIdToTaskIdList[procId + 1] = []

        for i in range(len(path)):
            procIdToTaskIdList[path[i].procId()].append(path[i].taskId())
        
        strId = ""
        for i in range(self.__tree.processorsCount()):
            procId = i + 1
            strId += "p_%d:" % procId
            for j in range(len(procIdToTaskIdList[procId])):
                strId += "t_%d" % procIdToTaskIdList[procId][j]
                if j < len(procIdToTaskIdList[procId]) - 1:
                    strId += ","
            
            strId += "; "
            
        return strId
                
            
        
    
    def getLowerBound(self):
        return self.__lowerBound
    
    def setLowerBound(self, value):
        self.__lowerBound = value
    
    
class AlekseevThread(QtCore.QThread):
    '''
    Классический алгоритм Алексеева для решения неоднородной распределительной
    задачи теории расписаний.
    '''
    
    DIR_UP = 'DIR_UP'
    DIR_DOWN = 'DIR_DOWN' 
    
    def __init__(self, schedule, parent=None):
        super(AlekseevThread, self).__init__(parent)
        self.__logger = logging.getLogger(__name__ + "." + self.__class__.__name__)
        self._schedule = schedule
        
        self._m = self._schedule.taskCount()
        self._n = self._schedule.processorCount()
        if self._m <= self._n:
            raise errors.ArgumentValueError()
        
        self._tau = self._calcTau()
        self._tFloor = self._calcTFloor()
        
        self._tree = Tree(self._n, self._m + 1)
        
    def _calcTau(self):
        return list(self._schedule.task(i).minResource() \
                         for i in range(self._schedule.taskCount()))
        
    def _calcTFloor(self):
        one = sum(self._tau) / float(self._n)
        two = max(self._tau)
        return max(one, two)
        
    def _calcBranchLowerBound(self, node):
        '''
        Вычисляется оценка снизу для текущего состояния частично 
        сформированного расписания.
        '''
        result = node.getLowerBound()
        if result is None:
            strId = node.toStrId()
            branch = copy.deepcopy(self._schedule)
            branch.fromStrId(strId)
        
            if len(branch.detachedTasks()) == 0:
                result = branch.maxProcLoad()
            else:
                tauOfDetachedTasks = list(branch.detachedTasks()[i].minResource() \
                                        for i in range(len(branch.detachedTasks())))
                maxTauOfDetachedTasks = max(tauOfDetachedTasks)
                z = branch.bindedTaskCount()
                r = self._n if (z <= self._m - self._n) else (self._m - z)
                
                proc = list(branch.processor(i) \
                            for i in range(branch.processorCount()))
                proc.sort(key=lambda p: p.load())
                maxLoad = proc[len(proc) - 1].load()
                
                sumLoad = sum(proc[i].load() for i in range(r))
                sumTau = sum(tauOfDetachedTasks)
                tz = (sumLoad + sumTau) / float(r)
                
                result = max(max(tz, maxLoad), maxTauOfDetachedTasks)
            
            node.setLowerBound(result)
        return result
    
    def _indexOfNodeWithMinLowerBound(self, nodes):
        minIndex = None #индекс дочернего узла с наименьшей оценкой
        minLowerBound = float("inf")
        for i in range(len(nodes)):
            lowerBound = self._calcBranchLowerBound(nodes[i])
            if lowerBound < minLowerBound:
                minLowerBound = lowerBound
                minIndex = i
        return minIndex, minLowerBound
        
    
    def __resetTimer(self):
        #self.__lastUpdatedTime = time.time()
        #self.__lastSeenNodesTotalCount = 0
        pass

    def __updateTimer(self):
        now = time.time()
#        if (now - self.__lastUpdatedTime >= 1.0):
#            deltaCount = self._seenNodesTotalCount - self.__lastSeenNodesTotalCount
#            self.__lastUpdatedTime = now
#            self.__lastSeenNodesTotalCount = self._seenNodesTotalCount
#            self.__logger.info("speed = %d operations per second" % (deltaCount))
            
        
    def __subTreeNodesCount(self, z):
        ''' Количество узлов в поддереве уровня z.'''
        if (z > self._m):
            return 0 #Нет никакого поддерева в данном случае
        result = 0
        for i in range(0, self._m - z + 1):
            result += self._n ** i 
        return result
        
    def run(self):
        self.__logger.info("START")
        
        self.__logger.info("T0 = " + str(self._tFloor))
        
        schedule = copy.deepcopy(self._schedule)
        schedule.detachTasksFromProcessors()
        
        self.__resetTimer()
        
        tCeil = float("inf")
        candidates = []
        stop = False
        
        dir = AlekseevThread.DIR_DOWN
        node = self._tree.getRoot()
        node.subTreeSeenNodesCount = 1
        node.subTreeIncludedNodesCount = 0
        while not stop:
            while not node.isLeaf() and not stop:
                
                self.__logger.warn("z=%d" % (node.z()))
                children = node.getChildren()
                minIndex, minLowerBound = self._indexOfNodeWithMinLowerBound(children)
                for child in children:
                    if child.wasSeen:
                        continue
                    child.wasSeen = True
                    child.subTreeSeenNodesCount = 1
                    child.subTreeIncludedNodesCount = 0
                
                if minLowerBound < tCeil:
                    dir = AlekseevThread.DIR_DOWN
                    node = children[minIndex]
                    node.wasIncluded = True
                    node.subTreeIncludedNodesCount = 1
                                
                    self.__logger.info("Task %s added to %s" \
                        % (schedule.taskById(node.taskId()).shortName(), \
                           schedule.processorById(node.procId()).shortName()))
                else:
                    assert(not node.isRootParent())
                    dir = AlekseevThread.DIR_UP
                    prevNode = node
                    node = node.getParent()
                    prevNode.subTreeIncludedNodesCount += sum(child.subTreeIncludedNodesCount for child in prevNode.getChildren())
                    prevNode.subTreeSeenNodesCount += sum(child.subTreeSeenNodesCount for child in prevNode.getChildren())
                    if node.isRootParent():
                        stop = True
                        self.__logger.info("Exit, the whole tree has been walked.")
                    else:
                        prevNode.setLowerBound(float("inf"))
                        
                        self.__logger.info("Task %s removed from %s" \
                            % (schedule.taskById(prevNode.taskId()).shortName(), \
                            schedule.processorById(prevNode.procId()).shortName()))
                        self.__logger.info("%s: subTreeSeenNodes=%d subTreeIncludedNodes=%d subTreeCutNodes=%d" \
                            % (prevNode.toString(), \
                            prevNode.subTreeSeenNodesCount, prevNode.subTreeIncludedNodesCount, \
                            prevNode.subTreeCutNodesCount()))
                    
                self.__updateTimer()
                
                    
            
            if stop:
                break            
            
            schedule.fromStrId(node.toStrId())
            if schedule.bindedTaskCount() == schedule.taskCount():
                assert(tCeil >= schedule.maxProcLoad())
                tCeil = schedule.maxProcLoad()
                candidates.append(copy.deepcopy(schedule))
                self.emit(QtCore.SIGNAL("candidateFound"), candidates[-1])
                self.__logger.warn("Candidate found " + candidates[-1].toStrId() +\
                                    " load " + str(candidates[-1].maxProcLoad()))
            
            assert(node.isLeaf())
            if tCeil == self._tFloor:
                stop = True
                self.__logger.info("Exit, we've found solution with tFloor value!")
            else:
                dir = AlekseevThread.DIR_UP
                prevNode = node
                node = node.getParent()
                if node.isRootParent():
                    #Сюда по идее не можем попасть!
                    stop = True
                    self.__logger.info("Exit...")
                else:
                    prevNode.setLowerBound(float("inf"))
                    self.__logger.info("Task %s removed from %s" \
                        % (schedule.taskById(prevNode.taskId()).shortName(), \
                        schedule.processorById(prevNode.procId()).shortName()))
                    self.__logger.info("%s: subTreeSeenNodes=%d subTreeIncludedNodes=%d subTreeCutNodes=%d" \
                        % (prevNode.toString(), \
                        prevNode.subTreeSeenNodesCount, prevNode.subTreeIncludedNodesCount, \
                        prevNode.subTreeCutNodesCount()))
        
        minIndex = -1
        minProcLoad = None
        for i in range(len(candidates)):
            if minProcLoad is None \
            or candidates[i].maxProcLoad() < minProcLoad:
                minIndex = i
                minProcLoad = candidates[i].maxProcLoad()
            self.__logger.info("Candidate " + candidates[i].toStrId() + " load " + str(candidates[i].maxProcLoad())) 
                
        assert(minIndex >= 0)
        self._result = candidates[minIndex]

        root = self._tree.getRoot()
        self.__logger.info("%s: subTreeSeenNodes=%d subTreeIncludedNodes=%d subTreeCutNodes=%d" \
            % (root.toString(), \
            root.subTreeSeenNodesCount, root.subTreeIncludedNodesCount, \
            root.subTreeCutNodesCount()))

        self.__logger.info("FINISH")
        self.emit(QtCore.SIGNAL("finished"), self)
        
    def result(self):
        return self._result
                
    

        
#class AlekseevThread(QtCore.QThread):
#    '''
#    Классический алгоритм Алексеева для решения неоднородной распределительной
#    задачи теории расписаний.
#    '''
#    
#    def __init__(self, schedule, parent=None):
#        super(AlekseevThread, self).__init__(parent)
#        self.__logger = logging.getLogger(__name__ + "." + self.__class__.__name__)
#        self._schedule = schedule
#        
#        self._m = self._schedule.taskCount()
#        self._n = self._schedule.processorCount()
#        if self._m <= self._n:
#            raise errors.ArgumentValueError()
#        
#        self._tau = self._calcTau()
#        self._tFloor = self._calcTFloor()
#        
#        self._lowerBoundsCache = dict()
#        self._seenNodesCount = [0] * (self._m + 2) #Индекс - это z уровень дерева. Временные счетчики просмотренных вершин в поддереве уровня z 
#        self._seenNodesTotalCount = 0 #Количество просмотренных вершин
#        self._cutNodesTotalCount = 0 #Отсеченные вершины, которые не нужно просматривать
#        
#    def _calcTau(self):
#        return list(self._schedule.task(i).minResource() \
#                         for i in range(self._schedule.taskCount()))
#        
#    def _calcTFloor(self):
#        one = sum(self._tau) / float(self._n)
#        two = max(self._tau)
#        return max(one, two)
#        
#    def _calcBranchLowerBound(self, branch):
#        '''
#        branch - это экземпляр Schedule. Вычисляется оценка снизу для 
#        текущего состояния расписания.
#        '''
#        
#        strId = branch.toStrId()
#        if strId not in self._lowerBoundsCache:
#            
#            if len(branch.detachedTasks()) == 0:
#                result = branch.maxProcLoad()
#            else:
#                tauOfDetachedTasks = list(branch.detachedTasks()[i].minResource() \
#                                        for i in range(len(branch.detachedTasks())))
#                maxTauOfDetachedTasks = max(tauOfDetachedTasks)
#                z = branch.bindedTaskCount()
#                r = self._n if (z <= self._m - self._n) else (self._m - z)
#                
#                proc = list(branch.processor(i) \
#                            for i in range(branch.processorCount()))
#                proc.sort(key=lambda p: p.load())
#                maxLoad = proc[len(proc) - 1].load()
#                
#                sumLoad = sum(proc[i].load() for i in range(r))
#                sumTau = sum(tauOfDetachedTasks)
#                tz = (sumLoad + sumTau) / float(r)
#                
#                result = max(max(tz, maxLoad), maxTauOfDetachedTasks)
#            self._lowerBoundsCache[strId] = result
#            
#        return self._lowerBoundsCache[strId]
#    
#    def __resetTimer(self):
#        self.__lastUpdatedTime = time.time()
#        self.__lastSeenNodesTotalCount = 0
#
#    def __updateTimer(self):
#        now = time.time()
#        if (now - self.__lastUpdatedTime >= 1.0):
#            deltaCount = self._seenNodesTotalCount - self.__lastSeenNodesTotalCount
#            self.__lastUpdatedTime = now
#            self.__lastSeenNodesTotalCount = self._seenNodesTotalCount
#            self.__logger.info("speed = %d operations per second" % (deltaCount))
#        
#    def __subTreeNodesCount(self, z):
#        ''' Количество узлов в поддереве уровня z.'''
#        if (z > self._m):
#            return 0 #Нет никакого поддерева в данном случае
#        result = 0
#        for i in range(0, self._m - z + 1):
#            result += self._n ** i 
#        return result
#        
#    def run(self):
#        self.__logger.info("START")
#        
#        self.__logger.info("T0 = " + str(self._tFloor))
#        
#        schedule = copy.deepcopy(self._schedule)
#        schedule.detachTasksFromProcessors()
#        
#        self.__resetTimer()
#        
#        tCeil = float("inf")
#        candidates = []
#        stop = False
#        z = 0
#        while not stop:
#            while z < self._m and not stop:
#                self.__logger.warn("z=%d seenNodesTotal=%d cutNodesTotal=%d" \
#                    % (z, self._seenNodesTotalCount, self._cutNodesTotalCount))
#                branches = [] #Элементы имеют вид: (расписание, оценка_снизу)
#                minIndex = None #Индекс ветви с наименьшей оценкой
#                for j in range(self._n):
#                    sch = copy.deepcopy(schedule)
#                    sch.rebindTaskWithUndo(sch.task(z), None, sch.processor(j).id())
#                    lowerBound = self._calcBranchLowerBound(sch) \
#                        if z < self._m - 1 \
#                        else sch.maxProcLoad()
#                    if minIndex is None or lowerBound < branches[minIndex][1]:
#                        minIndex = j
#                    branches.append((sch, lowerBound))
#                
#                if branches[minIndex][1] < tCeil:
#                    self.__logger.info("Task %s added to %s" \
#                        % (schedule.task(z).shortName(), \
#                           schedule.processor(minIndex).shortName()))
#                    schedule = branches[minIndex][0]
#                    z += 1
#                    self._seenNodesCount[z] += 1
#                    self._seenNodesTotalCount += 1
#                    self._seenNodesCount[z + 1] = 0
#                    
#                else:
#                    z -= 1
#                    if z == 0:
#                        stop = True
#                        self.__logger.info("exit 1")
#                    else:
#                        self.__logger.info("Task t_%d removed from p_%d" \
#                            % (schedule.getChangeInfo().taskId, \
#                               schedule.getChangeInfo().procToId))
#                        self._lowerBoundsCache[schedule.toStrId()] = float("inf")
#                        schedule.undoChange()
#                    
#                    notSeenNodesYet = 0
#                    for j in range(len(branches)):
#                        notSeenNodesYet += self.__subTreeNodesCount(z + 1) \
#                        if self._calcBranchLowerBound(branches[j][0]) < float("inf") else 0
#                    self._seenNodesCount[z] += self._seenNodesCount[z + 1]
#                    self._cutNodesTotalCount = self.__subTreeNodesCount(z) \
#                        - self._seenNodesCount[z] - notSeenNodesYet
#                    self.__logger.info("1: Seen %d nodes of %d. Not seen yet %d" \
#                        % (self._seenNodesCount[z], \
#                           self.__subTreeNodesCount(z), \
#                           notSeenNodesYet))
#                    
#                self.__updateTimer()
#            
#            if stop:
#                break
#            
#            if schedule.bindedTaskCount() == schedule.taskCount():
#                assert(tCeil >= schedule.maxProcLoad())
#                tCeil = schedule.maxProcLoad()
#                candidates.append(copy.deepcopy(schedule))
#                self.emit(QtCore.SIGNAL("candidateFound"), candidates[-1])
#                self.__logger.warn("Candidate found " + candidates[-1].toStrId() +\
#                                    " load " + str(candidates[-1].maxProcLoad()))
#            
#            if tCeil == self._tFloor:                
#                stop = True
#                self.__logger.info("exit 2")
#            else:
#                z -= 1
#                if z == 0:
#                    stop = True
#                    self.__logger.info("exit 3")
#                else:
#                    #Обратный ход
#                    self._lowerBoundsCache[schedule.toStrId()] = float("inf")
#                    changeInfo = schedule.getChangeInfo()
#                    self.__logger.info("Task t_%d removed from p_%d" \
#                                       % (changeInfo.taskId, changeInfo.procToId))
#                    schedule.undoChange()
#                
#                self._seenNodesCount[z] += self._seenNodesCount[z + 1]
#                self._cutNodesTotalCount = self.__subTreeNodesCount(z) - self._seenNodesCount[z]
#                self.__logger.info("2: Seen %d nodes of %d" %\
#                                   (self._seenNodesCount[z], self.__subTreeNodesCount(z)))
#        
#        minIndex = -1
#        minProcLoad = None
#        for i in range(len(candidates)):
#            if minProcLoad is None \
#            or candidates[i].maxProcLoad() < minProcLoad:
#                minIndex = i
#                minProcLoad = candidates[i].maxProcLoad()
#            self.__logger.info("Candidate " + candidates[i].toStrId() + " load " + str(candidates[i].maxProcLoad())) 
#                
#        assert(minIndex >= 0)
#        self._result = candidates[minIndex]
#
#        self.__logger.info("Seen Nodes Count is %d" % self._seenNodesCount[0])
#        self.__logger.info("Seen Nodes Total Count is %d" % self._seenNodesTotalCount)
#        self.__logger.info("FINISH")
#        self.emit(QtCore.SIGNAL("finished"), self)
#        
#    def result(self):
#        return self._result
#                
           
        
        
        
        
        
        
        
        
        