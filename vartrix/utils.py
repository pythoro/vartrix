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
        
    Note:
        The class name pointed to by the dotkey must exist in the module,
        or a KeyError will be raised.
    '''
    
    def __init__(self, name, container, dotkey):
        self.container = container
        self.name = name
        self.dotkey = dotkey
    
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
        return c()