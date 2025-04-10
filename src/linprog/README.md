# facfac

This repository contains code to optimize the decomposition of factorials into large factors
using linear programming.


## Getting Started

Preparation
```
cd src/linprog/
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

Run the code for N=207 and save the result in file `FC_207.txt`
```
python facfac.py --save=FC_207.txt 207
```

Validate the result
```
python validate.py FC_207.txt
```

Note that this code uses Gurobi for solving the linear programs and the default size-restricted
license allows solving problems up to around N=1000. For larger problem sizes, you need to request
an academic license.


## OEIS A034258

Compute the OEIS A034258 numbers for n=20,..,600:
```bash
for N in $(seq 20 154); do python facfac.py $N --oeis --save=../../Data/oeis_results/; if [ $? -ne 0 ]; then break; fi done
for N in $(seq 156 600); do python facfac.py $N --oeis --save=../../Data/oeis_results/; if [ $? -ne 0 ]; then break; fi done
```
This skips N=155, for which the LP heuristic fails to find an upper bound that establishes T(155) < 46.

Validating results:
```bash
for N in $(seq 20 600); do echo $N; F=(./oeis_results/FC_${N}_*.txt); python validate.py --check-num-factors ${F[0]}; if [ $? -ne 0 ]; then break; fi; python validate.py ${F[1]}; done
```
Note: this quick hack fails for instances where T+1 comes lexicographically before T, e.g. T=9, T+1=10.


## References

 - Publication: Terence Tao, Decomposing a factorial into large factors, 2025, https://arxiv.org/abs/2503.20170
 - Blog post: https://terrytao.wordpress.com/2025/03/26/decomposing-a-factorial-into-large-factors/

