"""
>>> import readrides
>>> rows = readrides.read_rides_as_dicts('Data/ctabus2.csv')

1. How many bus routes exist in Chicago?
# >>> total_routes = len(set(map(lambda x: x['route'], rows)))
# >>> print(total_routes)
# 181
#
# 2. How many people rode the number 22 bus on February 2, 2011? What about any route on any date of your choosing?
# >>> from collections import Counter
# >>> people_count = Counter()
#
# # >>> people_count['c'] = list(filter(lambda x: x['date'] == '02/02/2011' and x['route'] == '22', rows))
# >>> people_count['count'] = [bus for bus in rows if bus['date'] == '02/02/2011' and bus['route'] == '22'][0]
# >>> print(people_count['count'])
# {'route': '22', 'date': '02/02/2011', 'daytype': 'W', 'rides': 5055}
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
