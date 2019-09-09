# vartrix

Vartrix is about managing and automating parameters used in code.

## Quickstart tutorial - basic usage

Install using:

```
pip install vartrix
```

Then in your code, import vartrix to get started:

```python
import vartrix
```

### Containers
A container is a dictionary-like object that contains a set of parameters. The keys are 'dotkeys'. For example, 'a.b.c', or 'subpackage.module.class.key'.

There are a few ways to set up containers. First, from a nested dictionary:
```python
dct = {'A': {'apple': 5, 'banana': 7, 'grape': 11},
	   'B': {'fig': 13, 'pear': 17, 'orange': 19}}
container = vartrix.Container(dct)
print(container)
# {'A.apple': 5, 'A.banana': 7, 'A.grape': 11, 'B.fig': 13, 'B.pear': 17, 'B.orange': 19}
```

From a flat ('dotkey') dictionary:
```python
dct = {'A.apple': 5, 'A.banana': 7, 'A.grape': 11,
	   'B.fig': 13, 'B.pear': 17, 'B.orange': 19}
container = vartrix.Container(dct)
print(container)
# {'A.apple': 5, 'A.banana': 7, 'A.grape': 11, 'B.fig': 13, 'B.pear': 17, 'B.orange': 19}
```

You can use any dictionary to set up the Container.

### Name spaces

Usually, we set containers up using a Name_Space instance. You can use the default:
```python
container = vartrix.get_container('example_name')
```

Or, set up your own:
```python
ns = vartrix.Name_Space()
container = ns.create('example_name_2', dct=dct)
```

Initialise it with a dictionary, like the above, or load one into it. A short way to set up a container is like this, as new containers are created if required:
```python
ns['tutorial_1'].load(dct)
```


## Views
For large containers with multiple levels, it's much easier to deal with a View of a specific set of the dotkeys. Views allow the values for those dotkeys to be accessed without the preceeding levels of the key. For example:

```python
view_A = vartrix.View(ns['tutorial_1'], dotkeys='A')
print(view_A)
# {'apple': 5, 'banana': 7, 'grape': 11}
```

Views have both dictionary-style key access and attribute-style access:
```python
print(view_A['apple'])
# 5
print(view_A.apple)
# 5
```

You can use them in a class like this:
```python
class B():
	def __init__(self):
		self.params = vartrix.View(ns['tutorial_1'], dotkeys=['B'])

b = B()
print(b.params)
# {'fig': 13, 'pear': 17, 'orange': 19}
```

You can pass in the object instead. It will automatically remove the package name or '__main__' prefix on the class names. It automatically includes base classes so inheritance works.

```python
class A():
	def __init__(self):
		self.params = vartrix.View(ns['tutorial_1'], obj=self)
		# Class A objects have signature 'tutorial_1.A'
a = A()
print(a.params)
# {'apple': 5, 'banana': 7, 'grape': 11}
```
 
You can use multiple dotkeys:
```python
class Combined():
	def __init__(self):
		self.params = vartrix.View(ns['tutorial_1'], dotkeys=['A', 'B'])
c = Combined()
print(c.params)
# {'A.apple': 5, 'A.banana': 7, 'A.grape': 11, 'B.fig': 13, 'B.pear': 17, 'B.orange': 19}
```
	
	
## Remote updates
The views are automatically updated with changes from their associated container. Let's first make a view and get a reference to the container:

```python
a = A()
container = ns['tutorial_1']
```

Let's update the 'A.apple' value using setitem style:
```python
container['A.apple'] = 101
print(container['A.apple'])
# 101
print(a.params['apple'])
# 101
```

We can use the 'set' method:
```python
container.set('A.apple', 102)
print(container['A.apple'])
# 102
```python

Use the lset method for dotkets as lists of strings:
```python
container.lset(['A', 'apple'], 103)
print(container['A.apple'])
# 103
```

And use the dset method to set a range of values using a dictionary of dotkeys:
```python
{'A.apple': 103, 'A.banana': 7, 'A.grape': 11, 'B.fig': 13, 'B.pear': 17, 'B.orange': 19}
container.dset({'A.apple': 104, 'A.grape': 201})
print(container)
{'A.apple': 104, 'A.banana': 7, 'A.grape': 201, 'B.fig': 13, 'B.pear': 17, 'B.orange': 19}
```

## Preventing updating
If you don't want a view to update, set the `live` attribute to False, like this:
```python
a.params.live = False
container.dset({'A.apple': 111, 'A.grape': 222})
print(container)
# {'A.apple': 111, 'A.banana': 7, 'A.grape': 222, 'B.fig': 13, 'B.pear': 17, 'B.orange': 19}
print(a.params)
# {'apple': 104, 'banana': 7, 'grape': 201}
```

Call the `refresh()` method to manually refresh non-live Views. They automatically refresh when they are set back to live:
```python
a.params.live = True
print(a.params)
# {'apple': 111, 'banana': 7, 'grape': 222}
```


Live views stay up to date with the container, even when keys are added or removed:
```python
backup = container.copy()
dct = {'A.apple': 77, 'A.banana': 87, 'A.grape': 91, 'A.pineapple': 55,
	   'B.fig': 102, 'B.pear': 150, 'B.orange': 300}
container.load(dct)
print(a.params)
# {'apple': 77, 'banana': 87, 'grape': 91, 'pineapple': 55}
container.load(backup)
print(a.params)
# {'apple': 111, 'banana': 7, 'grape': 222}
```

To only set values temporarily, use the context manager:
```python
print(container)
# {'A.apple': 111, 'A.banana': 7, 'A.grape': 222, 'B.fig': 13, 'B.pear': 17, 'B.orange': 19}
d = {'A.apple': 555, 'B.orange': -7}
with container.context(d):
	print(container)
	# {'A.apple': 555, 'A.banana': 7, 'A.grape': 222, 'B.fig': 13, 'B.pear': 17, 'B.orange': -7}
print(container)
# {'A.apple': 111, 'A.banana': 7, 'A.grape': 222, 'B.fig': 13, 'B.pear': 17, 'B.orange': 19}
```


## View updates
Sometimes, it's more convenient to set values on a view. This works in a similar way. Values set on a live view are reflected in the container, and all other linked views.

Use a setitem style:
```python
a.params['apple'] = 1001
print(container['A.apple'])
# 1001
print(a.params['apple'])
# 1001
```

The `set` method:
```python
a.params.set('apple', 1002)
print(container['A.apple'])
# 1002
print(a.params['apple'])
# 1002
```

Or the dset method for multiple key-value pairs:
```python
a.params.dset({'apple': 1003, 'grape': 2002})
print(container)
# {'A.apple': 1003, 'A.banana': 7, 'A.grape': 2002, 'B.fig': 13, 'B.pear': 17, 'B.orange': 19}
print(a.params)
# {'apple': 1003, 'banana': 7, 'grape': 2002}
```
	
Use the context manager to set values temporarily:
```python
print(a.params)
# {'apple': 1003, 'banana': 7, 'grape': 2002}
d2 = {'apple': 400, 'grape': 1000}
with a.params.context(d2):
	print(a.params)
	# {'apple': 400, 'banana': 7, 'grape': 1000}
print(a.params)
# {'apple': 1003, 'banana': 7, 'grape': 2002}
```
