import numpy as np
import matplotlib.pyplot as plt
import math


# Code to generate Figure 2 of the original paper.

# Initialize empty lists to store the numbers
a = []
b = []


def read_file():
    # Open the file for reading
    with open(".\\tbounds.txt", "r") as file:
        # Read the file line by line
        for line in file:
            # Split the line into parts (assuming numbers are separated by whitespace)
            parts = line.split()
            # Ensure there are at least two numbers on the line
            if len(parts) >= 2:
                # Convert the numbers from strings to integers (or use float() if needed)
                a.append(int(parts[0]))
                b.append(int(parts[1]))



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
        return True


def best_t( N, init ):
    for t in range(init, N+1):
        if criterion(N,t):
            return t-1
    return N



def plot2():
    read_file()
    base = range(80,600)
    alt = [float(math.floor(2*N/7))/N for N in base]
    comparison = [math.exp(-1) for N in base]
    comparison2 = [math.exp(logfac(N) / N)  for N in base]
    third = [1/3 for N in base]
    conj = [(math.exp(-1) - 0.3044 / math.log(max(N,2))) for N in base]
    lower = [b[i]/a[i] for i in range(len(a))]
    upper = [best_t(a[i],b[i])/a[i] for i in range(len(a))]


    plt.figure(figsize=(8, 6))
    plt.plot(base, lower, label='$t(N)/N$ (lower)' )
    plt.plot(base, comparison, linestyle="--", label='$1/e$' )
    plt.plot(base, comparison2, label='$(N!)^{1/N}/N$' )
    plt.plot(base, third, linestyle="--", label='$1/3$' )
    plt.plot(base, conj, linestyle="--", label='$\\frac{1}{e} - c_0/\\log N$' )
    plt.plot(base, alt, label='$\\lfloor 2N/7\\rfloor/N$' )
    plt.plot(base, upper, linestyle=":", label='Lemma 2.1' )
    plt.title('$t(N)/N$')
    plt.xlabel('$N$')
    plt.ylim(0.25,0.4)
    plt.legend()
    plt.grid(True)
    plt.show()

plot2()
