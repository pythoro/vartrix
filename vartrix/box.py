# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 15:04:56 2019

@author: Reuben
"""

class Box():
    def __init__(self, container, dotkeys):
        self.dotkeys = dotkeys
        self.container = container
        # could cache on creation - then make clearing the cache optional to store values.
        # Cache couldn't be cleared, but that's OK.
    
    def _clash_error(self, key, dotkey):
        raise KeyError('Key "' + str(key) + '" defined in '
                       + dotkey + ' when already present in '
                       + 'one of: "' + '"; "'.join(self.dotkeys) + '"')

    def _key_error(self, key):
        raise KeyError('Key "' + str(key) + '" not found in any of: "' +
                       '"; "'.join(self.dotkeys) + '"')
    
    def add_dotkey(self, dotkey):
        self.dotkeys.append(dotkey)
    
    # use lru_cache for performance
    def get(self, key):
        only_dct = None
        for dotkey in self.dotkeys:
            dct = self.container.get(dotkey)
            if key in dct:
                if only_dct is not None:
                    self._clash_error(key, dotkey)
                only_dct = dct
        if only_dct is not None:
            return only_dct[key]
        else:
            self._key_error(key)
        
    def set(self, key, val):
        only_dct = None
        for dotkey in self.dotkeys:
            dct = self.container.get(dotkey)
            if key in dct:
                if only_dct is not None:
                    self._clash_error(key, dotkey)
                only_dct = dct
        if only_dct is not None:
            only_dct[key] = val
            # clear cache
        else:
            self._key_error(key)
    
    # use lru_cache
    def __getitem__(self, key):
        return self.get(key)
    
    def __setitem__(self, key, val):
        self.set(key, val)
    
    def combine(self):
        ''' Combines keys and checks for errors '''
        d = {}
        for dotkey in self.dotkeys:
            dct = self.container.get(dotkey)
            for key in dct.keys():
                if key in d:
                    self._clash_error(key, dotkey)
            d.update(dct)
        return d
        
    def __str__(self):
        return str(self.combine())
            
    def __repr__(self):
        return str(self)
            
    def copy(self):
        return self.combine() # maybe different method to clone?