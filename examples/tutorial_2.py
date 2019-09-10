# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 15:32:52 2019

@author: Reuben
"""

import vartrix
import os


ns = vartrix.Name_Space()

def setup_container():
    dct = {'A': {'apple': 1},
           'B': {'orange': 2, 'fig': 3}}
    container = ns['tutorial_2']
    container.load(dct)
    

class Automated():
    def __init__(self):
        self.params = vartrix.View(ns['tutorial_2'], dotkeys=['A', 'B'])
        
    def prepare(self):
        print('preparing...')

    def prepare_sequence(self, seq_name):
        print('running sequence: ' + seq_name)

    def prepare_method(self, method_name):
        print('running method: ' + method_name)

    def method_a(self, seq_name, val_dct, label_dct):
        print('calling method_a:')
        print('current labels: ' + str(label_dct))
        print('current params: ' + str(self.params))

    def finish_method(self, method_name):
        print('finishing method: ' + method_name)

    def finish_sequence(self, seq_name):
        print('finishing sequence: ' + seq_name)

    def finish(self):
        self.finish = True

def run():
    #s set up container
    setup_container()
    print(ns['tutorial_2'])
    # {'A.apple': 1, 'B.orange': 2, 'B.fig': 3}
    
    # Automated class is done

    # See tutorial_2.yml
    root = os.path.dirname(__file__)
    fname = os.path.join(root, 'tutorial_2.yml')
    automator = vartrix.Automator(ns['tutorial_2'], fname)
    
    # execute set_1 with an Automated class instance
    automated = Automated()
    automator.run('set_1', automated)
    
'''
preparing...
running sequence: seq_1
running method: method_a
calling method_a:
current labels: {'vec_1': 0, 'vec_2': 'a'}
current params: {'apple': 5, 'orange': 2, 'fig': 6}
calling method_a:
current labels: {'vec_1': 0, 'vec_2': 'b'}
current params: {'apple': 5, 'orange': 3, 'fig': 7}
calling method_a:
current labels: {'vec_1': 0, 'vec_2': 'c'}
current params: {'apple': 5, 'orange': 4, 'fig': 8}
calling method_a:
current labels: {'vec_1': 1, 'vec_2': 'a'}
current params: {'apple': 10, 'orange': 2, 'fig': 6}
calling method_a:
current labels: {'vec_1': 1, 'vec_2': 'b'}
current params: {'apple': 10, 'orange': 3, 'fig': 7}
calling method_a:
current labels: {'vec_1': 1, 'vec_2': 'c'}
current params: {'apple': 10, 'orange': 4, 'fig': 8}
calling method_a:
current labels: {'vec_1': 2, 'vec_2': 'a'}
current params: {'apple': 15, 'orange': 2, 'fig': 6}
calling method_a:
current labels: {'vec_1': 2, 'vec_2': 'b'}
current params: {'apple': 15, 'orange': 3, 'fig': 7}
calling method_a:
current labels: {'vec_1': 2, 'vec_2': 'c'}
current params: {'apple': 15, 'orange': 4, 'fig': 8}
finishing method: method_a
finishing sequence: seq_1
'''