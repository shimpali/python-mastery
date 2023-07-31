"""
>>> portfolio_cost('Data/portfolio.dat')
44671.15
>>> portfolio_cost('Data/portfolio2.dat')
19908.75
>>> portfolio_cost('Data/portfolio3.dat')
Couldn't parse line:  'C - 53.08\n'
Because there is an  invalid literal for int() with base 10: '-'
Couldn't parse line:  'DIS - N/A\n'
Because there is an  invalid literal for int() with base 10: '-'
Couldn't parse line:  'GE - 37.23\n'
Because there is an  invalid literal for int() with base 10: '-'
Couldn't parse line:  'INTC - 21.84\n'
Because there is an  invalid literal for int() with base 10: '-'
Couldn't parse line:  'MCD - 51.11\n'
Because there is an  invalid literal for int() with base 10: '-'
Couldn't parse line:  'MO - 70.09\n'
Because there is an  invalid literal for int() with base 10: '-'
Couldn't parse line:  'PFE - 26.40\n'
Because there is an  invalid literal for int() with base 10: '-'
Couldn't parse line:  'VZ - 42.92\n'
Because there is an  invalid literal for int() with base 10: '-'
12597.479999999998

"""


def portfolio_cost(filename):
    with open(filename, 'r') as file:
        cost = 0.0
        for line in file:
            columns = line.split()
            try:
                no_of_shares = int(columns[1])
                purchase_price = float(columns[2])
                cost += no_of_shares * purchase_price
            except ValueError as e:
                print("Couldn't parse line: ", repr(line))
                print("Because there is an ", e)
        return cost


print(portfolio_cost('Data/portfolio.dat'))