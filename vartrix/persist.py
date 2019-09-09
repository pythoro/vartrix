# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 17:05:43 2019

@author: Reuben
"""

import ruamel.yaml as yml

class Manager():
    def __init__(self):
        self.handlers = {'yaml': Yaml()}
        
    def add_handler(self, key, handler):
        self.handlers[key] = handler
        
    def load(self, source, *args, handler=None, **kwargs):
        if handler is not None:
            return self.handlers[handler].load(source, *args, **kwargs)
        for k, handler in self.handlers.items():
            if handler.suitable(source, *args, **kwargs):
                return handler.load(source, *args, **kwargs)

    def save(self, dct, target, *args, handler=None, **kwargs):
        if handler is not None:
            return self.handlers[handler].save(target, *args, **kwargs)
        for k, handler in self.handlers.items():
            if handler.suitable(target, *args, **kwargs):
                return handler.save(target, *args, **kwargs)


class Yaml():
    def suitable(self, fname, *args, **kwargs):
        test_1 = fname.endswith('.yml')
        test_2 = fname.endswith('.yaml')
        return test_1 or test_2
        
    def load(self, fname):
        with open(fname) as f:
            dct = yml.safe_load(f)
        return dct
    
    def save(self, dct, fname):
        with open(fname) as f:
            yml.safe_write(dct, f)
            
            
manager = Manager()
load = manager.load
save = manager.save
