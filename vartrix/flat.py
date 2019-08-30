# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 19:52:22 2019

@author: Reuben
"""

import weakref
from collections import defaultdict

class Flat(dict):
    ''' An dictionary with some extra methods'''

    def __init__(self):
        self._observers = defaultdict(weakref.WeakSet)

    def get(self, dotkey):
        return self[dotkey]

    def lget(self, key_list):
        return self['.'.join(key_list)]

    def dget(self, dotkeys):
        dct = {}
        for dotkey in dotkeys:
            dct[dotkey] = self[dotkey]
        return dct
            
    def set(self, dotkey, val, safe=False):
        if safe and dotkey not in self:
            raise KeyError('In safe mode, key ' + dotkey + ' must be present.')
        super().__setitem__(dotkey, val)
        self.update_observers(dotkey, val)
        
    def lset(self, key_list, val, safe=False):
        self.set('.'.join(key_list), val)

    def dset(self, dct, safe=False):
        ''' Pull in values from a flat dct '''
        for dotkey, val in dct.items():
            self.set(dotkey, val, safe=safe)

    def register_observer(self, dotkey, view):
        self._observers[dotkey].add(view)

    def get_dct(self, dotkey):
        out = {}
        for key, val in self.items():
            split = key.split('.')
            k = split.pop()
            root = '.'.join(split)
            root = '__ROOT__' if root == '' else root
            if root == dotkey:
                out[k] = val
        return out

    def update_observers(self, dotkey, val):
        split = dotkey.split('.')
        key = split.pop()
        root = '.'.join(split)
        root = '__ROOT__' if root == '' else root
        for view in self._observers[root]:
            view._view_update(key, val)

    def __setitem__(self, key, val):
        return self.set(key, val)