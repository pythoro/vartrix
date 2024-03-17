# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 21:00:38 2024

@author: Reuben
"""

import pytest
from pytest import approx, fixture
from vartrix.context import Context
from vartrix import sequence
import numpy as np


@fixture
def context1():
    dct = {"a": 1, "b": 2, "c": 3, "d": 4}
    return Context(dct)


class Test_Sequence:
    def test_make_label(self):
        update_dict = {"a": 5, "b": 2, "c": 6}
        ret = sequence.make_label(update_dict)
        assert ret == "a5.00_b2.00_c6.00"

    def test_dlist(self):
        dct = {"b": [2, 3], "c": [6, 7]}
        lst = sequence.dlist(dct)
        expected = [{"b": 2, "c": 6}, {"b": 3, "c": 7}]
        assert lst == approx(expected)

    def test_combinations_from_lists(self):
        lst = [[{"a": 5}, {"a": 4}], [{"b": 2, "c": 6}, {"b": 3, "c": 7}]]
        out = sequence.combinations_from_lists(lst)
        expected = [
            {"a": 5, "b": 2, "c": 6},
            {"a": 5, "b": 3, "c": 7},
            {"a": 4, "b": 2, "c": 6},
            {"a": 4, "b": 3, "c": 7},
        ]
        assert out == approx(expected)

    def test_combinations_from_dict(self):
        dct = {"b": [2, 3], "c": [6, 7]}
        out = sequence.combinations_from_dict(dct)
        expected = [
            {"b": 2, "c": 6},
            {"b": 2, "c": 7},
            {"b": 3, "c": 6},
            {"b": 3, "c": 7},
        ]
        assert out == approx(expected)

    def test_combinations(self):
        dicts = [{"a": [4, 5]}, {"b": [2, 3], "c": [6, 7]}]
        out = sequence.combinations(dicts)
        expected = [
            {"a": 4, "b": 2, "c": 6},
            {"a": 4, "b": 3, "c": 7},
            {"a": 5, "b": 2, "c": 6},
            {"a": 5, "b": 3, "c": 7},
        ]
        assert out == approx(expected)

    def func_test(self, context, update_dict):
        return update_dict

    def test_iterate(self, context1):
        update_dicts = [
            {"b": 2, "c": 6},
            {"b": 2, "c": 7},
            {"b": 3, "c": 6},
            {"b": 3, "c": 7},
        ]
        ret = sequence.iterate(self.func_test, context1, update_dicts)
        assert ret == approx(update_dicts)
