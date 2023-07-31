"""
>>> calculate_total_cost()
44671.15
"""


def calculate_total_cost():
    with open('Data/portfolio.dat', 'r') as file:
        cost = 0.0
        for line in file:
            columns = line.split()
            no_of_shares = int(columns[1])
            purchase_price = float(columns[2])
            cost += no_of_shares * purchase_price
        return cost
