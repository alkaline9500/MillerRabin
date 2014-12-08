"""
miller_rabin
The Miller-Rabin Primality Test
"""

__author__ = "Nic Manoogian"

import argparse
import multiprocessing as mp
from random import randint
from miller_rabin import miller_rabin

def prime_or_none(n):
    if miller_rabin(n):
        return n


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Miller-Rabin Primality Test.')
    parser.add_argument('start_value', help='value to begin testing', type=int)
    parser.add_argument('end_value', help='value to end testing (inclusive)', type=int)
    args = parser.parse_args()

    pool = mp.Pool()
    for m in pool.map(prime_or_none, range(args.start_value, args.end_value+1)):
        if m:
            print(m)
