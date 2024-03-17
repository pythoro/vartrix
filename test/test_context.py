# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 20:45:45 2024

@author: Reuben
"""

import pytest
from pytest import approx, fixture
from vartrix.context import Context
import numpy as np


@fixture
def context1():
    dct = {"a": 1, "b": [2, 3], "c": np.array([4, 5]), "d": {"e": 5}}
    return Context(dct)


class Test_Context:
    def test_copy(self, context1):
        context2 = context1.copy()
        assert isinstance(context2, Context)
        assert context2 is not context1
        
    def test_setitem(self, context1):
        with pytest.raises(RuntimeError):
            context1['a'] = 5

    def test_set(self, context1):
        with pytest.raises(RuntimeError):
            context1.set('a', 5)

    def test_update(self, context1):
        with pytest.raises(RuntimeError):
            context1.update({'a', 5})
        
    def test_with_value(self, context1):
        context2 = context1.with_value("a", 101)
        assert context1["a"] == 1
        assert context2["a"] == 101

    def test_with_values(self, context1):
        context2 = context1.with_values({"a": 101, 'b': [31, 32]})
        assert context1["a"] == 1
        assert context2["a"] == 101
        assert context2["b"] == [31, 32]

    def test_get_copy_list(self, context1):
        b = context1.get("b")
        b[0] = 67
        assert context1["b"][0] == 2

    def test_get_copy_numpy(self, context1):
        c = context1.get("c")
        c[0] = 67
        assert context1["c"][0] == 4

    def test_get_copy_dict(self, context1):
        d = context1.get("d")
        d["e"] = 67
        assert context1["d"]["e"] == 5

    def test_getitem(self, context1):
        assert context1["a"] == 1

    def func_test(self, context, update_dict):
        return update_dict

    def test_iterate(self, context1):
        update_dicts = [
            {"b": 2, "c": 6},
            {"b": 2, "c": 7},
            {"b": 3, "c": 6},
            {"b": 3, "c": 7},
        ]
        ret = context1.iterate(self.func_test, update_dicts)
        assert ret == approx(update_dicts)