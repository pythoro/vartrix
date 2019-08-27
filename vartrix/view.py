# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 20:59:39 2019

@author: Reuben
"""

class View():
    ''' Provides a virtual view of a Flat dictionary '''
    def __init__(self, flat, dotkeys=None):
        self._flat = flat
        self._overrides = {}
        self.dotkeys = []
        if dotkeys is not None:
            for dotkey in dotkeys:
                self.add_dotkey(dotkey)
        
    def add_dotkey(self, dotkey):
        self.dotkeys.append(dotkey)
       
    def get(self, key):
        if key in self._overrides: # it's overridden
            return self._overrides[key]
        flat = self._flat
        for dotkey in self.dotkeys:
            k = dotkey + '.' + key
            if k in flat:
                return flat[k]
        raise KeyError(key + ' not found in dotkeys: ' + '; '.join(self.dotkeys))
        
    def set(self, key, val, live=True):
        if not live:
            self._overrides[key] = val
        flat = self._flat
        for dotkey in self.dotkeys:
            k = dotkey + '.' + key
            if k in flat:
                flat[k] = val
                return
        raise KeyError(key + ' not found in dotkeys: ' + '; '.join(self.dotkeys))
        
    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, val):
        return self.set(key, val, live=False)
    