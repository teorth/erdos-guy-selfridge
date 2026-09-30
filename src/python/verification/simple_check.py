#!/usr/bin/env python3

# This program checks that a file containing a putative factorization
# of N! into F factors, each of which is at least M, is correct.

# If no file is provided, it reads from standard input.  If the flag
# "-s" is given, then it checks a subfactorization.

# If the factorization is correct, the program simply prints "N F M".

# The program is designed to be very simple to read so that it's very
# obvious what it does.  A more efficient approach might be to check
# that the prime factors up to N appear the correct number of times.
# It might also be useful in the future to allow for subfactorizations
# of N!.

# The file format is a bunch of whitespace-separated integers.  The
# first three integers are N, F, and M in that order.  Then there
# should be F integers which are the factors themselves, in any order,
# each of which should be at least M.

# Here is an example file for 20! factored as 20 terms, each of which
# is at least 6:

# 20 20 6
# 6 6 6 6 6 6 6 6
# 7 7
# 8 8
# 10 10 10 10
# 11 13 17 19

import gzip
import sys

subfactorization = False
if len(sys.argv) >= 2 and sys.argv[1] == "-s":
    subfactorization = True
    del sys.argv[1]

if len(sys.argv) == 1:
    f = sys.stdin
elif len(sys.argv) == 2:
    filename = sys.argv[1]
    if filename.lower().endswith(".gz"):
        f = gzip.open(filename, "rt")
    else:
        f = open(filename, "r")
else:
    print(f"Usage: {sys.argv[0]} [-s] [filename]")
    sys.exit(1)

integers = [int(x) for x in f.read().split()]

N, F, M, *factors = integers

# Check that there are exactly F factors, or >= F factors for a subfactorization
if subfactorization:
    assert len(factors) >= F, f"Expected >={F} factors, but received {len(factors)} factors instead."
else:
    assert len(factors) == F, f"Expected exactly {F} factors, but received {len(factors)} factors instead."

# Check that each factor is at least M
for factor in factors:
    assert factor >= M, f"Expected each factor to be at least {M}, but received a factor {factor} instead."

# Check that the product of the factors is N!
N_factorial = 1
for i in range(1, N+1):
    N_factorial *= i

putative_factorization = 1
for factor in factors:
    putative_factorization *= factor

if subfactorization:
    assert (N_factorial % putative_factorization) == 0, f"Expected a (sub)factorization of {N}!, but received something else instead."
else:
    assert N_factorial == putative_factorization, f"Expected a factorization of {N}!, but received something else instead."
    # We don't print the numbers in our error message because they might be very big.
        
# Looks correct!
print(N,F,M)
sys.exit(0)
