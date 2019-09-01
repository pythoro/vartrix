# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 22:12:43 2019

@author: Reuben
"""

from .container import Container
import ruamel.yaml as yml

class Automator():
    def __init__(self, flat, fname):
        self.flat = flat
        with open(fname) as f:
            self.sets = yml.safe_load(f)
        
    def run(self, set_name, automated_cls):
        set_data = self.sets[set_name]
        looper = Looper(set_data, automated_cls)
        



class Looper():
    def __init__(self, set_data, automated_cls):
        self.automated_cls = automated_cls
        sequences = Sequences(set_data)
    
    
    
class Aliases():
    def __init__(self, data):
        self.data = data
        
    def translate(self, dct):
        out = {}
        for k, v in dct.items():
            if k in self.data:
                out[self.data[k]] = v
            else:
                out[k] = v
        return out
        
    
class Vector():
    def __init__(self, data, name):
        self.name =  name
        self.i = 0
        self.child = None
        self.setup(data)
        
    def setup(self, data):
        dct = data.copy()
        if 'labels' in dct:
            self.labels = dct['labels']
            del dct['labels']
        else:
            key_list = list(data.keys())
            self.labels = data[key_list[0]]
        self.data = dct
        self.n = len(self.labels)
        
    def set_child(self, vector):
        self.child = vector
        
    def get_lst(self, lst=None, d=None):
        lst = [] if lst is None else lst
        d = {} if d is None else d
        for i in range(self.n):
            for k, vec in self.data.items():
                d[k] = vec[i]
            if self.child is not None:
                self.child.get_lst(lst, d)
            else:
                lst.append(d.copy())
        return lst
    
    def get_label_lst(self, lst=None, d=None):
        lst = [] if lst is None else lst
        d = {} if d is None else d
        for label in self.labels:
            d[self.name] = label
            if self.child is not None:
                self.child.get_label_lst(lst, d)
            else:
                lst.append(d.copy())
        return lst

        
class Vectors():
    def __init__(self, data):
        self.data = data
    
    def loop(self, v_names):
        root = None
        vectors = {k: Vector(v, k) for k, v in self.data.items()}
        for v_name in v_names:
            if root is None:
                root = vectors[v_name]
                current = vectors[v_name]
            else:
                current.set_child(vectors[v_name])
                current = vectors[v_name]
        return root.get_lst(), root.get_label_lst()
        
        
class Sequences():
    def __init__(self, data):
        self.sequences = data['sequences']
        self.aliases = Aliases(data['aliases'])
        self.vectors = Vectors(data['vectors'])
        
    def sequence(self, name):
        dct = {}
        s = self.sequences[name]
        for method, v_names in s.items():
            lst, labels = self.vectors.loop(v_names)
            lst = [self.aliases.translate(d) for d in lst]
            dct[method] = {'lst': lst, 'labels': labels}
        return dct
        