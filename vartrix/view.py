# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 20:59:39 2019

@author: Reuben
"""

import uuid

class View(dict):
    ''' Provides a virtual view of a Flat dictionary 
    
    Could cache as dict values and update like Box class for performance
    '''
    def __init__(self, flat, dotkeys=None, keep_live=True):
        self.__hash = hash(uuid.uuid4())
        self._flat = flat
        self.dotkeys = []
        self.keep_live = keep_live
        if dotkeys is not None:
            for dotkey in dotkeys:
                self.add_dotkey(dotkey)
        
    def __hash__(self):
        return self.__hash
        
    def add_dotkey(self, dotkey):
        if dotkey is None or dotkey in ['', '.']:
            dotkey == '__ROOT__'
        self._hook_to_flat(dotkey)
    
    def _clash_error(self, key, dotkey):
        raise KeyError('Key "' + str(key) + '" defined in '
                       + dotkey + ' when already present in '
                       + 'one of: "' + '"; "'.join(self.dotkeys) + '"')
    
    def _hook_to_flat(self, dotkey):
        flat = self._flat
        flat.register_observer(dotkey, self)
        dct = flat.get_dct(dotkey)
        for key in dct.keys():
            if key in self:
                self._clash_error(key, dotkey)
        self.update(dct)
        self.dotkeys.append(dotkey)
        
    def get(self, key):
        return self[key]
        
    def set(self, key, val):
        if not self.keep_live:
            super().__setitem__(key, val)
        flat = self._flat
        for dotkey in self.dotkeys:
            k = dotkey + '.' + key
            if k in flat:
                flat.set(k, val)
                return
        raise KeyError(key + ' not found in dotkeys: ' + '; '.join(self.dotkeys))
        
    def __setitem__(self, key, val):
        return self.set(key, val)
    
    def view_update(self, key, val):
        if self.keep_live:
            super().__setitem__(key, val)
    