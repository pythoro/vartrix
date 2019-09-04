# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 08:47:20 2019

@author: Reuben
"""

import os
import unittest

import ruamel.yaml as yml

from vartrix.flat import Flat
from vartrix import automate

base = {'alias.one': 5,
        'alias.two': 7,
        'alias.three': 11,
        'alias.four': 17}

def get_f():
    f = Flat(base)
    return f


def get_fname():
    root = os.path.dirname(os.path.abspath(__file__))
    fname = os.path.join(root, 'automation_sets.yml')
    return fname    

def get_test_data():
    fname = get_fname()
    with open(fname) as f:
        sets = yml.safe_load(f)
    return sets

class Test_Automator(unittest.TestCase):
    pass



class Test_Aliases(unittest.TestCase):
    pass


class Test_Vector(unittest.TestCase):
    def get_vec_1(self):
        d = {'labels': ['a', 'b'],
             'alias_1': [1, 2],
             'alias_2': [3, 4]}
        return automate.Vector_Factory.new(d, 'vec_1')
    
    def test_init_labelled(self):
        v = self.get_vec_1()
        expected = [{'alias_1': 1, 'alias_2': 3}, {'alias_1': 2, 'alias_2': 4}]
        self.assertListEqual(v.data, expected)
        self.assertListEqual(v.labels, ['a', 'b'])
        
    def test_get_lst_labelled(self):
        v = self.get_vec_1()
        lst = v.get_lst()
        self.assertListEqual(lst, [{'alias_1': 1, 'alias_2': 3},
                                   {'alias_1': 2, 'alias_2': 4}])

    def test_get_label_lst_labelled(self):
        v = self.get_vec_1()
        lst = v.get_label_lst()
        self.assertListEqual(lst, [{'vec_1': 'a'},
                                   {'vec_1': 'b'}])

    def get_vec_unlabelled(self):
        d = {'alias_1': [1, 2],
             'alias_2': [3, 4]}
        return automate.Vector_Factory.new(d, 'vec_unlabelled')
    
    def test_init_unlabelled(self):
        v = self.get_vec_unlabelled()
        expected = [{'alias_1': 1, 'alias_2': 3}, {'alias_1': 2, 'alias_2': 4}]
        self.assertListEqual(v.data, expected)
        self.assertListEqual(v.labels, [0, 1])
        
    def test_get_lst_unlabelled(self):
        v = self.get_vec_unlabelled()
        lst = v.get_lst()
        self.assertListEqual(lst, [{'alias_1': 1, 'alias_2': 3},
                                   {'alias_1': 2, 'alias_2': 4}])

    def test_get_label_lst_unlabelled(self):
        v = self.get_vec_unlabelled()
        lst = v.get_label_lst()
        self.assertListEqual(lst, [{'vec_unlabelled': 0},
                                   {'vec_unlabelled': 1}])


    def get_vec_2(self):
        d = {'labels': ['c', 'd'],
             'alias_3': [5, 6],
             'alias_4': [7, 8]}
        return automate.Vector_Factory.new(d, 'vec_2')
    
    def test_get_lst_nested(self):
        v = self.get_vec_1()
        v2 = self.get_vec_2()
        v.set_child(v2)
        lst = v.get_lst()
        expected = [
            {'alias_1': 1, 'alias_2': 3, 'alias_3': 5, 'alias_4': 7},
            {'alias_1': 1, 'alias_2': 3, 'alias_3': 6, 'alias_4': 8},
            {'alias_1': 2, 'alias_2': 4, 'alias_3': 5, 'alias_4': 7},
            {'alias_1': 2, 'alias_2': 4, 'alias_3': 6, 'alias_4': 8}]
        self.assertListEqual(lst, expected)

    def test_get_label_lst_nested(self):
        v = self.get_vec_1()
        v2 = self.get_vec_2()
        v.set_child(v2)
        lst = v.get_label_lst()
        expected = [{'vec_1': 'a', 'vec_2': 'c'},
                    {'vec_1': 'a', 'vec_2': 'd'},
                    {'vec_1': 'b', 'vec_2': 'c'},
                    {'vec_1': 'b', 'vec_2': 'd'}]
        self.assertListEqual(lst, expected)


class Test_List_Vector(unittest.TestCase):
    def get_d_1(self):
        d = {'alias_1': [1, 2],
             'alias_2': [3, 4]}
        return d
    
    def test_transpose_dict(self):
        d = self.get_d_1()
        v = automate.List_Vector('test_name')
        d_test = v.transpose_dict(d)
        expected = [{'alias_1': 1, 'alias_2': 3}, {'alias_1': 2, 'alias_2': 4}]
        self.assertListEqual(d_test, expected)
    
    
class Test_Vectors(unittest.TestCase):
    def make_vectors(self):
        d = {'vec_1': {'labels': ['a', 'b'],
                       'alias_1': [1, 2],
                       'alias_2': [3, 4]},
             'vec_2': {'labels': ['c', 'd'],
                       'alias_3': [5, 6],
                       'alias_4': [7, 8]}}
        v = automate.Vectors(d)    
        return v
    
    def test_loop(self):
        v = self.make_vectors()
        val_lst, label_lst = v.loop(['vec_1', 'vec_2'])
        self.assertListEqual(val_lst, [{'alias_1': 1, 'alias_2': 3, 'alias_3': 5, 'alias_4': 7},
                                       {'alias_1': 1, 'alias_2': 3, 'alias_3': 6, 'alias_4': 8},
                                       {'alias_1': 2, 'alias_2': 4, 'alias_3': 5, 'alias_4': 7},
                                       {'alias_1': 2, 'alias_2': 4, 'alias_3': 6, 'alias_4': 8}])
        self.assertListEqual(label_lst, [{'vec_1': 'a', 'vec_2': 'c'},
                                         {'vec_1': 'a', 'vec_2': 'd'},
                                         {'vec_1': 'b', 'vec_2': 'c'},
                                         {'vec_1': 'b', 'vec_2': 'd'}])


class Test_Sequencer(unittest.TestCase):
    def get_s(self):
        all_data = get_test_data()
        data = all_data['set_1']
        s = automate.Sequencer(data['sequences'],
                               data['aliases'],
                               data['vectors'])
        return s
    
    def test_seq_1(self):
        s = self.get_s()
        sd = s.sequence('seq_1')
        expected = {'method_a': {'val_list':
                                    [{'alias.one': 0},
                                     {'alias.one': 2},
                                     {'alias.one': 3},
                                     {'alias.one': 4}],
                                'label_lst': 
                                    [{'vec_1': 0},
                                     {'vec_1': 1},
                                     {'vec_1': 2},
                                     {'vec_1': 3}]}}
        self.assertDictEqual(sd, expected)
        
    def test_seq_2(self):
        s = self.get_s()
        sd = s.sequence('seq_2')
        expected = {
            'method_b': {
                'val_list': [
                    {'alias.one': 0, 'alias.two': 2, 'alias.three': 6},
                    {'alias.one': 0, 'alias.two': 3, 'alias.three': 7},
                    {'alias.one': 0, 'alias.two': 4, 'alias.three': 8},
                    {'alias.one': 2, 'alias.two': 2, 'alias.three': 6},
                    {'alias.one': 2, 'alias.two': 3, 'alias.three': 7},
                    {'alias.one': 2, 'alias.two': 4, 'alias.three': 8},
                    {'alias.one': 3, 'alias.two': 2, 'alias.three': 6},
                    {'alias.one': 3, 'alias.two': 3, 'alias.three': 7},
                    {'alias.one': 3, 'alias.two': 4, 'alias.three': 8},
                    {'alias.one': 4, 'alias.two': 2, 'alias.three': 6},
                    {'alias.one': 4, 'alias.two': 3, 'alias.three': 7},
                    {'alias.one': 4, 'alias.two': 4, 'alias.three': 8}],
                'label_lst': [
                    {'vec_1': 0, 'vec_2': 'a'},
                    {'vec_1': 0, 'vec_2': 'b'},
                    {'vec_1': 0, 'vec_2': 'c'},
                    {'vec_1': 1, 'vec_2': 'a'},
                    {'vec_1': 1, 'vec_2': 'b'},
                    {'vec_1': 1, 'vec_2': 'c'},
                    {'vec_1': 2, 'vec_2': 'a'},
                    {'vec_1': 2, 'vec_2': 'b'},
                    {'vec_1': 2, 'vec_2': 'c'},
                    {'vec_1': 3, 'vec_2': 'a'},
                    {'vec_1': 3, 'vec_2': 'b'},
                    {'vec_1': 3, 'vec_2': 'c'}]}, 
            'method_a': {'val_list': [
                    {'alias.two': 2, 'alias.three': 6, 'alias_4': 4},
                    {'alias.two': 2, 'alias.three': 6, 'alias_4': 5},
                    {'alias.two': 3, 'alias.three': 7, 'alias_4': 4},
                    {'alias.two': 3, 'alias.three': 7, 'alias_4': 5},
                    {'alias.two': 4, 'alias.three': 8, 'alias_4': 4},
                    {'alias.two': 4, 'alias.three': 8, 'alias_4': 5}],
                'label_lst': [
                    {'vec_2': 'a', 'vec_3': 'four'},
                    {'vec_2': 'a', 'vec_3': 'five'},
                    {'vec_2': 'b', 'vec_3': 'four'},
                    {'vec_2': 'b', 'vec_3': 'five'},
                    {'vec_2': 'c', 'vec_3': 'four'},
                    {'vec_2': 'c', 'vec_3': 'five'}]}}
        self.assertDictEqual(sd, expected)
        
    
    def test_seq_3(self):
        s = self.get_s()
        sd = s.sequence('seq_3')
        expected = {
            'method_c': {
                'val_list': [
                    {'alias.one': 0, 'alias_4': 4},
                    {'alias.one': 0, 'alias_4': 5},
                    {'alias.one': 2, 'alias_4': 4},
                    {'alias.one': 2, 'alias_4': 5},
                    {'alias.one': 3, 'alias_4': 4},
                    {'alias.one': 3, 'alias_4': 5},
                    {'alias.one': 4, 'alias_4': 4},
                    {'alias.one': 4, 'alias_4': 5}],
                'label_lst': [
                    {'vec_1': 0, 'vec_3': 'four'},
                    {'vec_1': 0, 'vec_3': 'five'},
                    {'vec_1': 1, 'vec_3': 'four'},
                    {'vec_1': 1, 'vec_3': 'five'},
                    {'vec_1': 2, 'vec_3': 'four'},
                    {'vec_1': 2, 'vec_3': 'five'},
                    {'vec_1': 3, 'vec_3': 'four'},
                    {'vec_1': 3, 'vec_3': 'five'}]}}
        self.assertDictEqual(sd, expected)
        

    def test_seq_4(self):
        s = self.get_s()
        sd = s.sequence('seq_4')
        expected = {
            'method_c': {
                'val_list': [
                    {'alias_4': 4, 'alias.one': 11, 'alias.two': 12},
                    {'alias_4': 4, 'alias.one': 13, 'alias.two': 14},
                    {'alias_4': 4, 'alias.one': 14, 'alias.two': 16},
                    {'alias_4': 5, 'alias.one': 11, 'alias.two': 12},
                    {'alias_4': 5, 'alias.one': 13, 'alias.two': 14},
                    {'alias_4': 5, 'alias.one': 14, 'alias.two': 16}],
                'label_lst': [
                    {'vec_3': 'four', 'vec_4': 'a'},
                    {'vec_3': 'four', 'vec_4': 'b'},
                    {'vec_3': 'four', 'vec_4': 'c'},
                    {'vec_3': 'five', 'vec_4': 'a'},
                    {'vec_3': 'five', 'vec_4': 'b'},
                    {'vec_3': 'five', 'vec_4': 'c'}]}}
        self.assertDictEqual(sd, expected)