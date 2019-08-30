# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 19:52:22 2019

@author: Reuben
"""

import weakref
from collections import defaultdict

def is_root(dotkey):
    return dotkey in [None, '__ROOT__', '', '.']

def safe_root(dotkey):
    if is_root(dotkey):
        return '__ROOT__'
    else:
        return dotkey
    

class Flat(dict):
    ''' An dictionary with some extra methods'''

    def __init__(self, dct=None):
        self._observers = defaultdict(weakref.WeakSet)
        if dct is not None:
            self.load(dct)

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
        self._observers[safe_root(dotkey)].add(view)

    def get_dct(self, dotkey):
        if is_root(dotkey):
            return self.copy()
        out = {}
        for key, val in self.items():
            root, k = self._split_dotkey(key)
            if root == dotkey:
                out[k] = val
        return out

    def update_observers(self, dotkey, val):
        root, key = self._split_dotkey(dotkey)
        for view in self._observers[root]:
            view._view_update(key, val)

    def __setitem__(self, key, val):
        return self.set(key, val)
    
    def _split_dotkey(self, dotkey):
        split = dotkey.split('.')
        k = split.pop()
        root = safe_root('.'.join(split))
        return root, k

    def _nest(self, key_list, val, dct=None):
        dct = {} if dct is None else dct
        if len(key_list) == 1:
            dct[key_list[0]] = val
        else:
            if key_list[0] not in dct:
                dct[key_list[0]] = {}
            self._nest(key_list[1:], val, dct[key_list[0]])
        return dct
    
    def nested(self):
        dct = {}
        for dotkey, val in self.items():
            key_list = dotkey.split('.')
            self._nest(key_list, val, dct)
        return dct
    
    def load(self, dct):
        self.clear()
        self.update(dct)
        for dotkey, observers in self._observers.items():
            for observer in observers:
                observer.refresh(dotkey)
                
                
    @classmethod
    def combine(cls, dct):
        ''' Combine a dictionary of containers '''
        c = cls()
        for key, flat in dct.items():
            for k, v in flat.items():
                dotkey = key + '.' + k
                c[dotkey] = v
        return c
    
    @classmethod
    def merge(cls, flats):
        ''' Combine a dictionary of containers '''
        c = cls()
        for flat in flats:
            c.update(flat)
            for dotkey, observers in flat._observers.items():
                c._observers[dotkey] |= observers # set union, in place
        return c