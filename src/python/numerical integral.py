import math

# A non-rigorous evaluation of c_0, by explicitly $\floor y \rfloor \log(\lceil y/e \rceil / (y/e)) dy/y^2$ on pieces up to some 
# threshold $b$, then using e/2b as an estimate for the remainder.

def integrand(x):
    # floor(x) and ceiling of (e*x)
    return math.floor(x) * math.log(math.ceil(x/math.e) / (x/math.e)) / x**2

def integrand2(x):
    return math.floor(x) * math.log( (6 * math.ceil(x/6 - 1/2) + 3) / x ) / x**2

integral = 0
a = 1
N = 1
M = 1

for i in range(5000):
    if N+1 < math.e * M:
        b = N+1
        N_new = N+1
        M_new = M
    else:
        b = math.e * M
        N_new = N
        M_new = M+1
    integral += N * ((-math.log(M) + math.log(b))/b - (-math.log(M) + math.log(a))/a)
    print(f"After incorporating [{a},{b}], the estimate for $c_0$ is {(integral + math.exp(1)/(2*b))/math.e}.") 
    N = N_new
    M = M_new
    a = b


