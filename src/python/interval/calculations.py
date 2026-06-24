import numpy as np
import matplotlib.pyplot as plt
import math


# The code here verifies the calculations in Section 7.  However, it only does so for a single N; I had previously thought that the bounds were monotone in N, but this turns out not to be the case.  As such, this code, while still technically correct, is not usable for clearing out large ranges of N.  I will need to perform a rewrite of the code in interval arithmetic to handle this issue.



# An effective error term in the prime number theorem, see (2.15)
def E(N):
    return 0.95 * math.sqrt(N) + 3.83 * 10**(-9) * N

def is_prime(n):
    """Return True if n is a prime number, else False."""
    if n < 2:
        return False
    # Check divisibility from 2 up to sqrt(n)
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def pi(N):
    """Return the number of primes less than or equal to N."""
    count = 0
    for i in range(2, math.floor(N) + 1):
        if is_prime(i):
            count += 1
    return count

def nu(p,m):
    count = 0
    n = m
    while n % p == 0:
        count += 1
        n //= p
    return count

def coprime_6(n):
    return n%6 == 1 or n%6 == 5

def pi_upper(N):
    assert N > 1, "Error: this bound is only valid for N > 1"
    return N/math.log(N) + 1.2762 * N / (math.log(N) ** 2)

# Upper bound for pi(x)-pi(y), see (2.19)
def pixy_upper(y,x):
    assert N > 1423, "Error: this bound is only valid for N > 1423"
    if y > x:
        return 0
    return (x-y)/math.log(y) + 2 * E(x) / math.log(y)

# Lower bound for pi(x)-pi(y), see (2.20)
def pixy_lower(y,x):
    assert N > 1423, "Error: this bound is only valid for N > 1423"
    if y > x:
        return 0
    return (1-2/math.sqrt(y))*(x-y)/math.log(y) - 2 * E(x) / math.log(x)

# See Table 1
def kappa(L):
    if L >= 341.34:
        return math.log(9/8)
    if L >= 40.5:
        return math.log(32/27)
    if L >= 4.5:
        return math.log(4/3)
    if L >= 4/3:
        return math.log(3/2)
    assert L >= 1, "Error: L must be at least 1"
    return math.log(2)

def fancy_kappa_2(L,gamma):
    assert gamma >= 0, "Error: gamma must be non-negative"
    assert gamma < 1, "Error: gamma must be less than 1"
    return (math.log(12)/(2*(1-gamma)*math.log(2)) - 1) * math.log(12*L) + kappa(L) * math.log(12) / (2*(1-gamma)*math.log(2))

def fancy_kappa_3(L,gamma):
    assert gamma >= 0, "Error: gamma must be non-negative"
    assert gamma < 1, "Error: gamma must be less than 1"
    return (math.log(12)/((1-gamma)*math.log(3)) - 1) * math.log(12*L) + kappa(L) * math.log(12) / ((1-gamma)*math.log(3))

def gamma_2(t,L):
    assert t > 2*L, "Error: t must be greater than 2*L"
    gamma = (2*math.log(2) / math.log(3)) * (math.log(2*L) + kappa(L)) / (math.log(t) - math.log(2*L))
    # print(f"gamma_2: {gamma}")
    return gamma

def gamma_3(t,L):
    assert t > 3*L, "Error: t must be greater than 3*L"
    gamma = (math.log(3) / (2*math.log(2))) * (math.log(3*L) + kappa(L)) / (math.log(t) - math.log(3*L))
    # print(f"gamma_3: {gamma}")
    return gamma

def kappa_starstar(L,gamma2,gamma3):
    kappa = max(fancy_kappa_2(L, gamma2), fancy_kappa_3(L, gamma3))
    # print(f"kappa_**: {kappa}")
    return kappa

def delta_lower(t,N):
    delta = math.log(N/t) - 1
    # print(f"Lower bound on delta: {delta}")
    return delta

# see (8.1)
def sigma_fn(t,N,A):
    sigma = 3*N/(t*A)
    # print(f"sigma: {sigma}")
    return sigma

# see (8.8)
def A_upper(t,N,A,K,sigma,p):
    sum = 0
    for m in range(1, math.floor(K*(1+sigma))+1):
        if coprime_6(m):
            sum += A * nu(p,m) * pixy_upper(t/min(m,K), t*(1+sigma)/m) / N
    return sum

def A_lower(t,N,A,K,sigma,p):
    sum = 0
    for m in range(1, math.floor(K*(1+sigma))+1):
        if coprime_6(m):
            sum += A * nu(p,m) * pixy_lower(t/min(m,K), t*(1+sigma)/m) / N
    return sum

def B_upper(t,N,K,sigma,p):
    sum = 0
    for m in range(1, math.floor(K*(1+sigma))+1):
        if m % p == 0: # this eliminates m=1
            x = t / (m-1)
            k = math.floor(N/x)
            while True:
                next_x = max( N/k, t/m )
                sum += nu(p,m) * pixy_upper(next_x, x) * k / N
                if next_x <= t/m:
                    break
                x = next_x
                k += 1
    return sum

def B_lower(t,N,K,sigma,p):
    sum = 0
    for m in range(1, math.floor(K*(1+sigma))+1):
        if m % p == 0: # this eliminates m=1
            x = t / (m-1)
            k = math.floor(N/x)
            while True:
                next_x = max( N/k, t/m )
                sum += nu(p,m) * pixy_lower(next_x, x) * k / N
                if next_x <= t/m:
                    break
                x = next_x
                k += 1
    return sum


# Total variation of f_alpha on (eps,1]
def total_variation(alpha, eps):
    assert alpha > 1, "Error: alpha must be greater than 1"
    assert eps < 1, "Error: eps must be less than 1"
    assert eps > 0, "Error: eps must be greater than 0"
    var = 0
    x = 1    # current value of x
    val = 0  # current value of f(x)
    n = 1    # current value of \lfloor 1/x \rfloor 
    m = 1    # current value of \lceil 1/ alpha x \rceil
    while True:
        f = n * math.log( m * alpha * x )
        var += abs(f - val)
        val = f
        if 1/(n+1) > 1 / (alpha * m):
            x = 1 / (n+1)
            n += 1
        else:
            x = 1 / (alpha * m)
            m += 1
        if x < eps:
            break
    f = n * math.log( m * alpha * eps )
    var += abs(f - val)
    var += abs(f)
    # print(f"Total variation of f_{alpha} on ({eps},1]: {var}")
    return var

# Integral of f_alpha on (eps,1]
def f_integ(alpha, eps):
    assert alpha > 1, "Error: alpha must be greater than 1"
    assert eps < 1, "Error: eps must be less than 1"
    assert eps > 0, "Error: eps must be greater than 0"
    integral = 0
    x = 1    # current value of x
    n = 1    # current value of \lfloor 1/x \rfloor 
    m = 1    # current value of \lceil 1/ alpha x \rceil
    while True:
        next_n = n
        next_m = m
        if 1/(n+1) > 1 / (alpha * m):
            next_x = max(1 / (n+1), eps)
            next_n += 1
        else:
            next_x = max(1 / (alpha * m), eps)
            next_m += 1
        integral += n * (math.log( m * alpha ) - 1) * ( x - next_x )
        integral += n * (x * math.log(x) - next_x * math.log(next_x))

        if next_x <= eps:
            break
        x = next_x
        n = next_n
        m = next_m

    # print(f"Integral of f_{alpha} from {eps} to 1: {integral}")
    return integral

# Lemma 8.2
def delta1_upper(t,N,A,delta):
    delta1 = 3*N/(2*t*A) + 4/N 
    # print(f"Upper bound on delta_1: {delta1} ({delta1 / delta * 100:.4f}% of delta)")
    return delta1

# (7.7), Lemma 2.2
def delta2_upper(t,N,K,delta):
    delta2 = f_integ(N/t, t/(N*K)) / math.log(t/K)
    delta2 += total_variation(N/t, t/(N*K)) * E(N) / (N * math.log(t/K))
    # print(f"Upper bound on delta_2: {delta2} ({delta2 / delta * 100:.4f}% of delta)")
    return delta2

# Corollary 8.4
def delta3_upper(t,N,A,K,delta):
    delta3 = pi_upper(t/K) + (math.log(N)/math.log(5)) * pi_upper(math.sqrt(N))
    delta3 *= (4*A + 3) * kappa(4.5) / (3 * N)
    # print(f"Upper bound on delta_3: {delta3} ({delta3 / delta * 100:.4f}% of delta)")
    return delta3

# (7.9)
def delta4_upper(t,N,A,K,sigma,delta):
    delta4 = 0
    for p in range(K+1, math.floor(K*(1+sigma))+1):
        if is_prime(p):
            delta4 += kappa(4.5) * A_upper(t,N,A,K,sigma,p)
    # print(f"Upper bound on delta_4: {delta4} ({delta4 / delta * 100:.4f}% of delta)")
    return delta4

# (7.10)
def delta5_upper(t,N,A,K,sigma, delta):
    delta5 = 0
    for p in range(4, K+1):
        if is_prime(p):
            delta5 += kappa(4.5) * max(A_upper(t,N,A,K,sigma,p) - B_lower(t,N,K,sigma,p),0) * math.log(p) / math.log(t/K**2)
            delta5 += kappa(4.5) * max(B_upper(t,N,K,sigma,p) - A_lower(t,N,A,K,sigma,p),0) 
    # print(f"Upper bound on delta_5: {delta5} ({delta5 / delta * 100:.4f}% of delta)")
    return delta5 

# (7.11)
def delta6_upper(N, delta):
    delta6 = kappa(4.5) / N
    # print(f"Upper bound on delta_6: {delta6} ({delta6 / delta * 100:.4f}% of delta)")
    return delta6

# (7.12), (8.4)
def delta7_upper(t,N,K,L, sigma, delta):
    delta7 = kappa(L) / math.log(t) * (math.log(12) / 2 - B_lower(t,N,K,sigma,2) * math.log(2) - B_lower(t,N,K,sigma,3) * math.log(3))
    # print(f"Upper bound on delta_7: {delta7} ({delta7 / delta * 100:.4f}% of delta)")
    return delta7

# (7.13)
def delta8_upper(t,N,L, delta):
    delta8 = 2 * (math.log(t) + kappa(L)) / N
    # print(f"Upper bound on delta_8: {delta8} ({delta8 / delta * 100:.4f}% of delta)")
    return delta8

# (7.15)
def alpha1_upper():
    alpha1 = 0
    # print(f"Upper bound on alpha_1: {alpha1}")
    return alpha1

# (7.16)
def alpha2_upper(t,N,K,sigma, gamma2, gamma3):
    alpha2_2 = (B_upper(t,N,K,sigma,2)-2*gamma2*B_lower(t,N,K,sigma,3)) / (1-gamma2)
    alpha2_3 = (2*B_upper(t,N,K,sigma,3)-gamma3*B_lower(t,N,K,sigma,2)) / (1-gamma3)
    alpha2 = max(alpha2_2, alpha2_3)
    # print(f"Upper bound on alpha_2: {alpha2}")
    return alpha2

# Corollary 8.4
def alpha3_upper(t,N,A,K, kappass):
    alpha3 = 2*(4*A+3)/(3*N*math.log(12))
    alpha3 *= math.log(t/K) + kappass
    alpha3 *= pi_upper(t/K) + (math.log(N)/math.log(5)) * pi_upper(math.sqrt(N))
    # print(f"Upper bound on alpha_3: {alpha3}")
    return alpha3

# (7.18)
def alpha4_upper(t,N,K,sigma, kappass):
    alpha4 = 0
    for p in range(K+1, math.floor(K*(1+sigma))+1):
        if is_prime(p):
            alpha4 += (2/math.log(12)) * (math.log(t/p) + kappass) * A_upper(t,N,A,K,sigma,p)
    # print(f"Upper bound on alpha_4: {alpha4}")
    return alpha4

# (7.19)
def alpha5_upper(t,N,A,K,sigma, kappass):
    alpha5 = 0
    for p in range(4, K+1):
        if is_prime(p):
            alpha5 += (2/math.log(12)) * max(A_upper(t,N,A,K,sigma,p) - B_lower(t,N,K,sigma,p), 0) * (math.log(p)/math.log(t/K**2)) * (math.log(K**2) + kappass)
            alpha5 += (2/math.log(12)) * max(B_upper(t,N,K,sigma,p) - A_lower(t,N,A,K,sigma,p), 0) * (math.log(p) + kappass)
    # print(f"Upper bound on alpha_5: {alpha5}")
    return alpha5

# (7.20)
def alpha6_upper(t,N,kappass):
    alpha6 = (2/math.log(12)) * (kappass + math.log(t)) / N
    # print(f"Upper bound on alpha_6: {alpha6}")
    return alpha6    

# (7.21)
def alpha7_upper(N,gamma2, gamma3):
    alpha7_2 = math.log(2*N) / ((1-gamma2) * N * math.log(2))
    alpha7_3 = 2*math.log(3*N) / ((1-gamma3) * N * math.log(3))
    alpha7 = max(alpha7_2, alpha7_3)
    # print(f"Upper bound on alpha_7: {alpha7}")
    return alpha7


# Check if Proposition 7.1 applies
def evaluate(t, N, A, K, L):
    assert isinstance(N,int), "Error: N must be an integer"
    assert isinstance(A,int), "Error: A must be an integer"
    assert isinstance(K,int), "Error: K must be an integer"
    assert t/K >= math.sqrt(N), "Error: t/K must be at least sqrt(N)"
    assert t/K**2 >= K, "Error: t/K^2 must be at least K"
    assert K >= 5, "Error: K must be at least 5"
    assert t <= N, "Error: t must be less than or equal to N"

    # print(f"Testing Proposition 7.1 for t={t}, N={N}, A={A}, K={K}, L={L}")
    gamma2 = gamma_2(t, L)
    gamma3 = gamma_3(t, L)
    kappass = kappa_starstar(L, gamma2, gamma3)
    sigma = sigma_fn(t, N, A)

    delta = delta_lower(t, N)
    delta1 = delta1_upper(t, N, A, delta)
    delta2 = delta2_upper(t, N, K, delta)
    delta3 = delta3_upper(t, N, A, K, delta)
    delta4 = delta4_upper(t, N, A, K, sigma, delta)
    delta5 = delta5_upper(t, N, A, K, sigma, delta)
    delta6 = delta6_upper(N, delta)
    delta7 = delta7_upper(t, N, K, L, sigma, delta)
    delta8 = delta8_upper(t, N, L, delta)
    delta_sum = delta1 + delta2 + delta3 + delta4 + delta5 + delta6 + delta7 + delta8
    
    alpha1 = alpha1_upper()
    alpha2 = alpha2_upper(t, N, K, sigma, gamma2, gamma3)
    alpha3 = alpha3_upper(t, N, A, K, kappass)
    alpha4 = alpha4_upper(t, N, K, sigma, kappass)
    alpha5 = alpha5_upper(t, N, A, K, sigma, kappass)
    alpha6 = alpha6_upper(t, N, kappass)
    alpha7 = alpha7_upper(N, gamma2, gamma3)
    alpha_sum = alpha1 + alpha2 + alpha3 + alpha4 + alpha5 + alpha6 + alpha7

    # print(f"Delta sum: {delta_sum} ({delta_sum / delta * 100:.4f}% of delta)")
    # print(f"Alpha sum: {alpha_sum}")

    assert delta_sum < delta, "Delta sum exceeds delta"
    assert alpha_sum < 1, "Alpha sum exceeds 1"
    # print("Delta and alpha sums are within bounds!")


A = 189
K = 293
N = int(10**(10.69))
L = 4.5
t = N/3
evaluate(t, N, A, K, L)
