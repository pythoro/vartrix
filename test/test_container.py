# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 19:49:18 2019

@author: Reuben
"""

import unittest

from vartrix.container import Container


class Box_Mock():
    def _box_update(self, key, val):
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

    def test_load(self):
        c = Container()
        dct = {'a.b': 6,
               'c': {'d': 9}}
        c.load(dct)
        expected = {'a.b': 6,
                    'c.d': 9}
        self.assertEqual(c.flat(), expected)
        self.assertTrue(isinstance(c['a'], Container))
        self.assertTrue(isinstance(c['c'], Container))
        
    def test_load_on_instantiate(self):
        dct = {'a.b': 6,
               'c': {'d': 9}}
        c = Container(dct)
        expected = {'a.b': 6,
                    'c.d': 9}
        self.assertEqual(c.flat(), expected)
        self.assertTrue(isinstance(c['a'], Container))
        self.assertTrue(isinstance(c['c'], Container))
        
    def test_combine(self):
        d1 = {'b': 5}
        d2 = {'d': 7}
        c1 = Container(d1)
        c2 = Container(d2)
        c = Container.combine({'c1': c1, 'c2': c2})
        expected = {'c1.b': 5,
                    'c2.d': 7}
        self.assertEqual(c.flat(), expected)
        self.assertEqual(c['c1'], c1)
        self.assertEqual(c['c2'], c2)
        
    def test_merge(self):
        d1 = {'a.b': 5}
        d2 = {'c.d': 7}
        c1 = Container(d1)
        b1 = Box_Mock()
        c1.register_observer(b1)
        c2 = Container(d2)
        b2 = Box_Mock()
        c2.register_observer(b2)
        c3 = c1['a']
        c4 = c2['c']
        c = Container.merge([c1, c2])
        expected = {'a.b': 5,
                    'c.d': 7}
        self.assertEqual(c.flat(), expected)
        self.assertEqual(c['a'], c3)
        self.assertEqual(c['c'], c4)
        self.assertIn(b1, c._observers)
        self.assertIn(b2, c._observers)