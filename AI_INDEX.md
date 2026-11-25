# AI index: Extremal laws for coupon collection with group drawings (v0.1.0-candidate)

Machine-oriented map of claims, evidence and limits. Human readers should start with [README.md](README.md) ("What
this is about") and the paper [manuscript.pdf](manuscript.pdf) (source [manuscript.tex](manuscript.tex); Section 1
states the problem, what was known, what is new, the main idea and a roadmap). DOI 10.5281/zenodo.24534721 (concept
10.5281/zenodo.24534720). Status: unrefereed candidate; internal AI-assisted review only.

## Normalisation

Coupons [n]. A sampling law is a distribution on packages (subsets of [n]); draws are i.i.d. T = number of draws until
the union is [n]. Slow side: packages of size exactly s, omitted set B of size r = n - s, p = r/n. Balanced (fair) law:
every coupon omitted with probability p. Fair mechanism (Grunbaum-Yaakobi): uniform law on a regular family of
distinct s-sets. Full model: uniform on all C(n,s) packages, time T_full. Z_j = number missing after j draws;
P(T > j) = P(Z_j > 0). Fast side: any law on packages of size at most s; x = n/s; H_x = int_0^1 (1-(1-u)^x)/u du.
gamma = Euler's constant. Reference keys as in [refs.bib](refs.bib): barak (arXiv:2606.28216), berend-asym, sher,
flm, fang, finner, gy and gy-isit, malkhi, pelekis.

## Claims and where they are proved

| ID | Claim | Location | Status / credit |
|---|---|---|---|
| 1 | For every balanced law and j >= 1, P(T > j) <= n p^j - (n(n-1)/r) u^j with u = r(r-1)/(n(n-1)); equality at any j >= 2 iff the omitted set is uniform on an S(2,r,n); the design law has the largest mean among balanced laws and fair mechanisms | Theorem 3.1 | written proof; degree-two Bonferroni-type bound classical (no novelty claimed) |
| 2 | Two-draw deficit identity and stability | Proposition 3.2 | written proof |
| 3 | Seven coupons, packages of four: design mean 47/12, full model 257/68, excess 7/51; tail difference 7^(1-j) - 35^(1-j) | Example 3.3 | written proof; exact check |
| 4 | Partial coverage with h-set balance: bound attained iff S(h+1,r,n) | Theorem 3.4 | written proof (h-set balance is stronger than fairness for h > 1) |
| 5 | n p^k -> lambda in (0, inf), fixed k >= 2: max E T over balanced laws and over fair mechanisms is k + min(1, lambda) + o(1); full model k + 1 - e^(-lambda) + o(1); peak excess 1/e at lambda = 1 | Theorem 4.1, Lemma 4.3 (regularisation), Figure 1 | written proof; star mechanism of barak (Theorem 2.4) attains k + 1 for lambda > 1 (credited, Remark 4.2); construction existential |
| 6 | For all n and r: E T - E T_full <= sum_j [min(1, n p^j) - 1 + (1 - p^j)^n] <= 1/e + (1 - gamma)/ln(n/r); at r = n/2 the bound is 0.9778; limit 1/e attained | Theorem 5.4 with Lemma 5.1, Proposition 5.2, Lemma 5.3 | written proof; answers barak's question quantitatively |
| 7 | Exhaustive search, n <= 7 all s and n = 8 with s in {2,6}: full model uniquely slowest except (6,3) (3,435 fair mechanisms, max 157/36, 12 copies of the 2-(6,3,2) design), (7,3) (2,505,121, max 163/30 by 30 Fano planes and 120 unions of two block-disjoint Fano planes), (7,4) (max 47/12 by 30 Fano complements) | Proposition 6.1, Table 2 | computer-assisted; double-precision enumeration with separation > 1e-6 and exact-rational recomputation; (6,3) smallest counterexample to gy Conjecture 2 |
| 8 | Product bound for independent coordinates each entering at most s functions | Lemma 7.1 | case p_j = s of finner Theorem 2.1 and (3.1); restated in pelekis Theorem 2.1 |
| 9 | Poisson-time comparison P(tau_h <= t) <= prod_i G_h(t d_i)^(1/s) <= G_h(t/x)^x; uniform partition unique minimiser of E T_h when s divides n | Theorem 7.2 | written proof; h = 1 is pelekis Theorem 2.6 after Poissonisation (credited) |
| 10 | E T >= x H_x for every law on packages of size at most s; equality iff s divides n and the law is a uniform partition | Theorem 7.3 | written proof; proves the conjecture recorded by fang and sher, with uniqueness, and gy Conjecture 3 |
| 11 | P(T > k) >= (b/n)^(k-1) with b = n - s; E T >= 1 + n/s, equality iff (n - s) divides n and omitted sets are a uniform partition | Corollary 7.4, Theorem 7.5 | written proof; the law and its mean are due to sher |
| Open | finite maxima without designs; growing horizons and fixed omitted fraction; unbounded excess for s = o(n); rates; fast side when neither s nor n - s divides n; tail ordering for general divisible capacities | Section 8 | open |

## Evidence

| Check | Script | Scope |
|---|---|---|
| Seven-point example; pointwise majorants and equality sets for r <= 60 (73,750 tests); S(3,4,8) partial coverage; minimum bounds (14 divisible pairs exact, complementary partitions, 594 random competitor laws); Lemma 5.1 (4,090 cases) and Proposition 5.2 (168 cases) exact; gap series for n <= 100 (4,950 cases, largest series/bound ratio 0.980); projective rank-chain means; finite full-model values at n = 100, 400, 1600 | [code/verify_coverage.py](code/verify_coverage.py) -> [results/verification.json](results/verification.json) | exact rational arithmetic plus float comparisons with declared tolerances |
| All fair mechanisms for the parameter pairs of Proposition 6.1 | [code/fair_maxima.c](code/fair_maxima.c) via [code/certify_fair_maxima.py](code/certify_fair_maxima.py) -> [results/fair_maxima.json](results/fair_maxima.json) | double-precision enumeration; separation > 1e-6 (observed >= 6.1e-3); maximisers and full model recomputed exactly; structure checked |
| Figure 1 curves min(1, lambda) and 1 - exp(-lambda) | [code/make_figure.py](code/make_figure.py) -> [figures/](figures/) | plot of the limit functions |

Every check exits non-zero on failure without `assert`, also under `python -O`. Negative controls (release replay;
the first also in CI): 47/12 -> 47/13 in verify_coverage.py and 163/30 -> 163/31 in certify_fair_maxima.py each exit 1
under -O. Release replay and environment: [REPLAY_RECEIPT.md](REPLAY_RECEIPT.md), [ENVIRONMENT.txt](ENVIRONMENT.txt).

Numbers quoted on the release page and in the audio: 47/12 and 257/68; 1/e (about 0.37); 0.42 (1 - gamma); below
one draw when packages hold at least half the coupons (0.978 at r = n/2); 2,505,121 fair mechanisms at (7,3); 163/30
for the Fano plane; (6,3) the smallest counterexample; (n/s)H(n/s); 1 + n/s; 0.03 draws at n = 1600. All come from
the paper and results/.

## Limits

Idealised independent draws with equal coupon frequencies (slow side). Theorem 4.1 is asymptotic with unquantified
o(1) terms and an existential construction. Exact slowest laws without designs are known only for the small cases
searched. Literature search of limited scope ([RESEARCH_GATES.json](RESEARCH_GATES.json)). Internal AI-assisted review
only; see [REVIEW_SUMMARY.md](REVIEW_SUMMARY.md).
