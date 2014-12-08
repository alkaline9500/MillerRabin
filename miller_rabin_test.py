"""
miller_rabin_test
Tests the accuracy of the Miller-Rabin algorithm
"""

__author__ = "Nic Manoogian"

import argparse

def square_and_multiply(base,exponent,modulus):
    """
    Square-and-multiply
    Returns x**n (mod m)
    """
    binaryExponent = []
    while exponent != 0:
        binaryExponent.append(exponent%2)
        exponent = exponent//2
    result = 1
    binaryExponent.reverse()
    for i in binaryExponent:
        if i == 0:
            result = (result*result) % modulus
        else:
            result = (result*result*base) % modulus
    return result

def miller_rabin(n, a):
    """
    Miller-Rabin Primality Test
    Returns true if n is a (probable) prime
    Returns false if n is a composite number
    """
    s = 0
    d = n - 1
    while d % 2 == 0:
        s = s + 1
        d = d >> 1
    x = square_and_multiply(a, d, n)
    if x != 1 and x + 1 != n:
        for r in range(1, s):
            x = square_and_multiply(x, 2, n)
            if x == 1:
                return False
            elif x == n - 1:
                a = 0
                break
        if a:
            return False
    return True



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Miller-Rabin Accuracy Test.')
    parser.add_argument('primes_filename', help='filename for the primes text file (one prime on each line)')
    parser.add_argument('start_value', help='value to begin testing', type=int)
    parser.add_argument('end_value', help='value to end testing (inclusive)', type=int)
    parser.add_argument('--include-even', dest='evens', action='store_true', help='include even numbers in the computations')
    parser.add_argument('-r', dest='ratio', action='store_true', help='report the ratio for the data')
    parser.add_argument('-t', dest='top_ten', action='store_true', help='report the top 10 numbers with the most errors')
    args = parser.parse_args()

    primes = []
    errors = {}
    number_correct = 0
    number_total = 0

    # Load primes
    for p in open(args.primes_filename):
        primes.append(int(p))

    start_value = args.start_value
    end_value = args.end_value
    skip_by = 2

    # Start on odd unless otherwise specified
    if args.evens:
        skip_by = 1
    else:
        if start_value % 2 == 0:
            start_value -= 1


    # Try all n in the range
    for n in range(start_value, end_value+1, skip_by):
        print(n)
        true_prime = n in primes
        errors[n] = 0
        # Test all values of a for error
        for a in range(2, n-2):
            if miller_rabin(n, a) == true_prime:
                number_correct += 1
            else:
                # Record n-value error 
                errors[n] += 1
            number_total += 1


    if args.ratio:
        ratio = float(number_correct)/float(number_total)
        print("{correct} out of {total} were correct: {ratio}".format(correct=number_correct, total=number_total, ratio=ratio))

    if args.top_ten:
        errorsSorted = sorted(errors, key=errors.get, reverse=True)
        for i in range(0,10):
            k = errorsSorted[i]
            top_ratio = errors[k] / (k-2)
            print("{i}: {key} with {value} errors: {ratio}".format(i=(i+1), key=k, value=errors[k], ratio=top_ratio))

