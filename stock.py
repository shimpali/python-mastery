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
    print(('-'*10 + ' ')*3)
    for s in portfolio2:
        print('%10s %10d %10.2f' % (s.name, s.shares, s.price))


if __name__ == '__main__':
    portfolio = read_portfolio('Data/portfolio.csv')
    print_portfolio(portfolio)
