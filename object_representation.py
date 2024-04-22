"""
Start this exercise, by going back to a simple version of the Stock class you created.
At the interactive prompt, define a new class called SimpleStock:
>>> class SimpleStock:
...        def __init__(self, name, shares, price):
...            self.name = name
...            self.shares = shares
...            self.price = price
...        def cost(self):
...            return self.shares * self.price

Once you have defined this class, create a few instances.
>>> goog = SimpleStock('GOOG',100,490.10)
>>> ibm  = SimpleStock('IBM',50, 91.23)

(a) Representation of Instances

At the interactive shell, inspect the underlying dictionaries of the two instances you created:
>>> goog.__dict__
{'name': 'GOOG', 'shares': 100, 'price': 490.1}
>>> ibm.__dict__
{'name': 'IBM', 'shares': 50, 'price': 91.23}

(b) Modification of Instance Data

Try setting a new attribute on one of the above instances:
>>> goog.date = "6/11/2007"
>>> goog.__dict__
{'name': 'GOOG', 'shares': 100, 'price': 490.1, 'date': '6/11/2007'}
>>> ibm.__dict__
{'name': 'IBM', 'shares': 50, 'price': 91.23}

In the above output, you'll notice that the goog instance has a attribute date whereas the ibm instance does not.
It is important to note that Python really doesn't place any restrictions on attributes. For example, the attributes of an instance are not limited to those set up in the __init__() method.

Instead of setting an attribute, try placing a new value directly into the __dict__ object:
>>> goog.__dict__['time'] = '9:45am'
>>> goog.time
'9:45am'

Here, you really notice the fact that an instance is a layer on top of a dictionary.

(c) The role of classes

The definitions that make up a class definition are shared by all instances of that class.
Notice, that all instances have a link back to their associated class:
>>> goog.__class__
<class 'object_representation.SimpleStock'>
>>> ibm.__class__
<class 'object_representation.SimpleStock'>

Try calling a method on the instances:
>>> goog.cost()
49010.0
>>> ibm.cost()
4561.5

Notice that the name 'cost' is not defined in either goog.__dict__ or ibm.__dict__.
Instead, it is being supplied by the class dictionary. Try this:
>>> SimpleStock.__dict__['cost']
<function SimpleStock.cost at 0x10b1ecb80>

Try callng the cost() method directly through the dictionary:

>>> SimpleStock.__dict__['cost'](goog)
49010.0
>>> SimpleStock.__dict__['cost'](ibm)
4561.5

Notice how you are calling the function defined in the class definition and how the self argument gets the instance.

If you add a new value to the class, it becomes a class variable that's visible to all instances. Try it:
>>> SimpleStock.spam = 42
>>> ibm.spam
42
>>> goog.spam
42

Observe that spam is not part of the instance dictionary.
>>> ibm.__dict__
{'name': 'IBM', 'shares': 50, 'price': 91.23}

Instead, it's part of the class dictionary:
>>> SimpleStock.__dict__['spam']
42

"""