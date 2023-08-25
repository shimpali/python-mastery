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
"""
import csv


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
