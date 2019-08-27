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