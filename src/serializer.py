# -*- coding: utf-8 -*-
'''
Created on 12.09.2011

@author: vlkv
'''
import errors
import sys
import json

class Serializable(object):
    def toJson(self):
        raise errors.PureVirtualCallError()

class CustomEncoder(json.JSONEncoder):
    
    def default(self, obj):
        if isinstance(obj, Serializable):
            return obj.toJson()
        else:
            return json.JSONEncoder.default(self, obj)
    
def CustomDecoder():
    return json.JSONDecoder(object_hook=hook)
        
def hook(objState):
    if "__class__" in objState and "__module__" in objState:
        __import__(objState["__module__"])
        cls = getattr(sys.modules[objState["__module__"]], objState["__class__"])
        return cls.fromJson(objState)
    else:
        return objState

