# -*- coding: utf-8 -*-
"""
Created on Sat Sep 14 11:36:50 2019

@author: Reuben
"""

import inspect, sys


class Factory():
    def __init__(self, name, container, dotkey):
        self.container = container
        self.name = name
        self.dotkey = dotkey
    
    def new(self):
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