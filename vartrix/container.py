# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 11:00:07 2019

@author: Reuben
"""

import uuid
import weakref

class Container(dict):
    ''' An awesome little nesting dictionary '''
    
    def __init__(self, dct=None, name=None):
        self.name = name
        self.__hash = hash(uuid.uuid4())
        self._observers = weakref.WeakSet()
        if dct is not None:
            self.load(dct)
    
    def __hash__(self):
        return self.__hash
    
    def __missing__(self, key):
        value = self[key] = type(self)()
        return value

    def register_observer(self, box):
        self._observers.add(box)

    def update_observers(self, key, val):
        for box in self._observers:
            box._box_update(key, val)

    def get(self, dotkey):
        # Use singledispatch instead - might be faster
        if dotkey is None:
            return self
        key_list = dotkey.split('.')
        return self.lget(key_list)

    def lget(self, key_list):
        obj = self
        for key in key_list:
            obj = obj[key]
        return obj

    def dget(self, dotkeys):
        dct = {}
        for dotkey in dotkeys:
            dct[dotkey] = self.get(dotkey)
        return dct
            
    def set(self, dotkey, val, safe=False):
        # Use singledispatch instead - might be faster
        key_list = dotkey.split('.')
        self.lset(key_list, val, safe=safe)
        
    def lset(self, key_list, val, safe=False):
        container = self
        for key in key_list[:-1]:
            if safe and key not in container:
                raise KeyError('In safe mode, key "' 
                               + '.'.join(key_list) + '" must be present.')
            container = container[key]
        k = key_list[-1]
        if safe and k not in container:
            raise KeyError('In safe mode, key "' 
                           + '.'.join(key_list) + '" must be present.')
        container[k] = val
        container.update_observers(k, val)

    def dset(self, dct, safe=False):
        ''' Pull in values from a flat dct '''
        for dotkey, val in dct.items():
            self.set(dotkey, val, safe=safe)
    
    def flat(self, dct=None, parents=None, current=None):
        ''' Create a flat dictionary (recursively) '''
        dct = self if dct is None else dct
        current = {} if current is None else current
        parents = [] if parents is None else parents
        for key, obj in dct.items():
            full_key = parents + [str(key)]
            if isinstance(obj, dict):
                self.flat(obj, parents=full_key, current=current)
            else:
                current['.'.join(full_key)] = obj
        return current
    
    def load(self, dct):
        flat = self.flat(dct)
        self.dset(flat)
        
    @classmethod
    def combine(cls, containers):
        ''' Combine a dictionary of containers '''
        c = cls()
        c.update(containers)
        return c
    
    @classmethod
    def merge(cls, containers):
        ''' Combine a dictionary of containers '''
        c = cls()
        for container in containers:
            c.update(container)
            c._observers |= container._observers # set union, in place
        return c
    