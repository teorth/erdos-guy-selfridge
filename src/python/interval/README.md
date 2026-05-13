# Interval computations

This directory contains scripts for the interval arithmetic computations used in the paper.

* `interval_constants.py` computes rigorous intervals for the constants
  $c_0$ and $c_1$.

* `interval_computations.py` checks the interval estimates used in the
  proof of the modified approximate factorization bounds.

To reproduce the constants, run the following from the repository root:

```
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r src/python/interval/requirements.txt
MPLCONFIGDIR=/tmp/erdos-guy-selfridge-mpl python src/python/interval/interval_constants.py
```

The final output should include intervals of the following form:

```
c0 = [0.30441901064575277447, 0.30441901109754626598]
c1 = [0.75554808426110209307, 0.75554808757613112213]
```

The `MPLCONFIGDIR` setting is only used to avoid Matplotlib cache warnings
on systems where the default home-directory cache is not writable.
