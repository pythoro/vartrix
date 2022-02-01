# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 19:52:22 2019

@author: Reuben

This module includes the Container class upon which all of vartrix is built.

The idea of a container is to contain all of the key-value pairs for some
set of variables or parameters. Keys have an implied heirarchy using a
dot-format. For example, 'A.b' means that 'b' is a subkey of 'A'. All keys
are stored in a simple flat dictionary format, but some extra methods
allow the heirarchy to be used to simplify usage.

"""

import weakref
from collections import defaultdict
from contextlib import contextmanager

from . import utils

def is_root(dotkey):
    ''' Check if a dotkey is the root (container level) '''
    return dotkey in [None, '__ROOT__', '', '.']

def safe_root(dotkey):
    ''' Ensure root dotkeys are consistent '''
    if is_root(dotkey):
        return '__ROOT__'
    else:
        return dotkey


class Container(dict):
    ''' A dictionary-like class that updates observers 
    
    Args:
        dct (dict): A dictionary (possibly nested) of key-value pairs to use.
        name (str): The name of the container.
        
    Note:
        A `dotkey` is a dictionary key in the Container. It's called a dotkey
        simply because it's designed to have dots in it to represent a
        heirarchy.
    '''

    def __init__(self, dct=None, name=None):
        self.name = name
        self._backup = {}
        if dct is not None:
            self.load(dct)

    def get(self, dotkey, dct=None):
        ''' Return the value of a dotkey '''
        split = dotkey.split('.', 1)
        dct = self if dct is None else dct
        if len(split) == 1:
            return dct[split]
        return self.get(split[1], dct[split[0]])

    def lget(self, key_list):
        ''' Return the value of a dotkey specified by a list of strings
        
        Args:
            key_list (list([str])): The strings that define the dotkey. For
            example, `['a', 'b']` would equate to the dotkey `'a.b'`.
        '''
        return self['.'.join(key_list)]

    def dget(self, dotkeys):
        ''' Return a dictionary of dotkey-values for multiple dotkeys 
        
        Args:
            dotkeys (list[(str)]): A list of dotkey strings.
        '''
        dct = {}
        for dotkey in dotkeys:
            dct[dotkey] = self[dotkey]
        return dct
            
    def set(self, dotkey, val, safe=False, dct=None):
        ''' Set the value of a dotkey 
        
        Args:
            dotkey (str): The key value
            val: The value to set. It can be a numpy array.
            safe (bool): Optional boolean. If true, the dotkey must already
            exist in the Container instance.
        '''
        split = dotkey.split('.', 1)
        dct = self if dct is None else dct
        if len(split) == 1:
            if safe and split[0] not in dct:
                raise KeyError('In safe mode, key ' + dotkey + ' must be present.')
            v = utils.denumpify(val)
            dct[split] = v  # Set the value
        else:
            if split[0] not in dct:
                d = self.set(split[1], v, safe=safe, dct={})
                dct[split[0]] = d
            else:
                self.set(split[1], v, safe=safe, dct=dct[split[0]])
    
    def lset(self, key_list, val, safe=False):
        ''' Set the value of a dotkey specified as a list 
        
        Args:
            dotkey (list([str])): The list of strings for the dotkey.
            val: The value to set. It can be a numpy array.
            safe (bool): Optional boolean. If true, the dotkey must already
            exist in the Container instance.
        '''
        self.set('.'.join(key_list), val)

    def dset(self, dct, safe=False):
        ''' Set multiple values specified in a dictionary
        
        Args:
            dct (dict): The dictionary of dotkey-value pairs.
            safe (bool): Optional boolean. If true, the dotkey must already
            exist in the Container instance.
        '''
        for dotkey, val in dct.items():
            self.set(dotkey, val, safe=safe)

    def __contains__(self, dotkey):
        try:
            self.get(dotkey)
            return True
        except KeyError:
            return False

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, val):
        return self.set(key, val)
    
    def flat(self):
        ''' Create a nested dictionary representation of the container '''
        return utils.flat(self)
    
    def load(self, dct):
        ''' Set the container data using a dictionary '''
        self.clear()
        self._backup.clear()
        self.add(dct)
        
    def reset(self):
        self.load(self._backup.copy())

    def add_flat(self, dct):
        ''' Add another set of data to the container '''
        flat = utils.nested(dct)
        self.update(dct)
        self._backup.update(dct)
        
    def add(self, dct):
        ''' Add another set of data to the container '''
        self.update(dct)
        self._backup.update(dct)
                
    @classmethod
    def combine(cls, dct):
        ''' Combine a dictionary of containers '''
        c = cls()
        for key, container in dct.items():
            c[key] = v
        return c
    
    @classmethod
    def merge(cls, containers):
        ''' Combine a dictionary of containers '''
        c = cls()
        for container in containers:
            c.update(container)
        return c
    
    @contextmanager
    def context(self, dct, safe=True):
        ''' A context manager for temporary changes in values 
        
        Args:
            dct (dict): A dictionary of dotkey-value pairs.
        '''
        originals = {k: self[k] for k in dct.keys()}
        self.dset(dct, safe=safe)
        yield self
        self.dset(originals, safe=safe)
    
    def copy(self):
        return Container(dct=self, name=self.name)
    
    def to_dict(self):
        return dict(self)