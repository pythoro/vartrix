# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 11:14:59 2019

@author: Reuben
"""

from .flat import Flat
from .container import Container

class Name_Space(dict):
    def __init__(self, obj_cls=Flat):
        self.obj_cls = obj_cls
    
    def __missing__(self, key):
        return self.create(key)
    
    def create(self, key, dct=None):
        new = self.obj_cls(name=key, dct=dct)
        self[key] = new
        return new
    
    def get(self, key, dct=None):
        if key not in self:
            return self.create(key, dct)
        return self[key]
