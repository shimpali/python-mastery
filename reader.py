"""
>>> import reader
>>> portfolio = read_csv_as_dicts('Data/portfolio.csv', [str,int,float])
>>> for s in portfolio:
...     print(s)
{'name': 'AA', 'shares': 100, 'price': 32.2}
{'name': 'IBM', 'shares': 50, 'price': 91.1}
{'name': 'CAT', 'shares': 150, 'price': 83.44}
{'name': 'MSFT', 'shares': 200, 'price': 51.23}
{'name': 'GE', 'shares': 95, 'price': 40.37}
{'name': 'MSFT', 'shares': 50, 'price': 65.1}
{'name': 'IBM', 'shares': 100, 'price': 70.44}

>>> rows = read_csv_as_dicts('Data/ctabus.csv', [str,str,str,int])
>>> len(rows)
577563
>>> rows[0]
{'route': '3', 'date': '01/01/2001', 'daytype': 'U', 'rides': 7354}

>>> from reader import read_csv_as_instances
>>> from stock import Stock
>>> portfolio = read_csv_as_instances('Data/portfolio.csv', Stock)
>>> portfolio
[<stock.Stock object at 0x11a5e2750>, <stock.Stock object at 0x11a5e27d0>, <stock.Stock object at 0x11a5e28d0>, <stock.Stock object at 0x11a5e2850>, <stock.Stock object at 0x11a5e2990>, <stock.Stock object at 0x11a5e2a50>, <stock.Stock object at 0x11a5e2ad0>]

>>> class Row:
...         def __init__(self, route, date, daytype, numrides):
...             self.route = route
...             self.date = date
...             self.daytype = daytype
...             self.numrides = numrides
...
...         @classmethod
...         def from_row(cls, row):
...             return cls(row[0], row[1], row[2], int(row[3]))
>>> rides = read_csv_as_instances('Data/ctabus.csv', Row)
>>> len(rides)
577563

>>> from reader import DictCSVParser
>>> parser = DictCSVParser([str, int, float])
>>> port = parser.parse('Data/portfolio.csv')

>>> import reader
>>> import stock
>>> port = reader.read_csv_as_instances('Data/portfolio.csv', stock.Stock)

"""

import csv
from abc import ABC, abstractmethod


def read_csv_as_dicts(filename, types):
    """
    Read a CSV file with column type conversion
    """
    records = []
    with open(filename) as f:
        rows = csv.reader(f)
        headers = next(rows)
        for row in rows:
            record = {name: func(val) for name, func, val in zip(headers, types, row)}
            records.append(record)
    return records


def read_csv_as_instances(filename, cls):
    """
    Read a CSV file into a list of instances
    """
    records = []
    with open(filename) as f:
        rows = csv.reader(f)
        headers = next(rows)
        for row in rows:
            records.append(cls.from_row(row))
    return records


class CSVParser(ABC):

    def parse(self, filename):
        records = []
        with open(filename) as f:
            rows = csv.reader(f)
            headers = next(rows)
            for row in rows:
                record = self.make_record(headers, row)
                records.append(record)
        return records

    @abstractmethod
    def make_record(self, headers, row):
        pass


class DictCSVParser(CSVParser):
    def __init__(self, types):
        self.types = types

    def make_record(self, headers, row):
        return { name: func(val) for name, func, val in zip(headers, self.types, row) }


class InstanceCSVParser(CSVParser):
    def __init__(self, cls):
        self.cls = cls

    def make_record(self, headers, row):
        return self.cls.from_row(row)