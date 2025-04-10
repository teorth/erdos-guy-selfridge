
import gurobipy as gp
import os.path
from decimal import ROUND_CEILING, Decimal, localcontext
from itertools import pairwise
from math import ceil, factorial, floor, prod
from typing import Dict, List, NamedTuple, Optional


class Problem(NamedTuple):
    """Factorization of N!"""
    N: int  # problem size
    T: int  # threshold
    c: Dict[int,int]  # prime counts
    f: List[Dict[int,int]]  # factorizations


class Factorization(NamedTuple):
    """Large-factor factorization of N!"""
    c: Dict[int,int]  # prime counts
    f: Dict[int,int]  # factor counts
    r: Dict[int,int]  # residual prime counts
    a: Dict[int,int]  # dual variables


def sieve(N: int, T: int) -> Problem:
    """Compute prime factorization of N!

    Parameters
    ----------
    N : int
        Problem parameter

    Returns
    -------
    Problem
        A factorization of N! suitable for constructing a linear program
    """
    c = {}  # prime counts
    f = [{} for _ in range(N+1)]  # factorizations

    w = list(range(N+1))  # work array
    for i in range(2, N+1):
        if w[i] == 1:
            continue
        assert w[i] == i, f"w[{i}] = {w[i]}, i = {i}"
        assert i not in c
        c[i] = 0

        j = i
        while j <= N:
            q, r = divmod(w[j], i)
            if r:
                j += i
            else:
                w[j] = q
                c[i] += 1
                f[j][i] = f[j].setdefault(i, 0) + 1
    assert all(wi==1 for wi in w[1:])
    #print(c)

    # sanity check
    if N <= 1000:
        assert prod(pow(i, ci) for (i, ci) in c.items()) == factorial(N)
        assert prod(prod(pow(p, c) for (p, c) in fi.items()) for fi in f) == factorial(N)

    return Problem(N, T, c, f)



def lpfac(prob: Problem, ilp: bool = False, rigorous: bool = False) -> Optional[Factorization]:
    """Find large factors using linear programming

    Parameters
    ----------
    prob : Problem
        The factorization of N!
    ilp : bool, optional
        Solve optimization problem as integer program. False by default.
    rigorous : bool, optional
        Add additional variables to make the optimal dual multipliers non-decreasing and the
        optimal value a rigorous upper bound. False by default.

    Returns
    -------
    Factorization
        A large-factor factorization, ore None if `rigorous` is true.
    """

    (N, T, c, f) = prob

    mod = gp.Model('lpfac')
    mod.Params.Threads = 1

    # variables
    x = {j: mod.addVar(vtype='C' if not ilp else 'I', name=f"x{j:04d}") for j in range(T, N+1)}
    z = {}
    if rigorous:
        for p, q in pairwise(c.keys()):
            zpq = mod.addVar(vtype='C', name=f"z({p},{q})")
            z.setdefault(p, []).append((-1, zpq))
            z.setdefault(q, []).append(( 1, zpq))

    # constraints
    row = {}
    for (i, ci) in c.items():
        assert ci > 0
        q0, r0 = divmod(T, i)
        if r0:
            q0 += 1
        # print(i, j0, T)
        row[i] = mod.addConstr(sum(f[j][i]*x[j] for j in range(i*q0, N+1, i)) +
                               sum(apq*zpq for (apq, zpq) in z.get(i, [])) <= ci)

    # objective
    mod.setObjective(sum(x.values()), gp.GRB.MAXIMIZE)

    # write model in MPS format
    # mod.write(f"MOD_{N}_{T}.mps")

    # solve problem
    mod.optimize()

    print(f"N = {N}")
    print(f"threshold: {T}")
    if rigorous:
        print(f"optimal objective value: {mod.ObjVal}")
        for (rp, rq) in pairwise(row.values()):
           assert rp.getAttr('pi') <= rq.getAttr('pi')
        return None
    # print LP result
    # for (j, xj) in x.items():
    #    print(f"x[{j}] = {xj.X:7.3f} ({int(xj.X)})")
    # for (i, ri) in row.items():
    #    print(f"π[{i}] = {ri.getAttr('pi'):7.3f} (rhs: {c[i]})")
    #    print(f"r[{i}] = {ri.getAttr('slack'):7.3f} (rhs: {c[i]})")
    # print(f"residual: {divmod(factorial(N), prod(pow(j, int(xj.X)) for (j, xj) in x.items()))}")
    # check dual certificate
    # assert abs((mod.ObjVal-sum(row[i].getAttr('pi')*ci for (i, ci) in c.items()))/mod.ObjVal) < 1e-12
    # for j in range(T, N+1):
    #     assert sum(row[i].getAttr('pi')*fij for (i, fij) in f[j].items()) >= 1, f"f={j}: {sum(row[i].getAttr('pi')*fij for (i, fij) in f[j].items())}"

    # compute factorization
    rc = {i: 0 for i in c.keys()}
    rf = [0]*(N+1)
    for (j, vj) in x.items():
       xj = int(vj.X)  # TODO: beware of rounding errors
       rf[j] = xj
       for i, ci in f[j].items():
           rc[i] += xj*ci
    print(f"number of factors: {sum(rf)}")

    # compute a strictly feasible upper bound
    ub = mod.ObjVal
    sa = {}
    if not ilp:
        with localcontext(rounding=ROUND_CEILING) as _:
            for (i, ri) in row.items():
                sai = round(Decimal(ri.getAttr('pi')), 12)
                if sai == 1:
                    sai = 1
                sa[i] = sai
                # print(f"{i}: {sa[i]} ({ri.getAttr('pi')})")
        sub = sum(sa[i]*ci for (i, ci) in c.items())
        if sub > floor(ub)+1:
            print(f"Failed to compute strict upper bound: ub={ub}, strict ub={sub}")
            for (i, ri) in row.items():
                sa[i] = ri.getAttr('pi')  # simpliy report what we got from the LP solver
        else:
            for j in range(T, N+1):
                assert sum(sa[i]*fij for (i, fij) in f[j].items()) >= 1, f"f={j}: {sum(sa[i]*fij for (i, fij) in f[j].items())}"
            rigorous = all(ap <= aq for (ap, aq) in pairwise(sa.values()))
            print(f"strict upper bound: {sub} ({'not ' if not rigorous else ''}rigorous)")

    res = Factorization(
        {i: rc[i] for i in c.keys() if rc[i] > 0},
        {i: rf[i] for i in range(T, N+1) if rf[i] > 0},
        {i: rri for i in c.keys() if (rri := c[i]-rc[i]) > 0},
        sa,
    )
    if N <= 1000:
        assert prod(prod(pow(p, rfi*c) for (p, c) in f[i].items()) for (i, rfi) in res.f.items()) == prod(pow(i, rci) for (i, rci) in res.c.items())
        assert prod(pow(i, rci) for (i, rci) in res.c.items()) * prod(pow(i, rri) for (i, rri) in res.r.items()) == factorial(N)

    # # header
    # print("                    ", end='')
    # for j in range(T, N+1):
    #     print(f" {j:4d}", end='')
    # print()
    # # x
    # print("                    ", end='')
    # for j in range(T, N+1):
    #     print(f"    *" if x[j].VBasis==0 else '     ', end='')
    # print()
    # print("    a / x           ", end='')
    # for j in range(T, N+1):
    #     if j in x:
    #         print(f" {x[j].X:4.1f}", end='')
    #     else:
    #         print(f"    ·", end='')
    # print("    c")
    # # matrix
    # for (i, ci) in c.items():
    #     print(f"{row[i].getAttr('pi'):.12f} {i:4d}:", end='')
    #     for j in range(T, N+1):
    #         if j//i*i == j:
    #             print(f" {f[j][i]:4d}", end='')
    #         else:
    #             print(f"    ·", end='')
    #     print(f" {ci:4d}")

    return res



def greedy(prob: Problem, fact: Factorization) -> Factorization:
    """Factor the residual of `fact` using a greedy strategy

    Parameters
    ----------
    prob : Problem
        The original problem
    fact : Factorization
        The optimized factorization of `prob`

    Returns
    -------
    Factorization
        Updated factorization including the factors found by the greedy strategy
    """

    (N, T, c, f) = prob
    (fc, ff, fr, _) = fact
    # print([fri for fri in fr.items() if fri[1]>0])

    i = N
    while i > 1:
        if i not in fr or fr[i] == 0:
            i -= 1
            continue
        j = i*ceil(T/i)
        while j <= N and (m := min(floor(fr.get(k, 0)/fjk) for (k, fjk) in f[j].items())) < 1:
            j += i
        if j > N:
            break
        ff[j] = ff.setdefault(j, 0) + m
        for k, fjk in f[j].items():
            fr[k] -= m*fjk
            fc[k] = fc.setdefault(k, 0) + m*fjk
        # print([fri for fri in fr.items() if fri[1]>0])

    if N <= 1000:
        assert prod(pow(i, fci) for (i, fci) in fc.items()) * prod(pow(i, fri) for (i, fri) in fr.items()) == factorial(N)
        assert prod(prod(pow(p, ffi*c) for (p, c) in f[i].items()) for (i, ffi) in ff.items()) == prod(pow(i, fci) for (i, fci) in fc.items())

    # residual factor
    residual = prod(pow(k, ck) for (k, ck) in fr.items() if ck > 0)
    # if residual > N:
    #     print({i: fri for (i, fri) in fr.items() if fri > 0})
    while residual > N:
        # Note: this can happen if the smallest remaining prime is larger than N/T (example case N=337503, T=112501)
        for (p, q) in pairwise(c.keys()):
            if q in fr and fr[q] > 0:
                break
        else:
            break
        j = next((k for k in range(p*ceil(T/p), N//2+1, p) if k in ff and ff[k] > 0))
        # swap prime p and q in factor j and residual
        ff[j] -= 1
        ff[j//p*q] = ff.setdefault(j//p*q, 0) + 1
        fc[p] -= 1
        fc[q] = fc.setdefault(q, 0) + 1
        fr[q] -= 1
        fr[p] = fr.setdefault(p, 0) + 1
        residual = residual//q*p
    # print({i: fri for (i, fri) in fr.items() if fri > 0})
    if residual >= T:
        ff[residual] = ff.setdefault(residual, 0) + 1
        for j, ci in fr.items():
            fr[j] -= ci
            fc[j] = fc.setdefault(j, 0) + ci
        ff[residual] = 1
        residual = 1
        if N <= 1000:
            assert all(fri==0 for fri in fr.values())
            assert prod(pow(i, ci) for (i, ci) in fc.items()) == factorial(N)
            assert prod(prod(pow(p, fj*c) for (p, c) in f[j].items()) for (j, fj) in ff.items()) == prod(pow(i, ci) for (i, ci) in fc.items())

    # assert residual < T, f"residual={residual}, T={T}"

    print(f"factors: {sum(ff.values())}")
    print(f"residual: {residual}")

    return fact



def write_factorization(N: int, T: int, fact: Factorization, filename: str):
    if os.path.isdir(filename):
        filename = f"{filename}/FC_{N}_{T}.txt"
    with open(filename, "w") as file:
        print(f"{N} {T}", file=file)
        print("FACTORS", file=file)
        for i, fi in fact.f.items():
            if fi == 0:
                continue
            print(f"{i} {fi}", file=file)
        residual = prod(pow(i, fri) for (i, fri) in fact.r.items())
        if residual > 1:
            print(f"{residual} 1", file=file)
        print("CERTIFICATE", file=file)
        for i, ai in fact.a.items():
            print(f"{i} {ai}", file=file)



def main(N: int, T: int, rigorous: bool = False, ilp: bool = False, save: str = None):
    prob = sieve(N, T)

    fact = lpfac(prob, ilp, rigorous)
    if fact is None:
        return  # just computing a rigorous LP upper bound

    if not ilp:
        fact = greedy(prob, fact)

    if save:
        write_factorization(N, T, fact, save)



def oeis(N: int, dirname: str = None):

    Tlb = ceil(2*N//7)
    if N == 56:
        Tlb -= 1  # well, well...
    Tub = None

    while Tub is None or Tub-Tlb > 1:

        T = (Tlb+Tub)//2 if Tub else Tlb
        # print(f"*** N={N}, Tlb={Tlb}, Tub={Tub}, T={T}")

        prob = sieve(N, T)

        fact = lpfac(prob, False)

        fNT = greedy(prob, fact)

        nfactors = sum(fNT.f.values())
        if not Tub:
            Tlb = T
            Tub = 2*T
            flb = fNT
        elif nfactors >= N:
            Tlb = T
            flb = fNT
        else:
            Tub = T
            fub = fNT

    assert N <= sum(flb.f.values()), f"N={N}, nfactors={sum(flb.f.values())}"
    assert N <= floor(sum(flb.a[i]*ci for (i, ci) in prob.c.items()))
    assert N > sum(fub.a[i]*ci for (i, ci) in prob.c.items()), f"N={N}, Tlb={Tlb}, Tub={Tub}, ub={sum(fub.a[i]*ci for (i, ci) in prob.c.items())}"
    print(f"T(oeis) = {Tlb}")

    if dirname:
        assert os.path.isdir(dirname)
        write_factorization(N, Tlb, flb, dirname)
        write_factorization(N, Tub, fub, dirname)
        with open(f"{dirname}/a034258.txt", "a") as file:
            print(f"{N} {Tlb}", file=file)



if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
            prog='facfac',
            description='Optimize decomposition of factorials into large factors')
    parser.add_argument('N', type=int)
    parser.add_argument('T', type=int, nargs='?', default=0)
    parser.add_argument('-r','--rigorous', action='store_true')
    parser.add_argument('-s','--save', type=str)
    parser.add_argument('--oeis', action='store_true', help="Optimize threshold instead of number of factors")
    parser.add_argument('--ilp', action='store_true', help='Solve optimization problem as integer program')

    args = parser.parse_args()

    N = args.N
    T = args.T or ceil(2*N/7)

    if not args.oeis:
        main(N, T, args.rigorous, args.ilp, args.save)
    else:
        oeis(N, args.save)

