import numpy as np
import matplotlib.pyplot as plt
import math
from sympy.ntheory import factorint

# Code for generating Figure 2 in the original paper.


inv_values = [1, 4, 9, 14, 16, 20, 24, 27, 32, 34, 38, 40, 46, 49, 51, 57, 58, 62, 65, 68, 72, 77, 80, 84, 87, 90, 93, 94, 100, 104, 108, 111, 114, 115, 118, 125, 125, 128, 130, 135, 140, 143, 145, 147, 153, 156, 159, 161, 168, 168, 172, 176, 176, 180, 187, 187, 192, 195, 200]

values = [0 for _ in range(200)]

for i in range(200):
    t = 0
    for j in inv_values:
        if j <= i+1:
            t += 1
    values[i] = t

print(values)


def is_prime(n):
    """Return True if n is a prime number, else False."""
    if n < 2:
        return False
    # Check divisibility from 2 up to sqrt(n)
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def logfac(N):
    sum = 0
    for i in range(1, N+1):
        sum += math.log(i)
    return sum

# Test if  \sum_{p > \frac{t}{\sqrt{t}+1}} \left\lfloor \frac{N}{p} \right\rfloor \log \left( \frac{p}{t} \left\lceil \frac{t}{p} \right\rceil \right) > \log N! - N \log t

def criterion( N, t ):
    sum = 0
    for p in range(1, N + 1):
        if is_prime(p) and p > t/(math.floor(math.sqrt(t))):
            sum += math.floor(N/p) * math.log((p/t)*math.ceil(t/p))
        
    if sum > logfac(N) - N * math.log(t) + 0.0001:
#        print(f"N={N}, t={t}, sum={sum}, RHS={logfac(N) - N * math.log(t)}")
        return True


def best_t( N, init ):
    for t in range(init, N+1):
        if criterion(N,t):
            return t-1
    return N


def plot1():
    norm = [values[i]/(i+1) for i in range(len(values))]
    base = [i+1 for i in range(len(values))]
    alt = [float(math.floor(2*(i+1)/7))/(i+1) for i in range(len(values))]
    comparison = [math.exp(-1) for _ in range(len(values))]
    comparison2 = [math.exp(logfac((i+1)) / (i+1)) / (i+1) for i in range(len(values))]
    third = [1/3 for _ in range(len(values))]
    conj = [math.exp(-1) - 0.3044 / math.log(max(i+1,2)) for i in range(len(values))]
    upper = [best_t(i+1, values[i])/(i+1) for i in range(len(values))]

    plt.figure(figsize=(8, 6))
    plt.plot(base, norm, label='$t(N)/N$' )
    plt.plot(base, comparison, linestyle="--", label='$1/e$' )
    plt.plot(base, comparison2, label='$(N!)^{1/N}/N$' )
    plt.plot(base, third, linestyle="--", label='$1/3$' )
    plt.plot(base, conj, linestyle="--", label='$1/e - c_0/\\log N$' )
    plt.plot(base, alt, label='$\\lfloor 2N/7\\rfloor / N$' )
    plt.plot(base, upper, linestyle=":", label='Lemma 2.1' )
    plt.title('$t(N)/N$')
    plt.xlabel('$N$')
    plt.ylim(0.2,0.5)
    plt.xlim(1,200)
    plt.legend()
    plt.grid(True)
    plt.show()

plot1()
