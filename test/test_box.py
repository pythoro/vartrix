# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 21:10:39 2019

@author: Reuben
"""

import unittest

from vartrix.box import Box
from vartrix.container import Container

def get_c_mock():
    c = Container()
    c.set('a.b', 5)
    c.set('b.c', 7)
    return c

class Test_Box(unittest.TestCase):
    def test_instantiate_root(self):
        c = get_c_mock()
        b = Box(c, None)
        self.assertTrue(isinstance(b, dict))
        self.assertDictEqual(c, b)
        
    def test_instantiate(self):
        c = get_c_mock()
        dotkeys = ['a']
        b = Box(c, dotkeys)
        expected = {'b': 5}
        self.assertDictEqual(b, expected)

    def test_instantiate_multiple(self):
        c = get_c_mock()
        dotkeys = ['a', 'b']
        b = Box(c, dotkeys)
        expected = {'b': 5, 'c': 7}
        self.assertDictEqual(b, expected)
        
    def test_add_dotkey(self):
        c = get_c_mock()
        dotkeys = ['a']
        b = Box(c, dotkeys)
        b._add_dotkey('b')
        expected = {'b': 5, 'c': 7}
        self.assertDictEqual(b, expected)

    def test_box_update(self):
        c = get_c_mock()
        dotkeys = ['a']
        b = Box(c, dotkeys)
        b._box_update('b', 11)        
        self.assertEqual(b['b'], 11)
        
    def test_remote_box_update(self):
        c = get_c_mock()
        dotkeys = ['a']
        b = Box(c, dotkeys)
        c.set('a.b', 11)
        self.assertEqual(b['b'], 11)
        
    def test_set(self):
        c = get_c_mock()
        dotkeys = ['a']
        b = Box(c, dotkeys)
        b.set('b', 11)
        self.assertEqual(b['b'], 11)
        self.assertEqual(c.get('a.b'), 11)
        
    def test_get_attr(self):
        c = get_c_mock()
        dotkeys = ['a']
        b = Box(c, dotkeys)
        res = b.b
        expected = 5
        self.assertEqual(res, expected)
        
    def test_set_item(self):
        c = get_c_mock()
        dotkeys = ['a']
        b = Box(c, dotkeys)
        b['b'] = 11
        self.assertEqual(b['b'], 11)
        self.assertEqual(c.get('a.b'), 11)