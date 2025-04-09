import matplotlib.pyplot as plt
import math

# Code for plotting fractional gaps of log 3 / log 2, which is useful in accurately upper bounding arbitrary numbers by numbers of the form 2^a 3^b

def largest_fractional_gap(N):
    log_ratio = math.log(3) / math.log(2)
    
    # Compute fractional parts
    frac_parts = [(n * log_ratio) % 1 for n in range(N)]
    
    # Add endpoints 0 and 1
    frac_parts.extend([0.0, 1.0])
    
    # Sort them
    frac_parts.sort()
    
    # Compute gaps between consecutive elements
    gaps = [frac_parts[i+1] - frac_parts[i] for i in range(len(frac_parts)-1)]
    
    # Find the largest gap
    max_gap = max(gaps)

    return max_gap


base = range(1,100)
gaps = [N * largest_fractional_gap(N) for N in base]


plt.figure(figsize=(8, 6))
plt.plot(base, gaps, label='$B \\delta_B$' )
plt.title('$B \\delta_B$ for $1 \\leq B \\leq 1900$')
plt.xlabel('$N$')
plt.legend()
plt.ylim(1,2.7)
plt.grid(True)
plt.show()

