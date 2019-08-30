# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 21:11:42 2019

@author: Reuben
"""

import unittest

from vartrix.flat import Flat
from vartrix.view import View

def get_f_mock():
    f = Flat()
    f.set('a.b', 5)
    f.set('b.c', 7)
    return f

class Test_View(unittest.TestCase):
    def test_get(self):
        f = get_f_mock()
        dotkeys = ['a']
        v = View(f, dotkeys)
        res = v['b']
        expected = 5
        self.assertEqual(res, expected)
        
    def test_get_attr(self):
        f = get_f_mock()
        dotkeys = ['a']
        v = View(f, dotkeys)
        res = v.b
        expected = 5
        self.assertEqual(res, expected)
        
    def test_set(self):
        f = get_f_mock()
        dotkeys = ['a']
        v = View(f, dotkeys)
        v['b'] = 99
        res = v['b']
        expected = 99
        self.assertEqual(res, expected)
        res2 = f['a.b']
        self.assertEqual(res2, expected)
        
    def test_set_remote(self):
        f = get_f_mock()
        dotkeys = ['a']
        v = View(f, dotkeys)
        f['a.b'] = 99
        res = v['b']
        expected = 99
        self.assertEqual(res, expected)
        res2 = f['a.b']
        self.assertEqual(res2, expected)
        
    def test_new_key(self):
        f = get_f_mock()
        dotkeys = ['a']
        v = View(f, dotkeys)
        f['a.new'] = 99
        res = v['new']
        expected = 99
        self.assertEqual(res, expected)
