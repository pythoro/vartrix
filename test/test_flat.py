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

class View_Mock():
    def _view_update(self, key, val):
        self.key = key
        self.val = val


class Test_Flat(unittest.TestCase):
    def test_instantiate(self):
        f = Flat()
        self.assertTrue(isinstance(f, dict))
            
    def test_register_observer(self):
        f = Flat()
        b = View_Mock()
        f.register_observer('a', b)
        self.assertIn(b, f._observers['a'])
        
    def test_update_observers(self):
        f = Flat()
        b = View_Mock()
        f.register_observer('a', b)
        f.update_observers('a.test_key', 4)
        self.assertEqual(b.key, 'test_key')
        self.assertEqual(b.val, 4)    
    
    def test_dict_set_item(self):
        f = Flat()
        f['a'] = 6

    def test_dict_get_item(self):
        f = Flat()
        f['a'] = 6
        self.assertEqual(f['a'], 6)
        
    def test_set(self):
        f = Flat()
        f.set('a.b', 6)
        self.assertEqual(f['a.b'], 6)

    def test_get(self):
        f = Flat()
        f.set('a.b', 6)
        self.assertEqual(f.get('a.b'), 6)

    def test_lset(self):
        f = Flat()
        f.lset(['a', 'b'], 6)
        expected = {'a.b': 6}
        self.assertDictEqual(f, expected)

    def test_lget(self):
        f = Flat()
        f.lset(['a', 'b'], 6)
        self.assertEqual(f.lget(['a', 'b']), 6)
        
    def test_dset(self):
        f = Flat()
        dct = {'a.b': 6}
        f.dset(dct)
        self.assertDictEqual(f, dct)
    
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