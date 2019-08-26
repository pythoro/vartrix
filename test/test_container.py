# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 19:49:18 2019

@author: Reuben
"""

import unittest

from vartrix.container import Container


class Box_Mock():
    def box_update(self, key, val):
        self.key = key
        self.val = val
        

class Test_Container(unittest.TestCase):
    def test_instantiate(self):
        c = Container()
        self.assertTrue(isinstance(c, dict))

    def test_hash(self):
        c = Container()
        hash(c)
        
    def test_missing(self):
        c = Container()
        t = c['test']
        self.assertEqual(type(t), Container)
       
    def test_register_observer(self):
        c = Container()
        b = Box_Mock()
        c.register_observer(b)
        self.assertIn(b, c._observers)
        
    def test_update_observers(self):
        c = Container()
        b = Box_Mock()
        c.register_observer(b)
        c.update_observers('test_key', 4)
        self.assertEqual(b.key, 'test_key')
        self.assertEqual(b.val, 4)
        
    def test_dict_set_item(self):
        c = Container()
        c['a'] = 6

    def test_dict_get_item(self):
        c = Container()
        c['a'] = 6
        self.assertEqual(c['a'], 6)
        
    def test_set(self):
        c = Container()
        c.set('a.b', 6)
        self.assertEqual(type(c['a']), Container)
        self.assertEqual(c['a']['b'], 6)

    def test_get(self):
        c = Container()
        c.set('a.b', 6)
        self.assertEqual(c.get('a.b'), 6)

    def test_lset(self):
        c = Container()
        c.lset(['a', 'b'], 6)
        self.assertEqual(type(c['a']), Container)
        self.assertEqual(c['a']['b'], 6)

    def test_lget(self):
        c = Container()
        c.lset(['a', 'b'], 6)
        self.assertEqual(c.lget(['a', 'b']), 6)
        
    def test_dset(self):
        c = Container()
        dct = {'a.b': 6}
        c.dset(dct)
        self.assertEqual(type(c['a']), Container)
        self.assertEqual(c['a']['b'], 6)
        
    def test_flat(self):
        c = Container()
        dct = {'a.b': 6}
        c.dset(dct)
        self.assertEqual(c.flat(), dct)
