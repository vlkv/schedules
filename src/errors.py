# -*- coding: utf-8 -*-
'''
Created on 03.09.2011

@author: vlkv
'''

class MessageError(Exception):
    '''
    Исключение для тех случаев, когда ошибок нет, но нужно отобразить
    пользователю какую-нибудь информацию.
    '''
    def __init__(self, msg=None):
        super(MessageError, self).__init__(msg)


class BaseException(Exception):
    '''
    Базовый класс для всех (почти) моих исключений.
    '''
    def __init__(self, msg=None, cause=None):
        '''
        msg - сообщение о том, что случилось
        cause - исключение, которое явилось причиной данного исключения.
        '''
        super(BaseException, self).__init__(msg)
        self.cause = cause

    
class IndexOutOfRangeError(BaseException):
    def __init__(self, msg=None, cause=None):
        super(IndexOutOfRangeError, self).__init__(msg, cause)
        
class IdNotFoundError(BaseException):
    def __init__(self, msg=None, cause=None):
        super(IdNotFoundError, self).__init__(msg, cause)
        
class CantBeNoneError(BaseException):
    def __init__(self, msg=None, cause=None):
        super(CantBeNoneError, self).__init__(msg, cause)
        
class ItemPresentsError(BaseException):
    def __init__(self, msg=None, cause=None):
        super(ItemPresentsError, self).__init__(msg, cause)
        
class ItemNotFoundError(BaseException):
    def __init__(self, msg=None, cause=None):
        super(ItemNotFoundError, self).__init__(msg, cause)
        
class PureVirtualCallError(BaseException):
    def __init__(self, msg=None, cause=None):
        super(PureVirtualCallError, self).__init__(msg, cause)
        
class CannotBindTaskTwiceError(BaseException):
    def __init__(self, msg=None, cause=None):
        super(PureVirtualCallError, self).__init__(msg, cause)
        
class NotEnoughArgumentsError(BaseException):
    def __init__(self, msg=None, cause=None):
        super(NotEnoughArgumentsError, self).__init__(msg, cause)
        
class ArgumentValueError(BaseException):
    def __init__(self, msg=None, cause=None):
        super(ArgumentValueError, self).__init__(msg, cause)
        
class ArgumentTypeError(BaseException):
    def __init__(self, msg=None, cause=None):
        super(ArgumentTypeError, self).__init__(msg, cause)

if __name__ == '__main__':
    raise IndexOutOfRangeError('asdf')

