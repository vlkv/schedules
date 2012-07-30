# -*- coding: utf-8 -*-
'''
Created on 13.09.2011

@author: vlkv
'''
import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
from PyQt4.QtCore import Qt
import traceback
import json
import os
import os.path

class MyMessageBox(QtGui.QMessageBox):
    '''Окно данного класса можно растягивать мышкой, в отличие от стандартного 
    QMessageBox-а. Решение взято отсюда: 
    http://stackoverflow.com/questions/2655354/how-to-allow-resizing-of-qmessagebox-in-pyqt4
    '''
    def __init__(self, parent=None):
        super(MyMessageBox, self).__init__(parent)    
        self.setSizeGripEnabled(True)            
        #Пока что кнопок еще нет. Они добавятся конечно, когда будет вызван setText(), но пока что их нет
        self.addButton(QtGui.QMessageBox.Ok)
        self.setDefaultButton(QtGui.QMessageBox.Ok)
        self.setEscapeButton(QtGui.QMessageBox.Ok)

    def event(self, e):
        result = QtGui.QMessageBox.event(self, e)

        self.setMinimumHeight(0)
        self.setMaximumHeight(16777215)
        self.setMinimumWidth(0)
        self.setMaximumWidth(16777215)
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)

        textEdit = self.findChild(QtGui.QTextEdit)
        if textEdit != None :
            textEdit.setMinimumHeight(0)
            textEdit.setMaximumHeight(16777215)
            textEdit.setMinimumWidth(0)
            textEdit.setMaximumWidth(16777215)
            textEdit.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
            
        return result

def showExcInfo(parent, ex, tracebk=True, details=None, title=None):
    '''
    Если traceback задать равным False, то окно не содержит раздел DetailedText
    с информацией о stack trace (как это по русски сказать?).
    
    Если задать details, то данный текст выводится в разделе DetailedText, причем
    неважно чему при этом равен tracebk (он игнорируется).
    
    Параметр title позволяет задать другой заголовок окна.
    '''
    
    #if tracebk and not is_none_or_empty(details):
    #    raise ValueError(tr("details cannot be not None or empty if tracebk is True."))
    
    mb = MyMessageBox(parent)
    mb.setWindowTitle(u"Информация" if title is None else title)
    mb.setText(unicode(ex))
    if not isNoneOrEmpty(details):
        mb.setDetailedText(details)
    elif tracebk:
        mb.setDetailedText(traceback.format_exc())
    
    mb.exec_()
    
def format_exc_info(type, value, tb):    
    return ''.join(traceback.format_exception(type, value, tb))

def isNoneOrEmpty(s):
    '''Возвращает True, если строка s является None или "".
    Если передать объект класса, отличного от str, генерируется исключение TypeError.
    '''
    if s is None:
        return True
    else:
        if isinstance(s, str):    
            return True if s == "" else False
        elif isinstance(s, unicode):
            return True if s == u"" else False
        else:    
            raise TypeError(u"isNoneOrEmpty() can be applied only to str or unicode objects.")


class UserConfig(object):
    '''
    Класс для работы с конфигурационными параметрами программы.
    '''
    FILE_NAME = "schedules.conf"
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            orig = super(UserConfig, cls)
            cls._instance = orig.__new__(cls, *args, **kwargs)
            cls.__load(cls._instance)
            
        return cls._instance
    
    def __init__(self):
        pass        
    
    def get(self, key, defaultValue=None):
        try:
            return self.__config[key]
        except KeyError:
            if defaultValue is not None:
                self.set(key, defaultValue)
                return defaultValue
            else:
                return None
    
    def set(self, key, value):
        if key not in self.__config or self.__config[key] <> value:
            self.__config[key] = value
            self.__save()
        
    def __save(self):
        f = open(UserConfig.FILE_NAME, "w")
        json.dump(self.__config, f, sort_keys=True, indent=4)
        f.close()
        
    def __load(self):
        if os.path.exists(UserConfig.FILE_NAME):
            f = open(UserConfig.FILE_NAME, "r")
            self.__config = json.load(f)
            f.close()
        else:
            self.__config = dict()
    
    
    
if __name__ == '__main__':
    UserConfig().set("key", 25)
    UserConfig().set("str", "bla bla bla")
    print UserConfig().get("key")
    print UserConfig().get("str")
    

