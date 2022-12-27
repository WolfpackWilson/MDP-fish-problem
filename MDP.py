# imports
import numpy as np
from pandas import DataFrame

# digits to round final results
ROUND = 3


def mdp(
    max_inv: int = 12, min_inv: int = 0, 
    max_fish: int = 5, max_T: int = 75,
    sale_price: float = 20, fuel_cost: float = 10, 
    fish_cost: float = 4, holding_cost: float = 1, 
    lost_sales_cost: float = 25, salvage_price: float = 12,
    d: list = [0, 1, 2, 3, 4], pd: list = [0.2, 0.2, 0.2, 0.3, 0.1]
):
    """Performs the Markov Decision Process for the fish problem.

    Parameters
    ----------
    max_inv: int
        The maximum inventory capacity
    min_inv: int
        The minimum inventory capacity
    max_fish: int
        The maximum number of catchable fish
    max_T: int
        The maximum period T
    sale_price: float
        The sale price of the fish
    fuel_cost: float
        The cost of fuel per trip
    fish_cost: float
        The cost of each fish
    holding_cost: float
        The holding cost for a fish
    lost_sales_cost: float
        The lost sales cost for an unserved demand
    salvage_price: float
        The salvage price
    d: list
        The possible demand values
    pd: list
        The probability of each demand
    """

    # initializing arrays
    k_alt = np.zeros(max_inv + 1, dtype=np.int8)
    q = np.zeros((max_inv + 1, max_inv + 1))
    p = np.zeros((max_inv + 1, max_inv + 1, max_inv + 1))
    v = np.zeros((max_inv + 1, max_T + 1))
    dec = np.zeros((max_inv + 1, max_T + 1), dtype=np.int8)
    pi = np.zeros(max_inv + 1)

    for i in range(min_inv, max_inv + 1):
        k_alt[i] = min(max_inv - i, max_fish)
        v[i, 0] = salvage_price * i
        pi[i] = 1 / (max_inv - min_inv + 1)

    # build p and q matrices
    for i in range(min_inv, max_inv + 1):
        for k in range(k_alt[i] + 1):
            fs_ind = k > 0

            for d_, pd_ in zip(d, pd):
                inv_b4_dmd = i + k
                sales = min(inv_b4_dmd, d_)
                ls = d_ - sales
                j = inv_b4_dmd - sales

                p[i, j, k] = p[i, j, k] + pd_
                q[i, k] = q[i, k] + (
                    sale_price * sales - (
                        fs_ind * fuel_cost
                        + fish_cost * k
                        + holding_cost * j
                        + lost_sales_cost * ls
                    )
                ) * pd_

    # optimize the control policy for each period
    best_k = None
    tmp = np.zeros(max_inv + 1)

    for n in range(1, max_T + 1):
        for i in range(min_inv, max_inv + 1):
            best_so_far = -np.inf

            for k in range(k_alt[i] + 1):
                sum_ = q[i, k]

                for j in range(max_inv + 1):
                    sum_ += + p[i, j, k] * v[j, n-1]

                if sum_ > best_so_far:
                    best_so_far = sum_
                    best_k = k

            v[i, n] = best_so_far
            dec[i, n] = best_k

        for i in range(min_inv, max_inv + 1):
            tmp[i] = 0

            for j in range(min_inv, max_inv + 1):
                tmp[i] += pi[j] * p[j, i, dec[j, n]]

        pi = [i for i in tmp]

    # calculate values, decisions, gains matrices
    values = DataFrame(v)
    decisions = DataFrame(dec)

    gains = values.copy()
    for col in range(1, len(values.columns)):
        gains[values.columns[col]] = \
            values[values.columns[col]] - values[values.columns[col - 1]]

    gains[0] = 0

    # get steady states array
    ss = DataFrame(pi, columns=['PI(i)']).round(ROUND).transpose()

    return values.round(ROUND), decisions, gains.round(ROUND), ss


if __name__ == '__main__':
    # define inputs
    max_inv = 12
    min_inv = 0
    max_fish = 5
    max_T = 75

    sale_price = 20
    fuel_cost = 10
    fish_cost = 4
    holding_cost = 1
    lost_sales_cost = 25
    salvage_price = 12

    d = [0, 1, 2, 3, 4]
    pd = [0.2, 0.2, 0.2, 0.3, 0.1]

    # run MDP
    values, decisions, gains, ss = mdp(
        max_inv, min_inv, max_fish, max_T, sale_price, fuel_cost, fish_cost,
        holding_cost, lost_sales_cost, salvage_price, d, pd
    )

    # display results
    print(values)
    print(decisions)
    print(gains)
    print(ss)
