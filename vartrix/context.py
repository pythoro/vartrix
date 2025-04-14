# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 08:32:42 2024

@author: Reuben

A Context is a dictionary-like object with some differences.

1. Setting or updating the context results in a new context object.
2. Getting a value will provide a copy of any mutable object (a list, dict, or
   np.array).

These two differences ensure that the context is not accidentally changed then
used.

"""

from __future__ import annotations
import typing
import numpy as np
from . import sequence


class Context(dict):
    """A dictionary-like object used to store attributes"""

    def __init__(self, *args, aliases=None, **kwargs):
        self._aliases = aliases
        dict.__init__(self, *args, **kwargs)

    def copy(self):
        d = dict.copy(self)
        return Context(d, aliases=self._aliases)

    def __setitem__(self, key: str, value: typing.Any) -> None:
        raise RuntimeError("Use the with_value method instead.")

    def set(self, key: str, value: typing.Any) -> None:
        raise RuntimeError("Use the with_value method instead.")

    def update(self, dct: dict) -> None:
        raise RuntimeError("Use the with_values method instead.")

    def with_value(
        self, key: str, value: typing.Any, safe: bool = True
    ) -> Context:
        """Return a new Context instance with a changed value"""
        if safe:
            assert key in self, "Key not in container: " + str(key)
        d = dict.copy(self)
        d[key] = value
        return Context(d, aliases=self._aliases)

    def with_values(self, dct: dict, safe: bool = True) -> Context:
        """Return a new Context instance with multiple changed values"""
        if safe:
            for key in dct.keys():
                assert key in self, "Key not in container: " + str(key)
        d = dict.copy(self)
        d.update(dct)
        return Context(d, aliases=self._aliases)

    def get(self, key: str) -> typing.Any:
        """Get a value"""
        return self.__getitem__(key)

    def __getitem__(self, key: str) -> typing.Any:
        """Get a value"""
        try:
            val = dict.__getitem__(self, key)
        except KeyError:
            if self._aliases is None:
                raise KeyError("Key not in Context: " + str(key))
            try:
                val = dict.__getitem__(self, self._aliases[key])
            except KeyError:
                raise KeyError("Key not in Context or aliases: " + str(key))
        if isinstance(val, (list, dict, np.ndarray)):
            return val.copy()
        return val

    def iterate(self, func: typing.Callable, update_dicts: list[dict]):
        """Iterates over contexts updated with a list of dictionaries"""
        return sequence.iterate(func, self, update_dicts)
