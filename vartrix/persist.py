# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 17:05:43 2019

@author: Reuben
"""

import ruamel.yaml as yml

class Manager():
    default_handler = 'yaml'
    
    def __init__(self):
        self.handlers = {'yaml': Yaml()}
        self.specified = None
        
    def add_handler(self, key, handler):
        self.handlers[key] = handler
        
    def specify(self, key):
        self.specified = key
        
    def load(self, source, handler=None, **kwargs):
        if handler is not None:
            return self.handlers[handler].load(source, **kwargs)
        if self.specified is not None:
            return self.handlers[self.specified].load(source, **kwargs)
        for k, handler in self.handlers.items():
            if handler.suitable(source, **kwargs):
                return handler.load(source, **kwargs)
        f = source + '.yaml'
        return self.handlers[self.default_handler].load(f, **kwargs)

    def save(self, dct, target, handler=None, **kwargs):
        if handler is not None:
            return self.handlers[handler].save(target, **kwargs)
        if self.specified is not None:
            return self.handlers[self.specified].save(dct, target, **kwargs)
        for k, handler in self.handlers.items():
            if handler.suitable(target, **kwargs):
                return handler.save(dct, target, **kwargs)
        f = target + '.yaml'
        return self.handlers[self.default_handler].save(dct, f, **kwargs)
        

class Yaml():
    def suitable(self, fname, **kwargs):
        test_1 = fname.endswith('.yml')
        test_2 = fname.endswith('.yaml')
        return test_1 or test_2
        
    def load(self, fname, **kwargs):
        with open(fname, mode='r') as f:
            dct = yml.safe_load(f)
        return dct
    
    def save(self, dct, fname, **kwargs):
        with open(fname, mode='w') as f:
            y = yml.YAML()
            y.dump(dict(dct), f)
            
            
manager = Manager()
load = manager.load
save = manager.save
