"""
miller_rabin_stats
The Miller-Rabin Primality Test with Statistics
"""

__author__ = "Nic Manoogian"

import argparse
import multiprocessing as mp
from random import randint

class ValueStatus():
    """
    Represents a status for Miller-Rabin to return
    """
    def __init__(self, n, prime, t=None):
        self.n = n
        self.prime = prime
        self.t = t

    def __repr__(self):
        if self.prime:
            return "({n} [P])".format(n=self.n)
        if self.t != None:
            return "({n} [C] t={t})".format(n=self.n, t=self.t)
        return "({n} [C] trivial)".format(n=self.n)


def miller_rabin(n, k=50):
    """
    Miller-Rabin Primality Test
    Returns true if n is a (probable) prime
    Returns false if n is a composite number
    """
    if n < 6:
        return [ValueStatus(n,False), ValueStatus(n,False), ValueStatus(n,True), ValueStatus(n,True), ValueStatus(n,False), ValueStatus(n,True)][n]
    elif n & 1 == 0:
        return ValueStatus(n,False)
    s = 0
    d = n - 1
    while d % 2 == 0:
        s = s + 1
        d = d >> 1
    for t in range(k):
        a = randint(2, n-2)
        x = pow(a, d, n)
        if x == 1 or x == n-1:
            continue
        for _ in range(s-1):
            x = pow(x, 2, n)
            if x == 1:
                return ValueStatus(n,False,t=t)
            elif x == n - 1:
                a = 0
                break
        if a:
            return ValueStatus(n,False,t=t)
    return ValueStatus(n,True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Miller-Rabin Primality Test\n' + 
                                                 'Outputs k values and how many elements were discovered on that witness')
    parser.add_argument('start_value', help='value to begin testing', type=int)
    parser.add_argument('end_value', help='value to end testing (inclusive)', type=int)
    parser.add_argument('-l', '--list-groups', dest="list_groups", action='store_true', help='Lists all elements within each witness group.')
    args = parser.parse_args()

    tvalues = {}
    pool = mp.Pool()
    for m in pool.map(miller_rabin, range(args.start_value, args.end_value+1)):
        if m.t != None:
            if m.t in tvalues:
                tvalues[m.t].append(m)
            else:
                tvalues[m.t] = [m]

    print("k iteration -> number elements discovered")

    for (t, value) in tvalues.items():
        if args.list_groups:
            print("{t} -> {c} : {l}".format(t=t, c=len(value), l=value))
        else:
            print("{t} -> {c}".format(t=t, c=len(value)))
