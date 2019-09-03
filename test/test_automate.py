# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 08:47:20 2019

@author: Reuben
"""

import unittest

import ruamel.yaml as yml

from vartrix.flat import Flat
from vartrix import automate

base = {'alias.one': 5,
        'alias.two': 7,
        'alias.three': 11,
        'alias.four': 17}

def get_f():
    f = Flat(base)
    return f

class Test_Automator(unittest.TestCase):
    pass



class Test_Aliases(unittest.TestCase):
    pass


class Test_Vector(unittest.TestCase):
    def get_vec_1(self):
        d = {'labels': ['a', 'b'],
             'alias_1': [1, 2],
             'alias_2': [3, 4]}
        return automate.Vector(d, 'vec_1')
    
    def test_init_labelled(self):
        v = self.get_vec_1()
        self.assertDictEqual(v.data, {'alias_1': [1, 2], 'alias_2': [3, 4]})
        self.assertListEqual(v.labels, ['a', 'b'])
        
    def test_get_lst_labelled(self):
        v = self.get_vec_1()
        lst = v.get_lst()
        self.assertListEqual(lst, [{'alias_1': 1, 'alias_2': 3},
                                   {'alias_1': 2, 'alias_2': 4}])

    def test_get_label_lst_labelled(self):
        v = self.get_vec_1()
        lst = v.get_label_lst()
        self.assertListEqual(lst, [{'vec_1': 'a'},
                                   {'vec_1': 'b'}])

    def get_vec_unlabelled(self):
        d = {'alias_1': [1, 2],
             'alias_2': [3, 4]}
        return automate.Vector(d, 'vec_unlabelled')
    
    def test_init_unlabelled(self):
        v = self.get_vec_unlabelled()
        self.assertDictEqual(v.data, {'alias_1': [1, 2], 'alias_2': [3, 4]})
        self.assertListEqual(v.labels, [0, 1])
        
    def test_get_lst_unlabelled(self):
        v = self.get_vec_unlabelled()
        lst = v.get_lst()
        self.assertListEqual(lst, [{'alias_1': 1, 'alias_2': 3},
                                   {'alias_1': 2, 'alias_2': 4}])

    def test_get_label_lst_unlabelled(self):
        v = self.get_vec_unlabelled()
        lst = v.get_label_lst()
        self.assertListEqual(lst, [{'vec_unlabelled': 0},
                                   {'vec_unlabelled': 1}])


    def get_vec_2(self):
        d = {'labels': ['c', 'd'],
             'alias_3': [5, 6],
             'alias_4': [7, 8]}
        return automate.Vector(d, 'vec_2')
    
    def test_get_lst_nested(self):
        v = self.get_vec_1()
        v2 = self.get_vec_2()
        v.set_child(v2)
        lst = v.get_lst()
        self.assertListEqual(lst, [{'alias_1': 1, 'alias_2': 3, 'alias_3': 5, 'alias_4': 7},
                                   {'alias_1': 1, 'alias_2': 3, 'alias_3': 6, 'alias_4': 8},
                                   {'alias_1': 2, 'alias_2': 4, 'alias_3': 5, 'alias_4': 7},
                                   {'alias_1': 2, 'alias_2': 4, 'alias_3': 6, 'alias_4': 8}])

    def test_get_label_lst_nested(self):
        v = self.get_vec_1()
        v2 = self.get_vec_2()
        v.set_child(v2)
        lst = v.get_label_lst()
        self.assertListEqual(lst, [{'vec_1': 'a', 'vec_2': 'c'},
                                   {'vec_1': 'a', 'vec_2': 'd'},
                                   {'vec_1': 'b', 'vec_2': 'c'},
                                   {'vec_1': 'b', 'vec_2': 'd'}])

    
class Test_Vectors(unittest.TestCase):
    def make_vectors(self):
        d = {'vec_1': {'labels': ['a', 'b'],
                       'alias_1': [1, 2],
                       'alias_2': [3, 4]},
             'vec_2': {'labels': ['c', 'd'],
                       'alias_3': [5, 6],
                       'alias_4': [7, 8]}}
        v = automate.Vectors(d)    
        return v
    
    def test_loop(self):
        v = self.make_vectors()
        val_lst, label_lst = v.loop(['vec_1', 'vec_2'])
        self.assertListEqual(val_lst, [{'alias_1': 1, 'alias_2': 3, 'alias_3': 5, 'alias_4': 7},
                                       {'alias_1': 1, 'alias_2': 3, 'alias_3': 6, 'alias_4': 8},
                                       {'alias_1': 2, 'alias_2': 4, 'alias_3': 5, 'alias_4': 7},
                                       {'alias_1': 2, 'alias_2': 4, 'alias_3': 6, 'alias_4': 8}])
        self.assertListEqual(label_lst, [{'vec_1': 'a', 'vec_2': 'c'},
                                         {'vec_1': 'a', 'vec_2': 'd'},
                                         {'vec_1': 'b', 'vec_2': 'c'},
                                         {'vec_1': 'b', 'vec_2': 'd'}])


class Test_Sequencer(unittest.TestCase):
    pass