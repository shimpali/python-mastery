"""
a) Descriptors in action

Earlier, you created a class Stock that made use of slots, properties, and other features.
All of these features are implemented using the descriptor protocol.
See it in action by trying this simple experiment.
>>> class Stock:
...        def __init__(self, name, shares, price):
...            self.name = name
...            self.shares = shares
...            self.price = price
...        def cost(self):
...            return self.shares * self.price

First, create a stock object, and try looking up a few attributes:
>>> s = Stock('GOOG', 100, 490.10)
>>> s.name
'GOOG'
>>> s.shares
100

Now, notice that these attributes are in the class dictionary.
>>> Stock.__dict__.keys()
dict_keys(['__module__', '__init__', 'cost', '__dict__', '__weakref__', '__doc__'])

Try these steps which illustrate how descriptors get and set values on an instance:
>>> q = Stock.__dict__['shares']
>>> q.__get__(s)
100
>>> q.__set__(s,75)
>>> s.shares
75
>>> q.__set__(s, '75')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "stock.py", line 23, in shares
    raise TypeError('Expected an integer')
TypeError: Expected an integer

The execution of __get__() and __set__() occurs automatically whenever you access instances.

b) Make your own descriptor

>>> class Foo:
...        a = Descriptor('a')
...        b = Descriptor('b')
...        c = Descriptor('c')
>>> f = Foo()
>>> f
<descrip.Foo object at 0x1095f9f90>
>>> f.a
a:__get__
>>> f.b
b:__get__
>>> f.a = 23
a:__set__ 23
>>> del f.a
a:__delete__

Ponder the fact that you have captured the dot-operator for a specific attribute.

c) From Validators to Descriptors

In the previous exercise, you wrote a series of classes that could perform checking. For example:

>>> PositiveInteger.check(10)
10
>>> PositiveInteger.check('10')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
    raise TypeError('Expected %s' % cls.expected_type)
TypeError: expected <class 'int'>
>>> PositiveInteger.check(-10)


>>> class Stock:
...    name   = String('name')
...    shares = PositiveInteger('shares')
...    price  = PositiveFloat('price')
...
...    def __init__(self,name,shares,price):
...        self.name = name
...        self.shares = shares
...        self.price = price

You'll find that your class works the same way as before, involves much less code, and gives you all of the desired checking:
>>> s = Stock('GOOG', 100, 490.10)
>>> s.name
'GOOG'
>>> s.shares
100
>>> s.shares = 75
>>> s.shares = '75'
... TypeError ...
>>> s.shares = -50
... ValueError ...

(d) Fixing the Names

One annoying thing about descriptors is the redundant name specification. For example:

class Stock:
    ...
    shares = PositiveInteger('shares')
    ...
We can fix that. Change the top-level Validator class to include a __set_name__() method like this:

# validate.py

class Validator:
    def __init__(self, name=None):
        self.name = name

    def __set_name__(self, cls, name):
        self.name = name

    @classmethod
    def check(cls, value):
        return value

    def __set__(self, instance,	value):
        instance.__dict__[self.name] = self.check(value)
Now, try rewriting your Stock class so that it looks like this:

class Stock:
    name   = String()
    shares = PositiveInteger()
    price  = PositiveFloat()

    def __init__(self,name,shares,price):
        self.name = name
        self.shares = shares
        self.price = price

"""

class Descriptor:
    def __init__(self, name):
        self.name = name
    def __get__(self, instance, cls):
        print('%s:__get__' % self.name)
    def __set__(self, instance, value):
        print('%s:__set__ %s' % (self.name, value))
    def __delete__(self, instance):
        print('%s:__delete__' % self.name)


class Validator:
    def __init__(self, name):
        self.name = name

    @classmethod
    def check(cls, value):
        return value

    # Note: The lack of the __get__() method in the descriptor means that Python will
    # use its default implementation of attribute lookup.
    # This requires that the supplied name matches the name used in the instance dictionary.
    def __set__(self, instance,	value):
        instance.__dict__[self.name] = self.check(value)

