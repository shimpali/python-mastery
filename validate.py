"""
(a) The directions of inheritance

Python has two different "directions" of inheritance. The first is found in the concept of "single inheritance"
where a series of classes inherit from a single parent. For example, try this example:

>>> class A:
...     def spam(self):
...        print('A.spam')
>>> class B(A):
...      def spam(self):
...         print('B.spam')
...         super().spam()
>>> class C(B):
...       def spam(self):
...          print('C.spam')
...          super().spam()
>>> C.__mro__
(<class 'validate.C'>, <class 'validate.B'>, <class 'validate.A'>, <class 'object'>)
>>> c = C()
>>> c.spam()
C.spam
B.spam
A.spam

Observe that the __mro__ attribute of class C encodes all of its ancestors in order. When you invoke the spam() method, it walks the MRO class-by-class up the hierarchy.

With multiple inheritance, you get a different kind of inheritance that allows different classes to be composed together. Try this example:

>>> class Base:
...        def spam(self):
...            print('Base.spam')
>>> class X(Base):
...        def spam(self):
...            print('X.spam')
...            super().spam()
>>> class Y(Base):
...        def spam(self):
...            print('Y.spam')
...            super().spam()
>>> class Z(Base):
...        def spam(self):
...            print('Z.spam')
...            super().spam()

Notice that all of the classes above inherit from a common parent Base.
However, the classes X, Y, and Z are not directly related to each other
(there is no inheritance chain linking those classes together).

However, watch what happens in multiple inheritance:

>>> class M(X,Y,Z):
...        pass
>>> M.__mro__
(<class 'validate.M'>, <class 'validate.X'>, <class 'validate.Y'>, <class 'validate.Z'>, <class 'validate.Base'>, <class 'object'>)
>>> m = M()
>>> m.spam()
X.spam
Y.spam
Z.spam
Base.spam

Here, you see all of the classes stack together in the order supplied by the subclass.
Suppose the subclass rearranges the class order:

>>> class N(Z,Y,X):
...        pass
>>> N.__mro__
(<class 'validate.N'>, <class 'validate.Z'>, <class 'validate.Y'>, <class 'validate.X'>, <class 'validate.Base'>, <class 'object'>)
>>> n = N()
>>> n.spam()
Z.spam
Y.spam
X.spam
Base.spam

Here, you see the order of the parents flip around. Carefully pay attention to what super() is doing in both cases.
It doesn't delegate to the immediate parent of each class--instead, it moves to the next class on the MRO.
Not only that, the exact order is controlled by the child. This is pretty weird.

Also notice that the common parent Base serves to terminate the chain of super() operations.
Specifically, the Base.spam() method does not call any further methods. I
t also appears at the end of the MRO since it is the parent to all of the classes being composed together.

(b) Build a Value Checker

In Exercise 3.4, you added some properties to the Stock class that checked attributes for
different types and values (e.g., shares had to be a positive integer).
Let's play with that idea a bit.
Start by creating a file validate.py and defining the following base class:

>>> class Validator:
...    @classmethod
...    def check(cls, value):
...        return value

Now, let's make some classes for type checking:

>>> class Typed(Validator):
...    expected_type = object
...    @classmethod
...    def check(cls, value):
...        if not isinstance(value, cls.expected_type):
...            raise TypeError(f'Expected {cls.expected_type}')
...        return super().check(value)
>>> class Integer(Typed):
...    expected_type = int
>>> class Float(Typed):
...    expected_type = float
>>> class String(Typed):
...    expected_type = str

Here's how you use these classes
(Note: the use of @classmethod allows us to avoid the extra step of creating instances which we don't really need):
>>> Integer.check(10)
10
>>> Integer.check('10')
Traceback (most recent call last):
  File "<stdin>", line 1, in check
    raise TypeError(f'Expected {cls.expected_type}')
TypeError: Expected <class 'int'>
>>> String.check('10')
'10'

You could use the validators in a function. For example:

>>> def add(x, y):
...        Integer.check(x)
...        Integer.check(y)
...        return x + y
>>> add(2, 2)
4
>>> add('2', '3')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 2, in add
  File "validate.py", line 11, in check
    raise TypeError(f'Expected {cls.expected_type}')
TypeError: Expected <class 'int'>

Now, make some more classes for different kinds of domain checking:

>>> class Positive(Validator):
...    @classmethod
...    def check(cls, value):
...        if value < 0:
...            raise ValueError('Expected >= 0')
...        return super().check(value)
>>> class NonEmpty(Validator):
...    @classmethod
...    def check(cls, value):
...        if len(value) == 0:
...            raise ValueError('Must be non-empty')
...        return super().check(value)

Where is all of this going? Let's start composing classes together with multiple inheritance like toy blocks:
>>> class PositiveInteger(Integer, Positive):
...    pass
>>> class PositiveFloat(Float, Positive):
...    pass
>>> class NonEmptyString(String, NonEmpty):
...    pass

Essentially, you're taking existing validators and composing them together into new ones. Madness!
However, let's use them to validate some things now:

>>> PositiveInteger.check(10)
10
>>> PositiveInteger.check('10')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
    raise TypeError(f'Expected {cls.expected_type}')
TypeError: Expected <class 'int'>
>>> PositiveInteger.check(-10)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
    raise ValueError('Expected >= 0')
ValueError: Must be >= 0

>>> NonEmptyString.check('hello')
'hello'
>>> NonEmptyString.check('')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
    raise ValueError('Must be non-empty')
ValueError: Must be non-empty

c) Using your validators

Your validators can be used to add value checking to functions and classes. For example, perhaps the validators could be used in the properties of Stock:
>>> class Stock:
...    @property
...    def shares(self):
...        return self._shares
...
...
...    @shares.setter
...    def shares(self, value):
...        self._shares = PositiveInteger.check(value)

"""