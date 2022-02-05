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

from contextlib import contextmanager

from . import utils


class Container(dict):
    ''' A dictionary-like class that updates observers 
    
    Args:
        dct (dict): A dictionary (possibly nested) of key-value pairs to use.
        
    Note:
        A `dotkey` is a dictionary key in the Container. It's called a dotkey
        simply because it's designed to have dots in it to represent a
        heirarchy.
    '''

    def __init__(self, dct=None):
        self._backup = {}
        if dct is not None:
            self.load(dct)
            
    def set(self, key, val, safe=False):
        ''' Set the value of a key
        
        Args:
            key (str): The key value
            val: The value to set. It can be a numpy array.
            safe (bool): Optional boolean. If true, the dotkey must already
            exist in the Container instance.
        '''
        if safe:
            if key not in self:
                raise KeyError('In safe mode, key ' 
                               + key + ' must be present.')
        v = utils.denumpify(val)
        dct[key] = v  # Set the value
    
    def dset(self, dct, safe=False):
        ''' Set multiple values specified in a dictionary
        
        Args:
            dct (dict): The dictionary of dotkey-value pairs.
            safe (bool): Optional boolean. If true, the dotkey must already
            exist in the Container instance.
        '''
        for key, val in dct.items():
            self.set(key, val, safe=safe)

    def load(self, dct):
        ''' Set the container data using a dictionary '''
        self.clear()
        self._backup.clear()
        self.add(dct)
        
    def reset(self):
        self.load(self._backup.copy())

    def add(self, dct):
        ''' Add another set of data to the container '''
        self.update(dct)
        self._backup.update(dct)
                
    @classmethod
    def merge(cls, containers):
        ''' Combine a list of containers '''
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
        return Container(dct=self)
    
    def to_dict(self):
        return dict(self)