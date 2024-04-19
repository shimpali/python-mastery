"""
(a) The Three Operations

The entire Python object system consists of just three core operations: getting, setting, and deleting of attributes.
Normally, these are accessed via the dot (.) like this:

>>> s = Stock('GOOG', 100, 490.1)
>>> s.name  # get
'GOOG'
>>> s.shares = 50  # set
>>> del s.shares  # delete

The three operations are also available as functions. For example:

>>> getattr(s, 'name')  # Same as s.name
'GOOG'
>>> setattr(s, 'shares', 50)  # Same as s.shares = 50
>>> delattr(s, 'shares')  # Same as del s.shares

An additional function hasattr() can be used to probe an object for the existence of an attribute:

>>> hasattr(s, 'name')
True
>>> hasattr(s, 'blah')
False

(b) Using getattr()

The getattr() function is extremely useful for writing code that processes objects in an extremely generic way.
To illustrate, consider this example which prints out
a set of user-defined attributes:

>>> s = Stock('GOOG', 100, 490.1)
>>> fields = ['name', 'shares', 'price']
>>> for name in fields:
...     print(name, getattr(s, name))
name GOOG
shares 100
price 490.1

(c) Table Output
In Exercise 3.1, you wrote a function print_portfolio() that made a nicely formatted table. That function was custom
tailored to a list of Stock objects. However, it can be completely generalized to work with any list of objects using the
technique in part (b).

Create a new module called tableformat.py. In that program, write a function print_table() that takes a sequence
(list) of objects, a list of attribute names, and prints a nicely formatted table. For example:

>>> import stock
>>> import tableformat
>>> portfolio = stock.read_portfolio('Data/portfolio.csv')
>>> tableformat.print_table(portfolio, ['name', 'shares', 'price'])
      name     shares      price
---------- ---------- ----------
        AA        100       32.2
       IBM         50       91.1
       CAT        150      83.44
      MSFT        200      51.23
        GE         95      40.37
      MSFT         50       65.1
       IBM        100      70.44

>>> tableformat.print_table(portfolio, ['shares', 'name'])
  shares       name
---------- ----------
       100         AA
        50        IBM
       150        CAT
       200       MSFT
        95         GE
        50       MSFT
       100        IBM

d) Bound Methods
It may be surprising, but method calls are layered onto the machinery used for simple attributes. Essentially, a method
is an attribute that executes when you add the required parentheses () to call it like a function. For example:
>>> s = Stock('GOOG', 100, 490.10)
>>> s.cost  # Looks up the method
 <bound method Stock.cost of <tableformat.Stock object at 0x10cdf6a10>>
>>> s.cost()  # Looks up and calls the method
49010.0
>>>  # Same operations using getattr()
>>> getattr(s, 'cost')
 <bound method Stock.cost of <tableformat.Stock object at 0x10cdf6a10>>
>>> getattr(s, 'cost')()
49010.0

A bound method is attached to the object where it came from.
If that object is modified, the method will see the modifications.
You can view the original object by inspecting the __self__ attribute of the method.
>>> c = s.cost
>>> c()
49010.0
>>> s.shares = 75
>>> c()
36757.5
>>> c.__self__
<tableformat.Stock object at 0x1095f7290>
>>> c.__func__
<function Stock.cost at 0x1095ec900>
>>> c.__func__(c.__self__)  # This is what happens behind the scenes of calling c()
36757.5

Try it with the sell() method just to make sure you understand the mechanics:
>>> f = s.sell
>>> f.__func__(f.__self__, 25)  # Same as s.sell(25)
>>> s.shares
50

>>> import stock
>>> import reader
>>> import tableformat
>>> portfolio = reader.read_csv_as_instances('Data/portfolio.csv', stock.Stock)
>>> tableformat.print_table(portfolio, ['name','shares','price'])
      name     shares      price
---------- ---------- ----------
        AA        100       32.2
       IBM         50       91.1
       CAT        150      83.44
      MSFT        200      51.23
        GE         95      40.37
      MSFT         50       65.1
       IBM        100      70.44

>>> import stock, reader, tableformat
>>> portfolio = reader.read_csv_as_instances('Data/portfolio.csv', stock.Stock)
>>> formatter = tableformat.TableFormatter()
>>> tableformat.print_table_class(portfolio, ['name', 'shares', 'price'], formatter)
Traceback (most recent call last):
...
NotImplementedError

>>> import stock, reader, tableformat
>>> portfolio = reader.read_csv_as_instances('Data/portfolio.csv', stock.Stock)
>>> formatter = tableformat.TextTableFormatter()
>>> tableformat.print_table_class(portfolio, ['name','shares','price'], formatter)
      name     shares      price
---------- ---------- ----------
        AA        100       32.2
       IBM         50       91.1
       CAT        150      83.44
      MSFT        200      51.23
        GE         95      40.37
      MSFT         50       65.1
       IBM        100      70.44


>>> import tableformat portfolio = reader.read_csv_as_instances('Data/portfolio.csv', stock.Stock)
>>> formatter = tableformat.CSVTableFormatter()
>>> tableformat.print_table_class(portfolio, ['name','shares','price'], formatter)
name,shares,price
AA,100,32.2
IBM,50,91.1
CAT,150,83.44
MSFT,200,51.23
GE,95,40.37
MSFT,50,65.1
IBM,100,70.44

>>> import stock, reader, tableformat
>>> portfolio = reader.read_csv_as_instances('Data/portfolio.csv', stock.Stock)
>>> formatter = tableformat.HTMLTableFormatter()
>>> tableformat.print_table_class(portfolio, ['name','shares','price'], formatter)
<tr> <th>name</th> <th>shares</th> <th>price</th> </tr>
<tr> <td>AA</td> <td>100</td> <td>32.2</td> </tr>
<tr> <td>IBM</td> <td>50</td> <td>91.1</td> </tr>
<tr> <td>CAT</td> <td>150</td> <td>83.44</td> </tr>
<tr> <td>MSFT</td> <td>200</td> <td>51.23</td> </tr>
<tr> <td>GE</td> <td>95</td> <td>40.37</td> </tr>
<tr> <td>MSFT</td> <td>50</td> <td>65.1</td> </tr>
<tr> <td>IBM</td> <td>100</td> <td>70.44</td> </tr>

>>> from tableformat import create_formatter, print_table_class
>>> formatter = create_formatter('html')
>>> print_table_class(portfolio, ['name','shares','price'], formatter)
<tr> <th>name</th> <th>shares</th> <th>price</th> </tr>
<tr> <td>AA</td> <td>100</td> <td>32.2</td> </tr>
<tr> <td>IBM</td> <td>50</td> <td>91.1</td> </tr>
<tr> <td>CAT</td> <td>150</td> <td>83.44</td> </tr>
<tr> <td>MSFT</td> <td>200</td> <td>51.23</td> </tr>
<tr> <td>GE</td> <td>95</td> <td>40.37</td> </tr>
<tr> <td>MSFT</td> <td>50</td> <td>65.1</td> </tr>
<tr> <td>IBM</td> <td>100</td> <td>70.44</td> </tr>

The TableFormatter class in this exercise is an example of something known as an "Abstract Base Class."
It's not something that's meant to be used directly. Instead, it's serving as a kind of interface specification for a
program component--in this case the various output formats.
Essentially, the code that produces the table will be programmed
against the abstract base class with the expectation that a user will provide a suitable implementation.

(a) Interfaces and type checking

>>> import stock, reader, tableformat
>>> portfolio = reader.read_csv_as_instances('Data/portfolio.csv', stock.Stock)
>>> class MyFormatter:
...      def headings(self, headers): pass
...      def row(self, rowdata): pass

>>> tableformat.print_table(portfolio, ['name','shares','price'], MyFormatter())
Traceback (most recent call last):
...
TypeError: Expected a TableFormatter

(b) Abstract Base Classes

Modify the TableFormatter base class so that it is defined as a proper abstract base class using the abc module.
Once you have done that, try this experiment:
>>> class NewFormatter(TableFormatter):
...     def headers(self, headings):
...         pass
...     def row(self, rowdata):
...         pass
>>> f = NewFormatter()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: Can't instantiate abstract class NewFormatter with abstract methods headings


"""


class Stock:
    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price

    def cost(self):
        return self.shares * self.price

    def sell(self, nshares):
        self.shares -= nshares


# Print a table
def print_table(records, fields, formatter):
    # print(' '.join('%10s' % fieldname for fieldname in fields))
    # print(('-' * 10 + ' ') * len(fields))
    # for record in records:
    #     print(' '.join('%10s' % getattr(record, fieldname) for fieldname in fields))
        if not isinstance(formatter, TableFormatter):
            raise TypeError('Expected a TableFormatter')

        formatter.headings(fields)
        for r in records:
            rowdata = [getattr(r, fieldname) for fieldname in fields]
            formatter.row(rowdata)


class TableFormatter:
    def headings(self, headers):
        raise NotImplementedError()

    def row(self, rowdata):
        raise NotImplementedError()


class TextTableFormatter(TableFormatter):
    def headings(self, headers):
        print(' '.join('%10s' % h for h in headers))
        print(('-' * 10 + ' ') * len(headers))

    def row(self, rowdata):
        print(' '.join('%10s' % d for d in rowdata))


class CSVTableFormatter(TableFormatter):
    def headings(self, headers):
        print(','.join(headers))

    def row(self, rowdata):
        print(','.join(str(d) for d in rowdata))


class HTMLTableFormatter(TableFormatter):
    def headings(self, headers):
        print('<tr>', end=' ')
        for h in headers:
            print('<th>%s</th>' % h, end=' ')
        print('</tr>')

    def row(self, rowdata):
        print('<tr>', end=' ')
        for d in rowdata:
            print('<td>%s</td>' % d, end=' ')
        print('</tr>')


def create_formatter(name):
    if name == 'text':
        formatter_cls = TextTableFormatter
    elif name == 'csv':
        formatter_cls = CSVTableFormatter
    elif name == 'html':
        formatter_cls = HTMLTableFormatter
    else:
        raise RuntimeError('Unknown format %s' % name)
    return formatter_cls()


def print_table_class(records, fields, formatter):
    formatter.headings(fields)
    for r in records:
        rowdata = [getattr(r, fieldname) for fieldname in fields]
        formatter.row(rowdata)
