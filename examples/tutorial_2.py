# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 15:32:52 2019

@author: Reuben
"""

import vartrix

ns = vartrix.Name_Space()

def setup_container():
    dct = {'apple': 1,
           'orange': 2,
           'fig': 3}
    container = ns['tutorial_2']
    container.load(dct)
    

class Automated():
    def __init__(self):
        container = ns['tutorial_2']
        self.params = {'apple': ns['apple'],
                       'orange': ns['orange']}
        
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
    # {'apple': 1, 'orange': 2, 'fig': 3}
    
    # Automated class is done

    # See tutorial_2.yml
    import os
    root = os.path.dirname(__file__)
    fname = os.path.join(root, 'tutorial_2.yml')
    automator = vartrix.Automator(ns['tutorial_2'], fname)
    
    # execute set_1 with an Automated class instance
    automated = Automated()
    automator.run('set_1', automated)
    
"""
{'apple': 1, 'orange': 2, 'fig': 3}
preparing...
running sequence: seq_1
running method: method_a
calling method_a:
current labels: {'vec_1': 5, 'vec_2': 'a'}
current params: {'apple': {}, 'orange': {}}
calling method_a:
current labels: {'vec_1': 5, 'vec_2': 'b'}
current params: {'apple': {}, 'orange': {}}
calling method_a:
current labels: {'vec_1': 5, 'vec_2': 'c'}
current params: {'apple': {}, 'orange': {}}
calling method_a:
current labels: {'vec_1': 10, 'vec_2': 'a'}
current params: {'apple': {}, 'orange': {}}
calling method_a:
current labels: {'vec_1': 10, 'vec_2': 'b'}
current params: {'apple': {}, 'orange': {}}
calling method_a:
current labels: {'vec_1': 10, 'vec_2': 'c'}
current params: {'apple': {}, 'orange': {}}
calling method_a:
current labels: {'vec_1': 15, 'vec_2': 'a'}
current params: {'apple': {}, 'orange': {}}
calling method_a:
current labels: {'vec_1': 15, 'vec_2': 'b'}
current params: {'apple': {}, 'orange': {}}
calling method_a:
current labels: {'vec_1': 15, 'vec_2': 'c'}
current params: {'apple': {}, 'orange': {}}
finishing method: method_a
finishing sequence: seq_1
"""