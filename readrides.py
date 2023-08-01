"""
>>> f = open('Data/ctabus.csv')
>>> next(f)
'route,date,daytype,rides\n'
>>> next(f)
'3,01/01/2001,U,7354'
>>> next(f)
'4,01/01/2001,U,9288'
>>> # --- RESTART
>>> import tracemalloc
>>> f = open('Data/ctabus.csv')
>>> tracemalloc.start()
>>> data = f.read()
>>> len(data)
12361039
>>> current, peak = tracemalloc.get_traced_memory()
>>> current
12362055
>>> peak
24722774
>>> # --- RESTART
>>> f2 = open('Data/ctabus.csv')
>>> lines2 = f2.readlines()
>>> len(lines2)
577564
>>> current, peak = tracemalloc.get_traced_memory()
>>> current
57718057
>>> peak
57730392
>>>
"""

import csv


def read_rides_as_tuples(filename):
    '''
    Read the bus ride data as a list of tuples
    '''
    records = []
    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)  # Skip headers
        for row in rows:
            route = row[0]
            date = row[1]
            daytype = row[2]
            rides = int(row[3])
            record = (route, date, daytype, rides)
            records.append(record)
    return records


def read_rides_as_dicts(filename):
    '''
    Read the bus ride data as a list of dicts
    '''
    records = []
    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)  # Skip headers
        for row in rows:
            route = row[0]
            date = row[1]
            daytype = row[2]
            rides = int(row[3])
            record = {
                'route': route,
                'date': date,
                'daytype': daytype,
                'rides': rides
            }
            records.append(record)
    return records


# class Row:
#     # Uncomment to see effect of slots
#     __slots__ = ('route', 'date', 'daytype', 'rides')
#
#     def __init__(self, route, date, daytype, rides):
#         self.route = route
#         self.date = date
#         self.daytype = daytype
#         self.rides = rides


# Uncomment to use a namedtuple instead
from collections import namedtuple

Row = namedtuple('Row', ('route', 'date', 'daytype', 'rides'))


def read_rides_as_instances(filename):
    '''
    Read the bus ride data as a list of instances
    '''
    records = []
    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)  # Skip headers
        for row in rows:
            route = row[0]
            date = row[1]
            daytype = row[2]
            rides = int(row[3])
            record = Row(route, date, daytype, rides)
            records.append(record)
    return records


if __name__ == '__main__':
    import tracemalloc

    tracemalloc.start()
    read_rides = read_rides_as_tuples
    rides = read_rides("Data/ctabus.csv")

    print('Memory Use: Current %d, Peak %d' % tracemalloc.get_traced_memory())

    read_rides2 = read_rides_as_dicts
    rides2 = read_rides2("Data/ctabus.csv")

    print('Memory Use: Current %d, Peak %d' % tracemalloc.get_traced_memory())

    read_rides3 = read_rides_as_instances
    rides3 = read_rides3("Data/ctabus.csv")

    print('Memory Use: Current %d, Peak %d' % tracemalloc.get_traced_memory())
