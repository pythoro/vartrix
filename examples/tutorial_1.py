# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 15:32:52 2019

@author: Reuben
"""

import vartrix
from vartrix.utils import Attrdict

dct = {'widget_a': 1,
       'widget_b': 2.5,
       'config_a': [5, 6, 7],
       'config_b': {'a': 9}}


def container_setup():
    container = vartrix.Container(dct)
    print(container)
    # {'widget_a': 1, 'widget_b': 2.5, 'config_a': [5, 6, 7], 'config_b': {'a': 9}}

def container_load():
    container = vartrix.Container()
    container.load(dct)
    print(container)
    # {'widget_a': 1, 'widget_b': 2.5, 'config_a': [5, 6, 7], 'config_b': {'a': 9}}


def container_reset():
    container = vartrix.Container(dct)
    container['temp'] = 'sfdt'
    container['widget_a'] = 67
    container.reset()
    print(container)
    # {'widget_a': 1, 'widget_b': 2.5, 'config_a': [5, 6, 7], 'config_b': {'a': 9}}
    
def load_from_file():
    # From a yaml file:
    import os
    path = os.path.dirname(__file__)
    d = vartrix.load(os.path.join(path, 'tutorial_1.yml'))
    container = vartrix.Container(d)
    print(container)
    # {'A.apple': 5, 'A.banana': 7, 'A.grape': 11, 'B.fig': 13, 'B.pear': 17, 'B.orange': 19}

def make_a_container():
    # You can use the default Namespace:
    c = vartrix.get_container('example_3')
    c.load(dct)
    return c

def get_the_same_container():
    """ We can get the same container again elsewhere in the code """
    c1 = example_3()
    c2 = vartrix.get_container('example_3')
    if c1 is c2:
        print('Got the same container.')
    
def custom_namespace():
    # Set up your own:
    ns = vartrix.Name_Space()
    container = ns.create('example_4', dct=dct)
    
    # You can also create a new container like this:
    c = ns['tutorial_1']


def using_in_class():
    """ Copy values over like this """
    make_a_container()
    c = vartrix.get_container('example_3')
   
    class Widget():
        def __init__(self):
            c = vartrix.get_container('example_3')
            self.params = {'a': c['widget_a'],
                           'b': c['widget_b']}
    
    widget = Widget()
    print(widget.params)
    # {'a': 1, 'b': 2.5}
    
def using_in_class_2():
    """ Or like this"""
    make_a_container()
    c = vartrix.get_container('example_3')
   
    class Widget():
        def __init__(self):
            c = vartrix.get_container('example_3')
            self.params = Attrdict({'a': c['widget_a'],
                                    'b': c['widget_b']})
    
    widget = Widget()
    print(widget.params.a)  # 1
    print(widget.params.b)  # 2.5
    return widget.params
         
def safely_set_values():
    """ We can use the 'set' method to use the 'safe' attribute """
    container = vartrix.Container(dct)
    container.set('missing_key', 102, safe=True)
    KeyError: 'In safe mode, key missing_key must be present.'
    
def set_by_dictionary():
    container = vartrix.Container(dct)
    new_dict = {'new_1': 104, 'new_2': 201}
    container.dset(new_dict)
    print(container)
    # {'widget_a': 1, 'widget_b': 2.5, 'config_a': [5, 6, 7],
    #  'config_b': {'a': 9}, 'new_1': 104, 'new_2': 201}
    # safe=True is also an optional argument

def context_manager():
    # To only set values temporarily, use the context manager:
    print(container)
    # {'A.apple': 111, 'A.banana': 7, 'A.grape': 222, 'B.fig': 13, 'B.pear': 17, 'B.orange': 19}
    d = {'A.apple': 555, 'B.orange': -7}
    with container.context(d):
        print(container)
        # {'A.apple': 555, 'A.banana': 7, 'A.grape': 222, 'B.fig': 13, 'B.pear': 17, 'B.orange': -7}
    print(container)
    # {'A.apple': 111, 'A.banana': 7, 'A.grape': 222, 'B.fig': 13, 'B.pear': 17, 'B.orange': 19}

