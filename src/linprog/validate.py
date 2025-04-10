import argparse
from decimal import Decimal
from math import factorial, prod
from typing import Dict, List, Tuple


def sieve(N: int) -> Tuple[Dict[int,int],List[Dict[int,int]]]:
    """Compute prime factorization of N!"""
    c = {}  # prime counts
    f = [{} for _ in range(N+1)]  # factorizations

    w = list(range(N+1))  # work array
    for i in range(2, N+1):
        if w[i] == 1:
            continue
        assert w[i] == i, f"w[{i}] = {w[i]}, i = {i}"
        assert i not in c
        c[i] = 0

        j = i
        while j <= N:
            q, r = divmod(w[j], i)
            if r:
                j += i
            else:
                w[j] = q
                c[i] += 1
                f[j][i] = f[j].setdefault(i, 0) + 1
    assert all(wi==1 for wi in w[1:])
    #print(c)

    # sanity check
    if N <= 1000:
        assert prod(pow(i, ci) for (i, ci) in c.items()) == factorial(N)
        assert prod(prod(pow(p, c) for (p, c) in fi.items()) for fi in f) == factorial(N)

    return (c, f)


def validate(filename, check_num_factors = False):
    with open(filename) as file:
        N, T = (int(x) for x in next(file).split())
        assert (line := next(file).rstrip()) == 'FACTORS', line
        C = []
        for line in file:
            if line.rstrip() == 'CERTIFICATE':
                break
            j, fj = (int(x) for x in line.split())
            C.append((j, fj))
        A = []
        for line in file:
            i, ai = line.split()
            A.append((int(i), Decimal(ai)))
    print(f"number of factors: {sum(ci for (i, ci) in C if i>=T)}")
    if check_num_factors:
        assert sum(ci for (i, ci) in C if i>=T) >= N, f"N = {N}, T = {T}, num factors: {sum(ci for (i, ci) in C if i>=T)}"
    FC, FF = sieve(N)
    # validate factorization
    F = [pow(i, ci) for (i, ci) in C]
    l = len(F)
    while l > 1:
        l, r = divmod(l, 2)
        for j in range(l):
            F[j] = F[2*j]*F[2*j+1]
        if r:
            F[l] = F[2*l]
            l += 1
    #assert F[0] == factorial(N), f"{F[0]}, {factorial(N)}"
    assert F[0] == factorial(N)
    # validate certificate
    print(f"upper bound: {sum(FC[i]*ai for (i, ai) in A)}")
    print("Valid!")


def validate_legacy(filename):
    with open(filename) as file:
        N = int(next(file))
        F = [] 
        for line in file:
            i, fi = (int(x) for x in line.split())
            F.append(pow(i, fi))
        l = len(F)
        while l > 1:
            l, r = divmod(l, 2)
            for i in range(l):
                F[i] = F[2*i]*F[2*i+1]
            if r:
                F[l] = F[2*l]
                l += 1
    #assert F[0] == factorial(N), f"{F[0]}, {factorial(N)}"
    assert F[0] == factorial(N)
    print("Valid!")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            prog='validate',
            description='Validate a factorial factorization.')
    parser.add_argument('file', type=str)
    parser.add_argument('--check-num-factors', action='store_true', help='Assert that the number of factors >= T is at least N')
    parser.add_argument('--legacy', action='store_true')

    args = parser.parse_args()

    if args.legacy:
        validate_legacy(args.file)
    else:
        validate(args.file, args.check_num_factors)
