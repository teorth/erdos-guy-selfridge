# erdos-guy-selfridge

For a natural number $N$, let $t(N)$ be the largest number such that $N!$ can be factored into $N$ integer factors, each of which is at least $t(N)$.  It is known that $t(N) = N/e + o(N)$ as $N \to \infty$, answering a question of [Erdős and Graham](https://www.erdosproblems.com/391); see [this paper](https://arxiv.org/abs/2503.20170).  This repository records the efforts to verify the [Guy-Selfridge conjectures](https://zbmath.org/0918.11013):

1. $t(N) \geq \lfloor 2N/7 \rfloor$ for all $N \neq 56$.
2. $t(N) \geq N/3$ for all $N \geq 3 \times 10^5$.  How small can the lower threshold $3 \times 10^5$ be?

A secondary goal is

3.  Extend the values of $t(N)$ reported in the OEIS (which currently [go up to $N \leq 79$](https://oeis.org/A034258/b034258.txt)).

## Current status

1. Conjecture 1 has been reduced to Conjecture 2.
2. Conjecture 2 is known in the range $8 \times 10^4 \leq N \leq 10^9$, and for sufficiently large $N$.
3. Some lower and upper bounds on $t(N)$ are known beyond $N=79$, but the OEIS table has not yet been extended.

## Timeline

| Date | Author | Conjecture | $N$ | Method | Comments |
| --- | --- | --- | --- | --- | --- |
| [27 Mar 2025](https://terrytao.wordpress.com/2025/03/26/decomposing-a-factorial-into-large-factors/#comment-687574) | Andrew Sutherland | 1 | $[1,10^5]$ | Greedy | N = [182](https://math.mit.edu/~drew/ES182.txt), [200](https://math.mit.edu/~drew/ES200.txt), [207](https://math.mit.edu/~drew/ES207.txt) treated separately
|  [27 Mar 2025](https://terrytao.wordpress.com/2025/03/26/decomposing-a-factorial-into-large-factors/#comment-687574) | Andrew Sutherland | 2 | $[298344, 3 \times 10^5]$ | Greedy | Surplus of 372 at $N=3 \times 10^5$
| [3 Apr 2025](https://terrytao.wordpress.com/2025/03/26/decomposing-a-factorial-into-large-factors/#comment-687641) | Matthieu Rosenfeld | 2 | $3 \times 10^5$ | Improved greedy | Surplus of 393
| [3 Apr 2025](https://terrytao.wordpress.com/2025/03/26/decomposing-a-factorial-into-large-factors/#comment-687646) | Uhrmar | 2 | $3 \times 10^5$ | Linear program | Surplus of 455; likely optimal
| [4 Apr 2025](https://terrytao.wordpress.com/2025/03/26/decomposing-a-factorial-into-large-factors/#comment-687655) | Matthieu Rosenfeld | 2 | $[138075, 5 \times 10^5]$ | Improved greedy
| [5 Apr 2025](https://terrytao.wordpress.com/2025/03/26/decomposing-a-factorial-into-large-factors/#comment-687676) | Kevin Ventullo | 2 | $[3 \times 10^5, 10^8$] | Improved greedy 
| [6 Apr 2025](https://terrytao.wordpress.com/2025/03/26/decomposing-a-factorial-into-large-factors/#comment-687676) | Kevin Ventullo | 2 | $[8 \times 10^4, 3 \times 10^8$] | Improved greedy | Conjecture 1 is now reduced to Conjecture 2
| [6 Apr 2025](https://terrytao.wordpress.com/2025/03/26/decomposing-a-factorial-into-large-factors/#comment-687695) | Matthieu Rosenfeld | 2 | $[8 \times 10^4, 10^9]$ | Improved greedy

## Additional links

- "[Decomposing a factorial into large factors](https://terrytao.wordpress.com/2025/03/26/decomposing-a-factorial-into-large-factors/)", blog post, Terence Tao, 26 March 2025.
- [Decomposing a factorial into large factors](https://arxiv.org/abs/2503.20170), arXiv preprint v2, Terence Tao, 28 March 2025.
- [OEIS A034256](https://oeis.org/A034258)
- [Lower bounds on $t(N)$ for $80 \leq N \leq 599$](https://terrytao.wordpress.com/wp-content/uploads/2025/03/tbounds.txt).
- [Notes on criteria for lower bounding $t(N)$](https://github.com/teorth/erdos-guy-selfridge/blob/main/LaTeX/notes.pdf)


