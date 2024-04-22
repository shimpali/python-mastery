"""
a) Slots vs. setattr

In previous exercises, __slots__ was used to list the instance attributes on a class.
The primary purpose of slots is to optimize the use of memory.
A secondary effect is that it strictly limits the allowed attributes to those listed.
A downside of slots is that it often interacts strangely with other parts of Python (for example, classes using slots can't be used with multiple inheritance).
For that reason, you really shouldn't use slots except in special cases.

If you really wanted to limit the set of allowed attributes, an alternate way to do it would be to define a __setattr__() method. Try this experiment:
>>> class Stock:
...        def __init__(self, name, shares, price):
...            self.name = name
...            self.shares = shares
...            self.price = price
...        def __setattr__(self, name, value):
...            if name not in { 'name', 'shares', 'price' }:
...                raise AttributeError('No attribute %s' % name)
...            super().__setattr__(name, value)

>>> s = Stock('GOOG', 100, 490.1)
>>> s.name
'GOOG'
>>> s.shares = 75
>>> s.share = 50
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 8, in __setattr__
AttributeError: No attribute share


In this example, there are no slots, but the __setattr__() method still restricts attributes to those in a predefined set.
You'd probably need to think about how this approach might interact with inheritance
(e.g., if subclasses wanted to add new attributes, they'd probably need to redefine __setattr__() to make it work).

(b) Proxies

A proxy class is a class that wraps around an existing class and provides a similar interface.
Define the following class which makes a read-only layer around an existing object:

>>> class Readonly:
...        def __init__(self, obj):
...            self.__dict__['_obj'] = obj
...        def __setattr__(self, name, value):
...            raise AttributeError("Can't set attribute")
...        def __getattr__(self, name):
...            return getattr(self._obj, name)

To use the class, you simply wrap it around an existing instance:
>>> from stock import Stock
>>> s = Stock('GOOG', 100, 490.1)
>>> p = Readonly(s)
>>> p.name
'GOOG'
>>> p.shares
100
>>> p.cost
<bound method Stock.cost of Stock('GOOG', 100, 490.1)>
>>> p.shares = 50
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 8, in __setattr__
AttributeError: Can't set attribute

(c) Delegation as an alternative to inheritance

Delegation is sometimes used as an alternative to inheritance.
The idea is almost the same as the proxy class you defined in part (b). Try defining the following class:

>>> class Spam:
...        def a(self):
...            print('Spam.a')
...        def b(self):
...            print('Spam.b')

Now, make a class that wraps around it and redefines some of the methods:
>>> class MySpam:
...        def __init__(self):
...            self._spam = Spam()
...        def a(self):
...            print('MySpam.a')
...            self._spam.a()
...        def c(self):
...            print('MySpam.c')
...        def __getattr__(self, name):
...            return getattr(self._spam, name)

>>> s = MySpam()
>>> s.a()
MySpam.a
Spam.a
>>> s.b()
Spam.b
>>> s.c()
MySpam.c
>>>

Carefully notice that the resulting class looks very similar to inheritance.
For example the a() method is doing something similar to the super() call.
The method b() is picked up via the __getattr__() method which delegates to the internally held Spam instance.

The __getattr__() method is commonly defined on classes that act as wrappers around other objects.
However, you have to be aware that the process of wrapping another object in this manner often introduces other complexities.
For example, the wrapper object might break type-checking if any other part of the application is using the isinstance() function.

Delegating methods through __getattr__() also doesn't work with special methods such as __getitem__(), __enter__(), and so forth.
If a class makes extensive use of such methods, you'll have to provide similar functions in your wrapper class.

"""