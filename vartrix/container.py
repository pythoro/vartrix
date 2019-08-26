# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 11:00:07 2019

@author: Reuben
"""

import uuid
import weakref

class Container(dict):
    ''' An awesome little nesting dictionary '''
    
    def __init__(self):
        self.__hash = hash(uuid.uuid4())
        self._observers = weakref.WeakSet()
    
    def __hash__(self):
        return self.__hash
    
    def __missing__(self, key):
        value = self[key] = type(self)()
        return value

    def register_observer(self, box):
        self._observers.add(box)

    def update_observers(self, key, val):
        for box in self._observers:
            box.box_update(key, val)

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
        obj = self
        for key in key_list[:-1]:
            if safe and key not in obj:
                raise KeyError('In safe mode, key "' 
                               + '.'.join(key_list) + '" must be present.')
            obj = obj[key]
        k = key_list[-1]
        if safe and k not in obj:
            raise KeyError('In safe mode, key "' 
                           + '.'.join(key_list) + '" must be present.')
        obj[key_list[-1]] = val
        obj.update_observers(key_list[-1], val)

    def dset(self, dct, safe=False):
        ''' Pull in values from a flat dct '''
        for dotkey, val in dct.items():
            self.set(dotkey, val, safe=safe)
    
    def flat(self, dct=None, parents=None):
        ''' Create a flat dictionary (recursively) '''
        dct = {} if dct is None else dct
        parents = [] if parents is None else parents
        for key, obj in self.items():
            full_key = parents + [str(key)]
            if type(obj) is type(self):
                obj.flat(dct, parents=full_key)
            else:
                dct['.'.join(full_key)] = obj
        return dct
    
    