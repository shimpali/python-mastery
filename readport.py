"""
>>> portfolio = read_portfolio('Data/portfolio.csv')
>>> from pprint import pprint
>>> pprint(portfolio)
[{'name': 'AA', 'price': 32.2, 'shares': 100},
 {'name': 'IBM', 'price': 91.1, 'shares': 50},
 {'name': 'CAT', 'price': 83.44, 'shares': 150},
 {'name': 'MSFT', 'price': 51.23, 'shares': 200},
 {'name': 'GE', 'price': 40.37, 'shares': 95},
 {'name': 'MSFT', 'price': 65.1, 'shares': 50},
 {'name': 'IBM', 'price': 70.44, 'shares': 100}]
>>> # Find all holdings more than 100 shares
>>> [s for s in portfolio if s['shares'] > 100]
[{'name': 'CAT', 'shares': 150, 'price': 83.44}, {'name': 'MSFT', 'shares': 200, 'price': 51.23}]

>>> # Compute total cost (shares * price)
>>> sum([s['shares']*s['price'] for s in portfolio])
44671.15
>>>

>>> # Find all unique stock names (set)
>>> { s['name'] for s in portfolio }
{'MSFT', 'IBM', 'AA', 'GE', 'CAT'}
>>>

>>> # Count the total shares of each of stock
>>> totals = { s['name']: 0 for s in portfolio }
>>> for s in portfolio:
...     totals[s['name']] += s['shares']

>>> totals
{'AA': 100, 'IBM': 150, 'CAT': 150, 'MSFT': 250, 'GE': 95}

>>> from collections import Counter
>>> totals = Counter()
>>> for s in portfolio:
...     totals[s['name']] += s['shares']

>>> totals
Counter({'MSFT': 250, 'IBM': 150, 'CAT': 150, 'AA': 100, 'GE': 95})

>>> # Get the two most common holdings
>>> totals.most_common(2)
[('MSFT', 250), ('IBM', 150)]
>>>

>>> # Adding counters together
>>> more = Counter()
>>> more['IBM'] = 75
>>> more['AA'] = 200
>>> more['ACME'] = 30
>>> more
Counter({'AA': 200, 'IBM': 75, 'ACME': 30})
>>> totals
Counter({'MSFT': 250, 'IBM': 150, 'CAT': 150, 'AA': 100, 'GE': 95})
>>> totals + more
Counter({'AA': 300, 'MSFT': 250, 'IBM': 225, 'CAT': 150, 'GE': 95, 'ACME': 30})

>>> from collections import defaultdict
>>> byname = defaultdict(list)
>>> for s in portfolio:
...     byname[s['name']].append(s)

>>> byname['IBM']
[{'name': 'IBM', 'shares': 50, 'price': 91.1}, {'name': 'IBM', 'shares': 100, 'price': 70.44}]
>>> byname['AA']
[{'name': 'AA', 'shares': 100, 'price': 32.2}]

"""

import csv


# A function that reads a file into a list of dicts
def read_portfolio(filename):
    portfolio = []
    with open(filename) as f:
        rows = csv.reader(f)
        headers = next(rows)
        for row in rows:
            record = {
                'name': row[0],
                'shares': int(row[1]),
                'price': float(row[2])
            }
            portfolio.append(record)
    return portfolio
