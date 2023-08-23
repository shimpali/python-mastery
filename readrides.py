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
import collections
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


def read_rides_as_dicts_no_class(filename):
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

# readrides.py
...


class RideData(collections.abc.Sequence):
    def __init__(self):
        # Each value is a list with all of the values (a column)
        self.routes = []
        self.dates = []
        self.daytypes = []
        self.numrides = []

    def __len__(self):
        # All lists assumed to have the same length
        return len(self.routes)

    def __getitem__(self, index):
        return {'route': self.routes[index],
                'date': self.dates[index],
                'daytype': self.daytypes[index],
                'rides': self.numrides[index]}

    def append(self, d):
        self.routes.append(d['route'])
        self.dates.append(d['date'])
        self.daytypes.append(d['daytype'])
        self.numrides.append(d['rides'])


def read_rides_as_dicts(filename):
    '''
    Read the bus ride data as a list of dicts
    '''
    records = RideData()  # <--- CHANGE THIS
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


def read_rides_as_instances_with_ntup(filename):
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


def read_rides_as_columns(filename):
    '''
    Read the bus ride data into 4 lists, representing columns
    '''
    routes = []
    dates = []
    daytypes = []
    numrides = []
    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)  # Skip headers
        for row in rows:
            routes.append(row[0])
            dates.append(row[1])
            daytypes.append(row[2])
            numrides.append(int(row[3]))
    return dict(routes=routes, dates=dates, daytypes=daytypes, numrides=numrides)


if __name__ == '__main__':
    import tracemalloc

    tracemalloc.start()
    read_rides = read_rides_as_tuples
    rides = read_rides("Data/ctabus.csv")

    print('Memory Use: Current %d, Peak %d' % tracemalloc.get_traced_memory())

    read_rides2 = read_rides_as_dicts_no_class
    rides2 = read_rides2("Data/ctabus.csv")

    print('Memory Use: Current %d, Peak %d' % tracemalloc.get_traced_memory())

    read_rides3 = read_rides_as_instances_with_ntup
    rides3 = read_rides3("Data/ctabus.csv")

    print('Memory Use: Current %d, Peak %d' % tracemalloc.get_traced_memory())
