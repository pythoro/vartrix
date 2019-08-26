# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 15:04:56 2019

@author: Reuben
"""

import uuid

from .container import Container

class Box(dict):
    def __init__(self, container, dotkeys, keep_live=True):
        self.__hash = hash(uuid.uuid4())
        self.dotkeys = []
        self.container = container
        self.keep_live = keep_live
        if dotkeys is None:
            self._hook_to_container(container, None)
        else:
            for dotkey in dotkeys:
                self.add_dotkey(dotkey)
        # could cache on creation - then make clearing the cache optional to store values.
        # Cache couldn't be cleared, but that's OK.
    
    def __hash__(self):
        return self.__hash
    
    def _clash_error(self, key, dotkey):
        raise KeyError('Key "' + str(key) + '" defined in '
                       + dotkey + ' when already present in '
                       + 'one of: "' + '"; "'.join(self.dotkeys) + '"')

    def _key_error(self, key):
        raise KeyError('Key "' + str(key) + '" must exist in one of these ' +
                       'dotkeys: "' +
                       '"; "'.join(self.dotkeys) + '"')
    
    def add_dotkey(self, dotkey):
        container = self.container.get(dotkey)
        if not isinstance(container, Container):
            raise KeyError('Key "' + str(dotkey) + '" is not a Container')
        self._hook_to_container(container, dotkey)
    
    def _hook_to_container(self, container, dotkey):
        container.register_observer(self)
        for key in container.keys():
            if key in self:
                self._clash_error(key, dotkey)
        self.update(container)
        self.dotkeys.append(dotkey)
           
    def box_update(self, key, val):
        if self.keep_live:
            super().__setitem__(key, val)
    
    def set(self, key, val):
        container = None
        for dotkey in self.dotkeys:
            c = self.container.get(dotkey)
            if key in c:
                if container is not None:
                    self._clash_error(key, dotkey)
                container = c
        if container is not None:
            container.set(key, val)
        else:
            self._key_error(key)
    
    def __setitem__(self, key, val):
        self.set(key, val)
        
