"""
miller_rabin
The Miller-Rabin Primality Test
"""

__author__ = "Nic Manoogian"

import argparse
from random import randint

def miller_rabin(n, k=50):
    """
    Miller-Rabin Primality Test
    Returns true if n is a (probable) prime
    Returns false if n is a composite number
    """
    if n < 6:
        return [False, False, True, True, False, True][n]
    elif n & 1 == 0:
        return False
    s = 0
    d = n - 1
    while d % 2 == 0:
        s = s + 1
        d = d >> 1
    for _ in range(k):
        a = randint(2, n-2)
        x = pow(a, d, n)
        if x == 1 or x == n-1:
            continue
        for _ in range(s-1):
            x = pow(x, 2, n)
            if x == 1:
                return False
            elif x == n - 1:
                a = 0
                break
        if a:
            return False
    return True



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Miller-Rabin Primality Test.')
    parser.add_argument('start_value', help='value to begin testing', type=int)
    parser.add_argument('end_value', help='value to end testing (inclusive)', type=int)
    args = parser.parse_args()

    for n in range(args.start_value, args.end_value+1):
        if miller_rabin(n):
            print(n)
