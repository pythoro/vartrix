# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 15:32:52 2019

@author: Reuben
"""

import vartrix

def run():
    # ------ setting up a container ---- #
    # From a nested dictionary:
    dct = {'A': {'apple': 5, 'banana': 7, 'grape': 11},
           'B': {'fig': 13, 'pear': 17, 'orange': 19}}
    container = vartrix.Container(dct)
    print(container)
    # {'A.apple': 5, 'A.banana': 7, 'A.grape': 11, 'B.fig': 13, 'B.pear': 17, 'B.orange': 19}
    
    # From a flat ('dotkey') dictionary:
    dct = {'A.apple': 5, 'A.banana': 7, 'A.grape': 11,
           'B.fig': 13, 'B.pear': 17, 'B.orange': 19}
    container = vartrix.Container(dct)
    print(container)
    # {'A.apple': 5, 'A.banana': 7, 'A.grape': 11, 'B.fig': 13, 'B.pear': 17, 'B.orange': 19}
    
    # From a yaml file:
    import os
    path = os.path.dirname(__file__)
    dct = vartrix.load(os.path.join(path, 'tutorial_1.yml'))
    container = vartrix.Container(dct)
    print(container)
    # {'A.apple': 5, 'A.banana': 7, 'A.grape': 11, 'B.fig': 13, 'B.pear': 17, 'B.orange': 19}
    
    # Usually, we set one up using a Name_Space instance. You can use the default:
    c = vartrix.get_container('example_name')
    
    # Or, set up your own:
    ns = vartrix.Name_Space()
    container = ns.create('example_name_2', dct=dct)
    
    # initialise it with a dictionary, or load it. A short way is like this, as
    # new containers are created if required:
    ns['tutorial_1'].load(dct)
    
    
    # ------ setting up views  ---- #
    
    # A view removes the preceeding dots from the container keys for specific
    # subsets. For example:
    view_A = vartrix.View(ns['tutorial_1'], dotkeys='A')
    print(view_A)
    # {'apple': 5, 'banana': 7, 'grape': 11}
    
    # Views have both dictionary-style key access and attribute-style access:
    print(view_A['apple'])
    # 5
    print(view_A.apple)
    # 5
    
    # You can use them in a class like this:
    class B():
        def __init__(self):
            self.params = vartrix.View(ns['tutorial_1'], dotkeys=['B'])
    
    b = B()
    print(b.params)
    # {'fig': 13, 'pear': 17, 'orange': 19}
    
    # You can pass in the object instead. It will automatically remove the 
    # package name or '__main__' prefix on the class names.
    # It automatically recourses through base classes so inheritance works.
    class A():
        def __init__(self):
            self.params = vartrix.View(ns['tutorial_1'], obj=self)
            # Class A objects have signature 'tutorial_1.A'
    a = A()
    print(a.params)
    # {'apple': 5, 'banana': 7, 'grape': 11}
     
    # You can use multiple dotkeys:
    class Combined():
        def __init__(self):
            self.params = vartrix.View(ns['tutorial_1'], dotkeys=['A', 'B'])
    c = Combined()
    print(c.params)
    # {'A.apple': 5, 'A.banana': 7, 'A.grape': 11, 'B.fig': 13, 'B.pear': 17, 'B.orange': 19}
        
        
    # ------- Remote updates ---------
    # The views are automatically updated with changes from the container
    
    a = A()
    container = ns['tutorial_1']
    
    # Let's update the 'A.apple' value:
    container['A.apple'] = 101
    print(container['A.apple'])
    # 101
    print(a.params['apple'])
    # 101
    
    
    # We can use the 'set' method:
    container.set('A.apple', 102)
    print(container['A.apple'])
    # 102
    print(a.params['apple'])
    # 102
    
    # Use the lset method for dotkets as lists of strings.
    container.lset(['A', 'apple'], 103)
    print('---')
    print(container['A.apple'])
    # 103
    print(a.params['apple'])
    # 103
    
    # And use the dset method to set a range of values using a dictionary of dotkeys.
    container.dset({'A.apple': 104, 'A.grape': 201})
    print(container)
    # {'A.apple': 104, 'A.banana': 7, 'A.grape': 201, 'B.fig': 13, 'B.pear': 17, 'B.orange': 19}
    print(a.params)
    # {'apple': 104, 'banana': 7, 'grape': 201}
    
    # If you don't want a view to update, set the live attribute to False
    a.params.live = False
    container.dset({'A.apple': 111, 'A.grape': 222})
    print(container)
    # {'A.apple': 111, 'A.banana': 7, 'A.grape': 222, 'B.fig': 13, 'B.pear': 17, 'B.orange': 19}
    print(a.params)
    # {'apple': 104, 'banana': 7, 'grape': 201}
    a.params.live = True
    print(a.params)
    # {'apple': 111, 'banana': 7, 'grape': 222}

    # Live views stay up to date with the container, even when keys are added
    # or removed:
    backup = container.copy()
    dct = {'A.apple': 77, 'A.banana': 87, 'A.grape': 91, 'A.pineapple': 55,
           'B.fig': 102, 'B.pear': 150, 'B.orange': 300}
    container.load(dct)
    print(a.params)
    # {'apple': 77, 'banana': 87, 'grape': 91, 'pineapple': 55}
    container.load(backup)
    print(a.params)
    # {'apple': 111, 'banana': 7, 'grape': 222}

    # To only set values temporarily, use the context manager:
    print(container)
    # {'A.apple': 111, 'A.banana': 7, 'A.grape': 222, 'B.fig': 13, 'B.pear': 17, 'B.orange': 19}
    d = {'A.apple': 555, 'B.orange': -7}
    with container.context(d):
        print(container)
        # {'A.apple': 555, 'A.banana': 7, 'A.grape': 222, 'B.fig': 13, 'B.pear': 17, 'B.orange': -7}
    print(container)
    # {'A.apple': 111, 'A.banana': 7, 'A.grape': 222, 'B.fig': 13, 'B.pear': 17, 'B.orange': 19}

    
   # ------- View updates ---------
    # Sometimes, it's more convenient to set values on a view. This works
    # in a similar way. Values set on a live view are reflected in the 
    # container, and all other linked views.
    
    # Use a setitem style:
    a.params['apple'] = 1001
    print(container['A.apple'])
    # 1001
    print(a.params['apple'])
    # 1001
    
    # The set method:
    a.params.set('apple', 1002)
    print(container['A.apple'])
    # 1002
    print(a.params['apple'])
    # 1002

    # Or the dset method for multiple key-value pairs
    a.params.dset({'apple': 1003, 'grape': 2002})
    print(container)
    # {'A.apple': 1003, 'A.banana': 7, 'A.grape': 2002, 'B.fig': 13, 'B.pear': 17, 'B.orange': 19}
    print(a.params)
    # {'apple': 1003, 'banana': 7, 'grape': 2002}
        
    # Use the context manager to set values temporarily  
    
    print(a.params)
    # {'apple': 1003, 'banana': 7, 'grape': 2002}
    d2 = {'apple': 400, 'grape': 1000}
    with a.params.context(d2):
        print(a.params)
        # {'apple': 400, 'banana': 7, 'grape': 1000}
    print(a.params)
    # {'apple': 1003, 'banana': 7, 'grape': 2002}