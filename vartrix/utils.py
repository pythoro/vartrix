# -*- coding: utf-8 -*-
"""
Created on Sat Sep 14 11:36:50 2019

@author: Reuben

This module contains helper classes and functions. 

"""

import inspect, sys


class Factory():
    ''' Instantiate module classes based on container key 
    
    Args:
        name (str): The module name (often `__name__`)
        container (Container): The container instance
        dotkey (str): The dotkey of the class name.
        build_function (func): OPTIONAL: A function that takes the new
        instance object. If provided, the return value of the Factory is
        the return value of the function.
        
    Note:
        The class name pointed to by the dotkey must exist in the module,
        or a KeyError will be raised.
    '''
    
    def __init__(self, name, container, dotkey, build_function=None):
        self.container = container
        self.name = name
        self.dotkey = dotkey
        self.build_function = build_function
    
    def new(self):
        ''' Create a new instance based on the current dotkey value '''
        cls_name = self.container[self.dotkey]
        clsmembers = inspect.getmembers(sys.modules[self.name],
                                        inspect.isclass)
        clsdct = {t[0]: t[1] for t in clsmembers}
        try:
            c = clsdct[cls_name]
        except KeyError:
            raise KeyError('Class ' + str(cls_name) + ' not found in module '
                           + str(self.name))
        if self.build_function is None:
            return c()
        else:
            obj = c()
            return self.build_function(obj)
        
        
def _nest(key_list, val, dct=None):
    dct = {} if dct is None else dct
    if len(key_list) == 1:
        dct[key_list[0]] = val
    else:
        if key_list[0] not in dct:
            dct[key_list[0]] = {}
        _nest(key_list[1:], val, dct[key_list[0]])
    return dct

def nested(dct):
    ''' Create a nested dictionary representation of a dotkey flat dictionary '''
    out_dct = {}
    for dotkey, val in dct.items():
        key_list = dotkey.split('.')
        _nest(key_list, val, out_dct)
    return out_dct