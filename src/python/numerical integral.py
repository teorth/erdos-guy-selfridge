import math

# A non-rigorous evaluation of c_0, by explicitly computing $\lfloor y \rfloor \log(\lceil y/e \rceil / (y/e)) dy/y^2$ on pieces up to some 
# threshold $b$, then using e/2b as an estimate for the remainder (the rationale being that for large $y$ one has $\log(\lceil y/e \rceil / (y/e)) \approx \{ y/e\}/(y/e)$, that $\lfloor y \rfloor \approx y$, and $latex \{y/e\}$ is approximately $1/2$ on the average, so that the tail is heuristically $\approx \int_b^\infty y \frac{1}{2} / (y/e) dy/y^2 = e/2b$)

def integrand(x):
    # floor(x) and ceiling of (e*x)
    return math.floor(x) * math.log(math.ceil(x/math.e) / (x/math.e)) / x**2

def integrand2(x):
    return math.floor(x) * math.log( (6 * math.ceil(x/6 - 1/2) + 3) / x ) / x**2

integral = 0
a = 1
N = 1
M = 1

for i in range(500000):
    if N+1 < math.e * M:
        b = N+1
        N_new = N+1
        M_new = M
    else:
        b = math.e * M
        N_new = N
        M_new = M+1
    integral += N * ((-math.log(M) + math.log(b))/b - (-math.log(M) + math.log(a))/a)

    # We can note that the function we are integrating is lower bounded by 0 and upper bounded by e/2 *(1 + 1/(1 + ex))
    print(f"After incorporating [{a},{b}], the estimate for $c_0$ is {(integral + math.exp(1)/(2*b))/math.e}.") 
    print(f"Bounds: [{integral/math.e}, {(integral + (math.exp(1)/b + math.log(1 + math.exp(1)/b))/2)/math.e}]")
    
    N = N_new
    M = M_new
    a = b


