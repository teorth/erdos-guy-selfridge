import numpy as np
import matplotlib.pyplot as plt
import math


# A variant of Figure 3 of the original paper.

new_values = [1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 8, 8, 8, 8, 8, 9, 9, 10, 10, 10, 10, 11, 11, 12, 12, 12, 12, 12, 12, 13, 13, 13, 14, 14, 15, 15, 15, 15, 15, 15, 16, 17, 17, 17, 17, 18, 18, 18, 19, 19, 19, 20, 20, 20, 20, 21, 21, 21, 21, 21, 22, 22, 22, 23, 23, 23, 23, 24, 24, 24, 25, 25, 25, 26, 26, 26, 27, 28, 28, 28, 28, 28, 28, 29, 29, 29, 29, 30, 30, 30, 30, 31, 31, 31, 32, 32, 32, 33, 34, 34, 34, 35, 35, 35, 35, 35, 35, 35, 37, 37, 37, 38, 38, 39, 39, 39, 39, 39, 40, 40, 40, 40, 40, 41, 41, 41, 42, 42, 43, 43, 44, 44, 44, 44, 44, 44, 45, 45, 45, 46, 46, 46, 47, 47, 48, 48, 48, 48, 48, 48, 48, 50, 50, 50, 50, 51, 51, 51, 51, 53, 53, 53, 53, 54, 54, 54, 54, 54, 54, 54, 56, 56, 56, 56, 56, 57, 57, 57, 58, 58, 58, 58, 58, 59, 59, 60, 60, 60, 61, 61, 61, 62, 62, 63, 63, 63, 63, 63, 63, 65, 65, 65, 66, 66, 66, 66, 66, 67, 67, 67, 67, 68, 68, 68, 69, 69, 69, 70, 70, 70, 70, 71, 71, 71, 71, 72, 72, 72, 73, 73, 74, 74, 75, 75, 75, 75, 75, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 79, 79, 80, 80, 80, 80, 80, 81, 82, 82, 83, 83, 83, 84, 84, 84, 84, 84, 84, 85, 85, 86, 86, 86, 87, 87, 88, 88, 88, 88, 88, 88, 88, 88, 89, 90, 90, 91, 91, 91, 91, 92, 92, 92, 93, 93, 93, 93, 93, 93, 94, 94, 94, 95, 95, 95, 96, 97, 98, 98, 98, 98, 99, 99, 99, 99, 99, 101, 101, 101, 102, 102, 102, 102, 103, 103, 104, 104, 104, 104, 104, 104, 104, 106, 106, 106, 106, 107, 107, 108, 108, 108, 108, 109, 109, 109, 110, 110, 110, 111, 111, 111, 111, 112, 112, 112, 112, 112, 112, 113, 113, 115, 115, 115, 115, 116, 116, 116, 116, 117, 117, 117, 117, 117, 117, 117, 117, 118, 119, 120, 120, 120, 120, 120, 121, 122, 122, 122, 123, 123, 123, 124, 124, 124, 124, 125, 125, 125, 125, 126, 126, 127, 127, 128, 128, 128, 128, 129, 129, 130, 130, 130, 130, 130, 131, 131, 131, 132, 132, 133, 133, 133, 134, 134, 134, 134, 135, 135, 135, 135, 135, 135, 135, 137, 137, 137, 138, 138, 138, 138, 139, 139, 139, 140, 140, 141, 141, 141, 141, 142, 142, 142, 142, 143, 143, 143, 143, 143, 144, 144, 144, 145, 145, 146, 146, 146, 147, 148, 148, 148, 149, 149, 149, 150, 150, 150, 150, 150, 150, 151, 151, 152, 152, 153, 153, 153, 154, 154, 154, 154, 154, 154, 154, 155, 155, 155, 155, 155, 157, 157, 157, 158, 158, 159, 159, 159, 159, 160, 160, 160, 160, 160, 160, 163, 163, 164, 164, 164, 165, 165, 165, 165, 165, 165, 165, 165, 165, 166, 166, 167, 167, 168, 168, 168, 168, 169, 170, 170, 170, 171, 171, 171, 171, 171, 172, 172, 172, 172, 172, 173, 173, 174, 174, 174, 174, 176, 176, 176, 177, 177, 177, 178, 178, 178, 179, 179, 180, 180, 180, 180, 180, 180, 180, 181, 181, 182, 182, 183, 183, 183, 184, 184, 184, 184, 184, 185]

greedy_values = [0 for _ in range(600)]


def read_file():
    # Open the file for reading
    with open(".\\tbounds.txt", "r") as file:
        # Read the file line by line
        for line in file:
            # Split the line into parts (assuming numbers are separated by whitespace)
            parts = line.split()
            # Ensure there are at least two numbers on the line
            if len(parts) >= 2:
                greedy_values[int(parts[0])-1] = int(parts[1])



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

    print(new_values)
    print(greedy_values)

    base = range(80,599)
    alt = [float(math.floor(2*N/7))/N for N in base]
    conj = [(math.exp(-1) - 0.3044 / math.log(max(N,2))) for N in base]
    lower = [greedy_values[N]/N for N in base]
    exact = [new_values[N]/N for N in base]
    upper = [best_t(N, new_values[N])/N for N in base]


    plt.figure(figsize=(8, 6))
    plt.plot(base, lower, label='Greedy algorithm (lower)' )
    plt.plot(base, exact, label='$t(N)/N$ (exact)' )
    plt.plot(base, conj, linestyle="--", label='$\\frac{1}{e} - c_0/\\log N$' )
    plt.plot(base, alt, label='$\\lfloor 2N/7\\rfloor/N$' )
    plt.plot(base, upper, linestyle=":", label='Lemma 2.1 (upper)' )
    plt.title('$t(N)/N$')
    plt.xlabel('$N$')
    plt.ylim(0.27,0.32)
    plt.legend()
    plt.grid(True)
    plt.show()

plot2()
