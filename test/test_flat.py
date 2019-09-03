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
        
    def refresh(self, dotkey):
        self.refresh = dotkey

class Test_Flat(unittest.TestCase):
    def test_instantiate(self):
        f = Flat()
        self.assertTrue(isinstance(f, dict))

    def test_load_on_init(self):
        dct = {'a.b': 6}
        f = Flat(dct)
        self.assertDictEqual(dct, f)

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
        
    def test_load(self):
        f = Flat()
        dct = {'a.b': 6}
        f.load(dct)
        self.assertDictEqual(dct, f)
        
    def test_refresh_observer_on_load(self):
        dct = {'a.b': 6}
        f = Flat(dct)
        b = View_Mock()
        f.register_observer('a', b)
        dct2 = {'a.b': 7,
                'a.e': 45}
        f.load(dct2)
        self.assertEqual(b.refresh, 'a')

    def test_combine(self):
        d1 = {'b': 5}
        d2 = {'d': 7}
        c1 = Flat(d1)
        c2 = Flat(d2)
        c = Flat.combine({'c1': c1, 'c2': c2})
        expected = {'c1.b': 5,
                    'c2.d': 7}
        self.assertEqual(c, expected)
        
    def test_merge(self):
        d1 = {'a.b': 5}
        d2 = {'c.d': 7}
        c1 = Flat(d1)
        b1 = View_Mock()
        c1.register_observer('a', b1)
        c2 = Flat(d2)
        b2 = View_Mock()
        c2.register_observer('c', b2)
        c = Flat.merge([c1, c2])
        expected = {'a.b': 5,
                    'c.d': 7}
        self.assertEqual(c, expected)
        self.assertIn(b1, c._observers['a'])
        self.assertIn(b2, c._observers['c'])
        
    def test_context(self):
        dct = {'a.b': 6, 'a.c': 7}
        f = Flat(dct)
        new1 = {'a.b': 66}
        new2 = {'a.c': 77}
        with f.context(new1):
            expected1 = {'a.b': 66, 'a.c': 7}
            self.assertDictEqual(f, expected1)
            with f.context(new2):
                expected2 = {'a.b': 66, 'a.c': 77}
                self.assertDictEqual(f, expected2)
            self.assertDictEqual(f, expected1)
        self.assertDictEqual(dct, f)