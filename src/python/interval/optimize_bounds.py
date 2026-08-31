from python.interval.calculations import evaluate
import numpy as np

MIN_A = 160
MAX_A = 200
JUMP_A = 1

MIN_K = 270
MAX_K = 320
JUMP_K = 1

L = 4.5

MIN_N_EXP = 10.0
MAX_N_EXP = 11.1
JUMP_N_EXP = 0.001

best_A = None
best_K = None
best_L = None
best_N_exp = MAX_N_EXP

for A in np.arange(MIN_A, MAX_A, JUMP_A):
    for K in np.arange(MIN_K, MAX_K, JUMP_K):
        for N_EXP in np.arange(MIN_N_EXP, best_N_exp, JUMP_N_EXP)[::-1]:
            N_EXP = np.round(N_EXP, decimals=10)
            N = int(10**N_EXP)
            t = N/3
            try:
                evaluate(t, N, A, K, L)

                if N_EXP < best_N_exp:
                    best_A = A
                    best_K = K
                    best_L = L
                    best_N_exp = N_EXP
                    print(f"New best: N_EXP={N_EXP}, A={A}, K={K}, L={L}")
            except AssertionError:
                # evaluate failed its inequalities — try a smaller N_EXP next.
                break
            except Exception as e:
                # Do not treat programming errors (NameError, TypeError, …) as
                # "no feasible N" — that silently skips the rest of the sweep.
                raise