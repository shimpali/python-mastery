"""
>>> s = Stock('GOOG', 100, 490.10)
>>> s.name
'GOOG'
>>> s.shares
100
>>> s.price
490.1
>>> s.cost()
49010.0
>>> print('%10s %10d %10.2f' % (s.name, s.shares, s.price))
GOOG
100
490.10
>>> t = Stock('IBM', 50, 91.5)
>>> t.cost()
4575.0
>>> s.shares
100
>>> s.sell(25)
>>> s.shares
75
>>> portfolio = read_portfolio('Data/portfolio.csv')
>>> for s in portfolio:
...     print(s)
<stock.Stock object at 0x10b7fc950>
<stock.Stock object at 0x10b7fc9d0>
<stock.Stock object at 0x10b7fcad0>
<stock.Stock object at 0x10b7fca50>
<stock.Stock object at 0x10b7fcb90>
<stock.Stock object at 0x10b7fcc50>
<stock.Stock object at 0x10b7fccd0>
>>> portfolio1 = read_portfolio('Data/portfolio.csv')
>>> for sh in portfolio1:
...     print('%10s %10d %10.2f' % (sh.name, sh.shares, sh.price))
AA        100      32.20
IBM         50      91.10
CAT        150      83.44
MSFT        200      51.23
GE         95      40.37
MSFT         50      65.10
IBM        100      70.44

(a) Alternate constructors
>>> row = ['AA', '100', '32.20']
>>> st = Stock.from_row(row)
>>> st.name
'AA'
>>> st.shares
100
>>> st.price
32.2
>>> st.cost()
3220.0000000000005

(b) Class variables and inheritance
Class variables such as 'types' below are sometimes used as a customization mechanism when inheritance is used. 
For example, in the Stock class, the types can be easily changed in a subclass. 
Try this example which changes the price attribute to a Decimal instance 
(which is often better suited to financial calculations):

>>> from decimal import Decimal
>>> class DStock(Stock):
...     types = (str, int, Decimal)

>>> row = ['AA', '100', '32.20']
>>> s = DStock.from_row(row)
>>> s.price
Decimal('32.20')
>>> s.cost()
Decimal('3220.00')

>>> s = Stock('GOOG', 100, 490.1)
>>> s.cost_prop    # Property. Computes the cost
49010.0

(c) Enforcing Validation Rules
>>> stc = StockTypeCheck('GOOG', 100, 490.10)
>>> stc.shares = 50          # OK
>>> stc.shares = '50'
Traceback (most recent call last):
...
TypeError: Expected integer
>>> stc.shares = -10
Traceback (most recent call last):
...
ValueError: shares must be >= 0

>>> stc.price = 123.45       # OK
>>> stc.price = '123.45'
Traceback (most recent call last):
...
TypeError: Expected float
>>> stc.price = -10.0
Traceback (most recent call last):
...
ValueError: price must be >= 0

(d) Adding __slots__

>>> s3 = Stock('GOOG', 100, 490.10)
>>> s3.spam = 42
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'Stock' object has no attribute 'spam'

(e) Reconciling Types
>>> from decimal import Decimal
>>> class DStock(Stock):
...     _types = (str, int, Decimal)
>>> sd = DStock('AA', 50, Decimal('91.1'))
>>> sd.price = 92.3
Traceback (most recent call last):
...
TypeError: Expected a Decimal

>>> goog = Stock('GOOG', 100, 490.10)
>>> goog
Stock('GOOG', 100, 490.1)

>>> import stock, reader
>>> portfolio_1 = reader.read_csv_as_instances('Data/portfolio.csv', stock.Stock)
>>> portfolio_1
[Stock('AA', 100, 32.2), Stock('IBM', 50, 91.1), Stock('CAT', 150, 83.44), Stock('MSFT', 200, 51.23), Stock('GE', 95, 40.37), Stock('MSFT', 50, 65.1), Stock('IBM', 100, 70.44)]

>>> a = Stock('GOOG', 100, 490.1)
>>> b = Stock('GOOG', 100, 490.1)
>>> a == b
True

This context manager works by making a temporary patch to sys.stdout to cause all output to redirect to a different file. On exit, the patch is reverted.
>>> import sys
>>> class redirect_stdout:
...        def __init__(self, out_file):
...            self.out_file = out_file
...        def __enter__(self):
...            self.stdout = sys.stdout
...            sys.stdout = self.out_file
...            return self.out_file
...        def __exit__(self, ty, val, tb):
...            sys.stdout = self.stdout

>>> from tableformat import create_formatter, print_table_class
>>> formatter = create_formatter('text')
>>> with redirect_stdout(open('out.txt', 'w')) as file:
...        print_table_class(portfolio, ['name','shares','price'], formatter)
...        file.close()
>>> # Inspect the file
>>> print(open('out.txt').read())
      name     shares      price
---------- ---------- ----------
        AA        100       32.2
       IBM         50       91.1
       CAT        150      83.44
      MSFT        200      51.23
        GE         95      40.37
      MSFT         50       65.1
       IBM        100      70.44
"""
import tableformat


class Stock:
    __slots__ = ('name', 'shares', 'price')
    _types = (str, int, float)

    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price

    def cost(self):
        return self.shares * self.price

    @property
    def cost_prop(self):
        return self.shares * self.price

    def sell(self, nshares):
        self.shares -= nshares

    @classmethod
    def from_row(cls, row):
        values = [func(val) for func, val in zip(cls._types, row)]
        return cls(*values)

    def __repr__(self):
        # Note: The !r format code produces the repr() string
        return f'{type(self).__name__}({self.name!r}, {self.shares!r}, {self.price!r})'

    def __eq__(self, other):
        return isinstance(other, Stock) and ((self.name, self.shares, self.price) ==
                                             (other.name, other.shares, other.price))


def read_portfolio(filename):
    """
    Read a CSV file of stock data into a list of Stocks
    """
    import csv
    portfolio = []
    with open(filename) as f:
        rows = csv.reader(f)
        headers = next(rows)
        for row in rows:
            record = Stock(row[0], int(row[1]), float(row[2]))
            portfolio.append(record)
    return portfolio


def print_portfolio(portfolio2):
    """
    Make a nicely formatted table showing stock data
    """
    print('%10s %10s %10s' % ('name', 'shares', 'price'))
    print(('-' * 10 + ' ') * 3)
    for s in portfolio2:
        print('%10s %10d %10.2f' % (s.name, s.shares, s.price))


class StockTypeCheck:
    _types = (str, int, float)

    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price

    @classmethod
    def from_row(cls, row):
        values = [func(val) for func, val in zip(cls._types, row)]
        return cls(*values)

    @property
    def shares(self):
        return self._shares

    @shares.setter
    def shares(self, value):
        if not isinstance(value, int):
            raise TypeError('Expected an integer')
        if value < 0:
            raise ValueError('shares must be >= 0')
        self._shares = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, float):
            raise TypeError('Expected a float')
        if value < 0:
            raise ValueError('price must be >= 0')
        self._price = value

    @property
    def cost(self):
        return self.shares * self.price

    def sell(self, nshares):
        self.shares -= nshares


if __name__ == '__main__':
    portfolio = read_portfolio('Data/portfolio.csv')
    print_portfolio(portfolio)
