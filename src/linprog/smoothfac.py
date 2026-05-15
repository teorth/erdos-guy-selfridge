
import gurobipy as gp
import os
from itertools import chain
from typing import Dict, Iterable, List, Optional, Tuple
from math import ceil, floor, prod, sqrt


def coliter(f: List[int], j: int) -> Iterable[Tuple[int,float]]:
    """Iterate prime factors of factor j"""
    while j > 1:
        i = f[j]
        assert i > 1
        fij = 0.0
        while f[j] == i:
            assert (j//i)*i == j
            fij += 1.0
            j = j//i
        yield (i, fij)


def main(N: int, T: int, filename: Optional[str], lp_filename: Optional[str]):

    sqT = ceil(sqrt(T))

    print(f"Solving problem: N = {N}, T = {T}, (√T = {sqT})")

    # allocate memory for factorization
    c: List[float] = [0.0]*(sqT+1)   # prime counts of N! for small primes < sqrt(T)
    f: List[int] = [1]*(N+1)  # factorizations of smooth factors / counts of non-smooth factors

    # f value encoding
    #  - f[j] > 1: j is smooth with largest prime f[j]
    #  - f[j] = 1: j was not visited
    #  - f[j] = 0: j is not smooth
    #  - f[j] < 0: -f[j] is count of non-smooth factor j (selected greedily)

    # sieve smooth factors
    for i in range(2, sqT+1):
        if f[i] != 1:
            continue  # i is not prime
        ci = 0.0
        j = i
        while j <= N:
            f[j] = i # store largest prime factor of j
            fj = j
            while fj > 1:
                q = fj//i
                if q*i != fj:
                    break
                fj = q
                ci += 1.0
            j += i
        c[i] = ci

    # for i in range(2, sqT+1):
    #     if c[i] == 0.0:
    #         continue
    #     print(f"i={i}, c={c[i]}")
    # for j in range(2, N+1):
    #     print(j, f[j])

    # sieve non-smooth factors
    nf_nsmth = 0
    for i in range(sqT+1, N+1):
        if f[i] != 1:
            continue  # i is not prime
        ci = 0.0
        j = i
        while j <= N:
            f[j] = 0 # mark as non-smooth
            fj = j
            while fj > 1:
                q = fj//i
                if q*i != fj:
                    break
                fj = q
                ci += 1.0
            j += i
        # 'greedy complement' of i
        j = int(ceil(T/i))
        assert j <= sqT
        # store factor count (negate to differentiate from smooth factors)
        # f[i] = -int(ci)
        f[i*j] = -int(ci)
        nf_nsmth += int(ci)
        # 'deflate' factors of greedy complement
        while j > 1:
            k = f[j]
            assert k > 1 and (j//k)*k == j
            c[k] -= ci
            assert c[k] >= 0
            j = j//k
    print(f"number of non-smooth factors: {nf_nsmth}")

    # print('--------------')
    # for j in range(2, N+1):
    #     print(j, f[j])

    # write LP constraints to file (column oriented)
    if lp_filename:
        if os.path.isdir(lp_filename):
            lp_filename = f"{lp_filename}/LP_{N}_{T}.txt"
        nrows = sum(1 for i in range(2, sqT+1) if c[i] > 0.0)
        c_idx = [-1]*(sqT+1)
        k = 0
        for i in range(2, sqT+1):
            if c[i] > 0.0:
                c_idx[i] = k
                k += 1
        assert k == nrows
        with open(lp_filename, "w") as file:
            print(f"{N} {T} {nrows}", file=file)
            # write rhs
            print(str.join(' ', (str(int(n)) for n in chain.from_iterable((i, c[i]) for (i, ci) in enumerate(c) if ci > 0.0))), file=file)
            # write columns
            for j in range(T, N+1):
                if f[j] <= 0:
                    continue
                assert f[j] > 1
                print(str.join(' ', (str(int(n)) for n in chain.from_iterable((c_idx[i], fij) for (i, fij) in coliter(f, j)))), file=file)

    # solve LP
    mod = gp.Model('smoothfac')
    mod.Params.Threads = 1
    # constraints
    row = {i: mod.addConstr(0 <= c[i], f"A{i:03d}") for i in range(2, sqT+1) if c[i] > 0.0}
    mod.update()
    for (i, ri) in row.items():
        ri.setAttr('RHS', c[i])
    mod.update()
    # variables
    x = {}
    for j in range(T, N+1):
        if f[j] <= 0:
            continue
        assert f[j] > 1
        cj = gp.Column()
        for (i, fij) in coliter(f, j):
            cj.addTerms(fij, row[i])
        x[j] = mod.addVar(vtype='C', column=cj, name=f"x{j:04d}")
    mod.update()
    # objective
    mod.setObjective(sum(x.values()), gp.GRB.MAXIMIZE)
    # mod.write("smoothfac.mps")
    # solve problem
    mod.optimize()
    # ***DEBUG***
    # print(f"ub = {mod.ObjVal + sum(-f[j] for j in range(T, N+1) if f[j] < 0):.5f} (obj: {mod.ObjVal:.5f})")
    # for i in range(2, sqT+1):
    #     if c[i] == 0.0:
    #         continue
    #     print(f"i={i:2d}: a={row[i].getAttr('pi'):.5f}, c={c[i]}")
    # for j in range(T, T+5*sqT+1):
    #     if f[j] <= 0:
    #         print(f"  {j:4d} {-f[j]:3d}")
    #         continue
    #     print(f"{'*' if x[j].X > 0.0 else '·'} {j:4d} {x[j].X:9.5f}    {str.join(' / ', (str(t) for t in coliter(f, j)))}")
    # ***ENDEBUG***

    upper_bound_lp = mod.ObjVal

    # record counts of LP factors
    sc: Dict[int,int] = {}
    nf_lp = 0
    for (j, vj) in x.items():
        xj = int(vj.X)  # TODO: beware of rounding errors
        if xj == 0:
            continue
        sc[j] = xj
        nf_lp += xj
        # 'deflate' LP factors
        l = j
        while l > 1:
            i = f[l]
            assert i > 1 and (l//i)*i == l, f"j={j}, i={i}, l={l}"
            c[i] -= xj
            assert c[i] >= 0
            l = l//i
    assert sum(sc.values()) == nf_lp
    print(f"number of LP factors: {nf_lp}")

    # greedy
    nf_grdy = 0
    i = sqT
    while i > 1:
        if c[i] == 0.0:
            i -= 1
            continue
        # 'greedy complement' of i
        j = i*int(ceil(T/i))
        while j <= N:
            if f[j] <= 0:
                j += 1
                continue
            m = min(int(floor(c[k]/fkj)) for (k, fkj) in coliter(f, j))
            if m >= 1:
                break
            j += i
        if j > N:
            break
        # record greedy factor
        nf_grdy += m
        sc[j] = sc.setdefault(j, 0) + m
        # 'deflate' LP factors
        while j > 1:
            k = f[j]
            assert k > 1 and (j//k)*k == j, f"j={j}, i={k}"
            c[k] -= m
            assert c[k] >= 0
            j = j//k
    assert sum(sc.values()) == nf_lp + nf_grdy
    print(f"number of greedy factors: {nf_grdy}")
    print(f"total factors: {nf_nsmth+nf_lp+nf_grdy}")

    if filename:
        if os.path.isdir(filename):
            filename = f"{filename}/FC_{N}_{T}.txt"
        for i, sci in sc.items():
            assert f[i] > 1
            f[i] = -sci
        with open(filename, "w") as file:
            print(f"{N} {T}", file=file)
            print("FACTORS", file=file)

            for j in range(T, N+1):
                fj = f[j]
                if fj >= 0:
                    continue
                print(f"{j} {-fj}", file=file)
            residual = prod(pow(i, int(ci)) for (i, ci) in enumerate(c) if ci > 0.0)
            if residual > 1:
                print(f"{residual} 1", file=file)
            print("CERTIFICATE", file=file)
            # TODO

    lower_bound = nf_nsmth+nf_lp+nf_grdy
    upper_bound = nf_nsmth + upper_bound_lp # combine non-smooth factors and upper bound on smooth factors
    print(f"Factor bounds: [{lower_bound}, {upper_bound}]")

    return lower_bound, upper_bound


if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser(
            prog='smoothfac',
            description='Optimize decomposition of factorials into large √T-smooth factors')
    parser.add_argument('N', type=int, help='Problem size')
    parser.add_argument('T', type=int, nargs='?', default=0, help='Threshold. Default: ceil(N/3)')
    parser.add_argument('-s','--save', type=str, metavar='FILENAME')
    parser.add_argument('--write-lp', type=str, metavar='FILENAME')

    args = parser.parse_args()

    N = args.N
    T = args.T or ceil(N/3)

    filename = args.save
    lp_filename = args.write_lp

    main(N, T, filename, lp_filename)
