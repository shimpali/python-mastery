"""
>>> import readrides
>>> rows = readrides.read_rides_as_dicts('Data/ctabus2.csv')

1. How many bus routes exist in Chicago?
# >>> total_routes = len(set(map(lambda x: x['route'], rows)))
# >>> print(total_routes)
# 181
#
# 2. How many people rode the number 22 bus on February 2, 2011? What about any route on any date of your choosing?
>>> rows_on_22 = list(filter(lambda x: x['route'] == '22', rows))
>>> print(rows_on_22)
[{'route': '22', 'date': '01/01/2001', 'daytype': 'U', 'rides': 7877}, {'route': '22', 'date': '01/02/2001', 'daytype': 'W', 'rides': 19558}]
>>> print(max(rows_on_22, key=lambda row: row['rides']))
{'route': '22', 'date': '01/02/2001', 'daytype': 'W', 'rides': 19558}


{'route': '22', 'date': '02/02/2011', 'daytype': 'W', 'rides': 5055}
# >>> date_wise_routes = [bus['rides'] for bus in rows if bus['date'] == '02/02/2011' and bus['route'] == '22']
# >>> print(*date_wise_routes)
# 5055

3. What is the total number of rides taken on each bus route?
>>> total_number_of_rides(rows)

"""
from collections import Counter


def total_number_of_rides(rows):
    # total_rides[row['route']] = Counter(rows)[row['route']]
    ride_count = Counter()
    total_rides = dict()
    routes = set(map(lambda x: x['route'], rows))
    # counts = {row['route']: rows.count(row['route']) for row in rows}
    # print(routes)
    # for row in rows:
    for route in routes:
        ride_count[route] = [bus for bus in rows if bus['route'] == route]
        print(ride_count)

    # for row in rows:
    #     all_rows = Counter(rows)
    #     print(all_rows)
    #     if row['route'] in routes:
    #         ride_count['rides'] = Counter(rows)
    #         print(ride_count)
    # print(total_rides)

