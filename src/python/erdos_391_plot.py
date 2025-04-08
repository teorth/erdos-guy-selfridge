import matplotlib.pyplot as plt
import math

# Code for generating Figure 4 in the original paper.

def is_prime(n):
    """Return True if n is a prime number, else False."""
    if n < 2:
        return False
    # Check divisibility from 2 up to sqrt(n)
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def contrib(N,p):
    if p > N:
        return 0
    if p > N/math.e:
        return math.floor(N/p)*(math.log(p) - math.log(N/math.e))
    if p > N/(2*math.e):
        return math.floor(N/p)*(math.log(2*p) - math.log(N/math.e))
    return 0

def contrib2(N,p):
    if p < N/(math.e) / (math.floor(math.sqrt(N/math.e))):
        return 0
    return math.floor(N/p)*(math.log(p*math.ceil(N/(math.e*p))) - math.log(N/math.e))


def lower(N):
    return sum(contrib(N,p) for p in range(1, N + 1) if is_prime(p))

def lower_alt(N):
    return sum(contrib2(N,p) for p in range(1, N + 1) if is_prime(p))

def upper(N):
    return math.log(2*math.pi*N) + 1/(12*N)

def lower2(N):
    M = N/math.sqrt(2*math.e)
    pi1 = N/math.log(N)*(1+1/math.log(N))
    pi2 = M/math.log(M)*(1+1.2762/math.log(M))
    return (pi1 - pi2) * math.log(math.e/2)

def lower3(N):
    M = N/math.sqrt(2*math.e)
    pi1 = N/math.log(N)
    pi2 = 1.2551 * M/math.log(M)
    return (pi1 - pi2) * math.log(math.e/2)

base = range(80,598)
LHS = [lower(N) for N in base]
LHS_alt = [lower_alt(N) for N in base]
RHS = [upper(N) for N in base]
LHS2 = [lower2(N) for N in base]
LHS3 = [lower3(N) for N in base]

plt.figure(figsize=(8, 6))
plt.plot(base, LHS_alt, label='LHS of (2.4)' )
plt.plot(base, LHS2, label='LHS of (2.5)' )
plt.plot(base, RHS, label='RHS' )
plt.title('Left and right-hand sides of (2.4), (2.5)')
plt.xlabel('$N$')
plt.legend()
plt.grid(True)
plt.show()

