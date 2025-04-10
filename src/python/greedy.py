import math
import sympy
from sympy.ntheory import factorint
import time

# A greedy algorithm to factorize, adapted from Maple code of Andrew Sutherland. (Thanks to Adam Wagner for help with the code conversion to Python.)

def solve(N,T):
    P = list(sympy.primerange(1, T))
    pi = {p: i+1 for i, p in enumerate(P)}  # Use dictionary for mapping primes to indices
    
    E = {}  # Use dictionary to store exponents of primes in N!

    # For each prime, count its exponent in the factorization of N! by examining the prime exponents one at a time. For example, for 20! and p = 2,
    # we would note that 20 // 2 = 10, 20 // 4 = 5, 20 // 8 = 2, and 20 // 16 = 1, so there must be 10+5+2+1 = 18 factors
    for p in P:
        exponent = 0
        for i in range(1, int(math.log(N, p)) + 1):
            exponent += N // (p**i)
        E[pi[p]] = exponent

    L = []  # Use list to store all factors
    for p in sympy.primerange(T, N + 1):  # All primes of size >= T can be directly added to the factorization
        L.extend([p] * (N // p))

    i = len(P)  # Number of primes in the range
    minm = 0
    t_start = time.time()

    while True:
        while i > 0 and E.get(i, 0) == 0:
            i -= 1
        if i == 0:
            break

        m = max(math.ceil(T / P[i-1]), minm)
        while m < T:
            F = factorint(m)
            X = {}
            for q, count in F.items():
                if q in pi:
                    X[pi[q]] = count
            X[i] = X.get(i, 0) + 1
            
            valid_m = True
            for j in X:
                if E.get(j, 0) < X[j]:
                    valid_m = False
                    break
            if valid_m:
                break
            
            m += 1
            if E.get(i,0) >= X.get(i,0):
                minm = m

        if m == T:
            break
        
        for j in X:
            E[j] = E.get(j, 0) - X[j]

        L.append(m * P[i-1])

    t_end = time.time()

    assert all(n >= T for n in L)
    
    product_L = 1
    for n in L:
        product_L *= n
        
    factorial_N = math.factorial(N)

    if factorial_N % product_L == 0:
        is_divisible = True
    else:
        is_divisible = False
        
    assert is_divisible

    print(f"Tested N={N} against T={T}")
    print(f"Test ran in {t_end - t_start} seconds")
    if len(L) >= N:  # Report success or failure
        print(f"SUCCESS: factorized {N}! into {len(L)} factors of size >={T}")
    else:
        print(f"FAILURE: factorized {N}! into {len(L)} factors of size >={T}")

solve(300000,100000)