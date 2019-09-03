# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 22:12:43 2019

@author: Reuben
"""

import ruamel.yaml as yml


class Automator():
    def __init__(self, flat, fname):
        self.flat = flat
        with open(fname) as f:
            self.sets = yml.safe_load(f)
        
    def run(self, set_name, automated_cls):
        set_data = self.sets[set_name]
        s = Sequencer(set_data[set_name])
        obj = automated_cls(set_name=set_name)
        obj.prepare()
        for name in s.sequence_names:
            self.execute_sequence(s, name, obj)
        obj.finish()

    def execute_sequence(self, s, name, obj):
        obj.prepare_sequence(name)
        seq_dct = s.sequence(name)
        flat = self.flat
        for method_name, (val_list, label_lst) in seq_dct.items():
            obj.prepare_method(method_name)
            method = getattr(obj, method_name)
            with flat.context(val_list[0]):
                for val_dct, label_dct in zip(val_list, label_lst):
                    flat.dset(val_dct)
                    method(val_dct, label_dct)
            obj.finish_method(method_name)
        obj.finish_sequence(name)
        
    
class Aliases(dict):
       
    def translate(self, dct):
        out = {}
        for k, v in dct.items():
            if k in self:
                out[self[k]] = v
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
        def default_labels(d):
            for v in dct.values():
                n = len(v)
                return [i for i in range(n)]
        dct = data.copy()
        self.labels = dct.pop('labels', default_labels(dct))
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
        
        
class Sequencer():
    def __init__(self, data):
        self.sequences = data['sequences']
        self.aliases = Aliases(data['aliases'])
        self.vectors = Vectors(data['vectors'])
        
    def sequence(self, name):
        seq_dct = {}
        s = self.sequences[name]
        for method_name, v_names in s.items():
            val_list, label_lst = self.vectors.loop(v_names)
            val_list = [self.aliases.translate(d) for d in val_list]
            seq_dct[method_name] = {'val_list': val_list,
                                    'label_lst': label_lst}
        return seq_dct
    
    @property
    def sequence_names(self):
        return list(self.sequences.keys())
        
