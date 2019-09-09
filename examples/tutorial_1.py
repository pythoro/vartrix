# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 15:32:52 2019

@author: Reuben
"""

import vartrix


def get_container_from_nested():
    dct = {'A': {'apple': 5, 'banana': 7, 'grape': 11},
           'B': {'fig': 13, 'pear': 17, 'orange': 19}}
    container = vartrix.Container(dct)
    return container

def get_container_from_flat():
    dct = {'A.apple': 5, 'A.banana': 7, 'A.grape': 11,
           'B.fig': 13, 'B.pear': 17, 'B.orange': 19}
    container = vartrix.Container(dct)
    return container

ns = vartrix.Name_Space()
ns['tutorial_1'] = get_container_from_nested()


class A():
    def __init__(self):
        self.params = vartrix.View(ns['tutorial_1'], obj=self)
        
class A2():
    def __init__(self):
        self.params = vartrix.View(ns['tutorial_1'], dotkeys='A')
        
class B():
    def __init__(self):
        self.params = vartrix.View(ns['tutorial_1'], dotkeys=['B'])
        
class Combined():
    def __init__(self):
        self.params = vartrix.View(ns['tutorial_1'], dotkeys=['A', 'B'])
        
def demo_A():
    a = A()
    print(a.params)
    
def demo_A2():
    a = A2()
    print(a.params)
    
def demo_B():
    b = B()
    print(b.params)
    
def demo_Combined():
    c = Combined()
    print(c.params)
    
    
def demo_A_remote_update():
    a = A()
    container = ns['tutorial_1']
    
    container['A.apple'] = 101
    print('---')
    print(container)
    print(a.params)

    container.set('A.apple', 102)
    print('---')
    print(container)
    print(a.params)
    
    container.lset(['A', 'apple'], 103)
    print('---')
    print(container)
    print(a.params)

    container.dset({'A.apple': 104, 'A.grape': 201})
    print('---')
    print(container)
    print(a.params)
    

def demo_A_local_update():
    a = A()
    container = ns['tutorial_1']

    print('---')
    print(container)
    print(a.params)

    a.params['apple'] = 1001
    print('---')
    print(container)
    print(a.params)
    
    a.params.set('apple', 1002)
    print('---')
    print(container)
    print(a.params)

    a.params.dset({'apple': 1003, 'grape': 2002})
    print('---')
    print(container)
    print(a.params)
    
