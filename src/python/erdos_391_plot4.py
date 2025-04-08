import numpy as np
import matplotlib.pyplot as plt
import math

# code for generating Figure 1 in the original paper

def plot3():
    L = 5000
    base = [i/L for i in range(1, L+1)]
    fn = [math.floor(L/i) * math.log(math.e * i/L * math.ceil(L/(math.e*i))) / math.e for i in range(1,L+1)]
    compare = [0.3044 for i in range(1,L+1)]
    basetrunc = [i/L for i in range(math.ceil(L/math.sqrt(2*math.e)), L+1)]
    trunccompare = [math.log(math.e/2)/math.e for _ in range(math.ceil(L/math.sqrt(2*math.e)), L+1)]
    plt.figure(figsize=(8, 6))
    plt.plot(base, fn, label='$\\frac{1}{e} \\lfloor \\frac{1}{x} \\rfloor \\log(ex \\lceil \\frac{1}{ex} \\rceil)$' )
    plt.plot(base, compare, label='$c_0$' )
    plt.plot(basetrunc, trunccompare, label='$\\frac{1}{e} \\log(e/2)$' )
    plt.title('$\\frac{1}{e} \\lfloor \\frac{1}{x} \\rfloor \\log(ex \\lceil \\frac{1}{ex} \\rceil)$')
    plt.xlabel('$x$')
    plt.legend()
    plt.grid(True)
    plt.show()

plot3()
