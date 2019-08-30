# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 19:31:41 2019

@author: Reuben
"""


import unittest

from vartrix.flat import Flat

def get_f():
    f = Flat()
    f.set('a.b', 5)
    f.set('b.c', 7)
    return f

class Test_Flat(unittest.TestCase):
    def test_nest(self):
        f = Flat()
        ret = f._nest(['a', 'b', 'c', 'd'], 5)
        expected = {'a': {'b': {'c': {'d': 5}}}}
        self.assertDictEqual(ret, expected)
        
    def test_nested(self):
        f = get_f()
        ret = f.nested()
        expected = {'a': {'b': 5},
                    'b': {'c': 7}}
        self.assertDictEqual(ret, expected)