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

    i = len(P)  # Current prime to examine (we start with the largest prime in the range)
    minm = 0
    t_start = time.time()

    # The algorithm roughly works as follows:
    # 1. Take the largest prime number that we need to factor out (suppose this is called p)
    # 2. Find the smallest number m, such that m * p divides our number, and m * p >= T
    # 3. Factor out m * p and then repeat this algorithm on the resulting number
    while True:
        # If the current prime has an exponent of zero in the factorization, move on to the next-largest prime
        while i > 0 and E.get(i, 0) == 0:
            i -= 1
        if i == 0:
            break

        # Search for the smallest m such that m * p >= T
        m = max(math.ceil(T / P[i-1]), minm)
        while m < T:
            F = factorint(m)

            X = {}  # Dictionary containing the exponents of all prime factors of m that are <= T
            for q, count in F.items():
                if q in pi:
                    X[pi[q]] = count
            X[i] = X.get(i, 0) + 1  # Increment the exponent of the current prime by 1 (essentially changing to m * p from m)
            
            # Check to make sure that m * p can divide our number evenly. If this condition is met, break the loop
            valid_m = True
            for j in X:
                if E.get(j, 0) < X[j]:
                    valid_m = False
                    break
            if valid_m:
                break
            
            m += 1
            if E.get(i,0) >= X.get(i,0):  # On future iterations of the loop, skip every m up to this point 
                minm = m

        # If we have reached our upper limit, then we are done
        if m == T:
            break
        
        # Factor m * p out of our current number
        for j in X:
            E[j] = E.get(j, 0) - X[j]

        L.append(m * P[i-1])

    t_end = time.time()

    # Confirm that all factors in L are at least T
    assert all(n >= T for n in L)
    
    # Confirm that the product of L evenly divides N!
    product_L = 1
    for n in L:
        product_L *= n
        
    factorial_N = math.factorial(N)

    if factorial_N % product_L == 0:
        is_divisible = True
    else:
        is_divisible = False
        
    assert is_divisible

    # Report results
    print(f"Tested N={N} against T={T}")
    print(f"Test ran in {t_end - t_start} seconds")
    if len(L) >= N:  # Report success or failure
        print(f"SUCCESS: factorized {N}! into {len(L)} factors of size >={T}")
    else:
        print(f"FAILURE: factorized {N}! into {len(L)} factors of size >={T}")

solve(300000,100000)