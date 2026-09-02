import math
from sympy import primerange
import sys

def main(P: int, N: int, T: int, simple_check: bool = False):
    primes = list(primerange(2, P+1))
    budget = {p: 0 for p in primes}

    divided_factors = []
    for i in range(1, N+1):
        t = i
        # Divide out the small primes
        for p in primes:
            while (t % p) == 0:
                t //= p
                budget[p] += 1
        divided_factors.append(t)

    divided_factors.sort()

    # Verify header of lp_solve solution
    line = sys.stdin.readline()
    assert line == "\n", f"Unexpected line (expected empty line): {line!r}"
    line = sys.stdin.readline()
    assert line.startswith("Value of objective function: "), f"Unexpected line (expected \"Value ...\"): {line!r}"
    line = sys.stdin.readline()
    assert line == "\n", f"Unexpected line (expected empty line): {line!r}"    
    line = sys.stdin.readline()
    assert line == "Actual values of the variables:\n", f"Unexpected line (expected \"Actual values ...\"): {line!r}"

    # Reconstruct factors to multiply by
    multiply_factors = []
    for line in sys.stdin:
        variable, value = line.split()
        assert variable.startswith("a")
        n = int(variable[1:])
        value = int(value)
        t = n
        for p in primes:
            while (t % p) == 0:
                t //= p
                budget[p] -= value
        assert t == 1, f"Variable {variable} which corresponds to n={n} was not {P}-smooth!"
        for i in range(value):
            multiply_factors.append(n)
    multiply_factors.sort(reverse=True)

    # Check prime budgets
    for p in primes:
        assert budget[p] >= 0, f"Prime budget exhausted for prime {p}."

    assert len(divided_factors) == len(multiply_factors), f"Unexpected number of factors."
    factors = [divided_factor * multiply_factor for divided_factor, multiply_factor in zip(divided_factors, multiply_factors)]
    for factor in factors:
        assert factor >= T, f"The resulting factor {factor} should have been at least {T}."
    if simple_check:
        print(N, N, T)
        for factor in factors:
            print(factor)
    else:
        print(P, N, T)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
            prog='rearrange_lp_sol',
            description='Rearrange small prime factors from the lp_solve solution of a rearrange_lp problem.')
    parser.add_argument('P', type=int)
    parser.add_argument('N', type=int)
    parser.add_argument('T', type=int, nargs='?', default=0)
    parser.add_argument('--simple_check', action='store_true', help='Output file for simple_check.py to check.')

    args = parser.parse_args()

    P = args.P
    N = args.N
    T = args.T or math.ceil(N/4)

    main(P, N, T, args.simple_check)
