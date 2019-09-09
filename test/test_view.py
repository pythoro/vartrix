# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 21:11:42 2019

@author: Reuben
"""

import unittest

from vartrix.container import Container
from vartrix.view import View

def get_c():
    c = Container()
    c.set('a.b', 5)
    c.set('b.c', 7)
    return c

class Test_View(unittest.TestCase):
    def test_init(self):
        c = get_c()
        dotkeys = ['a']
        v = View(c, dotkeys)
        self.assertTrue(isinstance(v, dict))
        
    def test_init_none(self):
        c = get_c()
        v = View(c, dotkeys=None)
        self.assertTrue(isinstance(v, dict))
        self.assertDictEqual(c, v)

    def test_init_empty(self):
        c = get_c()
        v = View(c, dotkeys=[''])
        self.assertTrue(isinstance(v, dict))
        self.assertDictEqual(c, v)

    def test_init_dot(self):
        c = get_c()
        v = View(c, dotkeys=['.'])
        self.assertTrue(isinstance(v, dict))
        self.assertDictEqual(c, v)
    
    def test_get(self):
        c = get_c()
        dotkeys = ['a']
        v = View(c, dotkeys)
        res = v['b']
        expected = 5
        self.assertEqual(res, expected)

    def test_get_attr(self):
        c = get_c()
        dotkeys = ['a']
        v = View(c, dotkeys)
        res = v.b
        expected = 5
        self.assertEqual(res, expected)
        
    def test_refresh(self):
        c = get_c()
        dotkeys = ['a']
        v = View(c, dotkeys)
        v.clear()
        v.refresh('a')
        res = v['b']
        expected = 5
        self.assertEqual(res, expected)
                
    def test_refresh_attr(self):
        c = get_c()
        dotkeys = ['a']
        v = View(c, dotkeys)
        del v.b
        v.refresh('a')
        res = v.b
        expected = 5
        self.assertEqual(res, expected)   
        
    def test_refresh_all(self):
        c = get_c()
        dotkeys = ['a']
        v = View(c, dotkeys)
        v.clear()
        v.refresh_all()
        res = v['b']
        expected = 5
        self.assertEqual(res, expected)
        
    def test_set(self):
        c = get_c()
        dotkeys = ['a']
        v = View(c, dotkeys)
        v['b'] = 99
        res = v['b']
        expected = 99
        self.assertEqual(res, expected)
        res2 = c['a.b']
        self.assertEqual(res2, expected)
        
    def test_set_remote(self):
        c = get_c()
        dotkeys = ['a']
        v = View(c, dotkeys)
        c['a.b'] = 99
        res = v['b']
        expected = 99
        self.assertEqual(res, expected)
        res2 = c['a.b']
        self.assertEqual(res2, expected)
        
    def test_new_key(self):
        c = get_c()
        dotkeys = ['a']
        v = View(c, dotkeys)
        c['a.new'] = 99
        res = v['new']
        expected = 99
        self.assertEqual(res, expected)
