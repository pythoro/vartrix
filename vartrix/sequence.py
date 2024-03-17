# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 10:20:52 2024

@author: Reuben

Function to generate and run through sequences of parameters.

"""

from __future__ import annotations
import typing
from itertools import product
from . import context


def make_label(update_dict, abbr=None) -> str:
    """Make a string label for an update_dict

    >>> update_dict = {'a': 5, 'b': 2, 'c': 6}
    >>> make_label(update_dict)
    'a5.00_b2.00_c6.00'
    """
    abbrs = {k: k for k in update_dict.keys()}
    if abbr is not None:
        abbrs.update(abbr)
    vals = [abbrs[k] + f"{v:0.2f}" for k, v in update_dict.items()]
    return "_".join(vals)


def dlist(dct: dict) -> list[dict]:
    """Make a list of dictionaries for multiple symultaneous key values

    Args:
        dct (dict): A dictionary. Each value should be an interable, and
            all iterables must be the same length.

    Returns:
        list: A list of dictionaries for use in the `combinations_from_list`
        function.

    >>> dct = {'b': [2, 3], 'c': [6, 7]}
    >>> dlist(dct)
    [{'b': 2, 'c': 6},
     {'b': 3, 'c': 7}]
    """
    keys = list(dct.keys())
    vals = list(dct.values())
    transposed = list(zip(*vals))
    return [{k: v for k, v in zip(keys, val)} for val in transposed]


def combinations_from_lists(lst: list[list[dict]]) -> list[dict]:
    """Create update_dicts from a list of sublists of dicts

    Each sublist dictionary represents one set of values. The items in each
    sublist are combined with every other possible set of values from the
    other sublists.

    Each key in each dictionary must match one in the Context.

    >>> lst = [[{'a': 5}, {'a': 4}], [{'b': 2, 'c': 6}, {'b': 3, 'c': 7}]]
    >>> combinations_from_lists(lst)
    [{'a': 5, 'b': 2, 'c': 6},
     {'a': 5, 'b': 3, 'c': 7},
     {'a': 4, 'b': 2, 'c': 6},
     {'a': 4, 'b': 3, 'c': 7}]
    """
    combs = list(product(*lst))
    return [{l: v for dct in tup for l, v in dct.items()} for tup in combs]


def combinations_from_dict(dct: dict) -> list[dict]:
    """Create update_dicts from a dictionary

    Each key in the dictionary must match one in the Context.

    Each value in the dictionary must be an iterable. Each value in each
    iterable is combined with with every other possible set of values in the
    other iterables.

    >>> dct = {'b': [2, 3], 'c': [6, 7]}
    >>> combinations_from_dict(dct)
    [{'b': 2, 'c': 6},
     {'b': 2, 'c': 7},
     {'b': 3, 'c': 6},
     {'b': 3, 'c': 7}]
    """
    combs = list(product(*dct.values()))
    labels = list(dct.keys())
    return [{l: v for l, v in zip(labels, vals)} for vals in combs]


def iterate(
    func: typing.Callable, context: context.Context, update_dicts: list[dict]
) -> list:
    """Call a function with a context updated with each update_dict

    Returns:
        A list of return values.
    """
    returns = []
    for update_dict in update_dicts:
        loop_context = context.with_values(update_dict, safe=True)
        returns.append(func(loop_context, update_dict))
    return returns
