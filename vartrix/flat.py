# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 19:52:22 2019

@author: Reuben
"""

class Flat(dict):
    ''' An dictionary with some extra methods'''

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
        self[dotkey] = val
        
    def lset(self, key_list, val, safe=False):
        self.set('.'.join(key_list), val)

    def dset(self, dct, safe=False):
        ''' Pull in values from a flat dct '''
        for dotkey, val in dct.items():
            self.set(dotkey, val, safe=safe)
