# Extremal laws for coupon collection with group drawings

**How slow, and how fast, can group coupon collection be?** Version 0.1.0-candidate. DOI
[10.5281/zenodo.24534721](https://doi.org/10.5281/zenodo.24534721) (all versions:
[10.5281/zenodo.24534720](https://doi.org/10.5281/zenodo.24534720)). Release page:
https://evidencepress.org/releases/coupon-collection-extremal-laws/

Unrefereed research candidate. Author: Anonymous. Text CC0-1.0; code MIT (see [LICENSE.md](LICENSE.md)).

## What this is about

Suppose you want a full set of n different coupons: stickers, trading cards, or fragments of a DNA library. In the
classical version each box holds one random coupon, and a full set takes about n(1 + 1/2 + ... + 1/n) boxes on
average. Here each box holds a *group* of s coupons at once, and whoever fills the boxes decides how the groups
overlap. How quickly can a full set be completed? And how slowly can completion be made while staying *fair*, meaning
every coupon is equally common?

The same question appears wherever items arrive in groups: promotions that want slow but fair completion, sequencing
and DNA-storage runs where reads arrive in batches, probabilistic quorum systems in which clients contact random groups
of servers that must overlap, and the placement of data replicas across machines.

## What was known

- Grunbaum and Yaakobi conjectured that drawing uniformly from all possible groups (the *full model*) is the slowest
  fair rule.
- Barak-Pelleg and Berend disproved this with the seven-point Fano plane, and asked how slow a fair rule can be and how
  large the excess over the full model can become.
- On the fast side, Fang and Chang (2014) solved the case where each box holds half the coupons, and conjectured that
  splitting the coupons into equal disjoint groups is always fastest when s divides n.

## What is new

Write r = n − s for the number of coupons a box leaves out.

1. **Designs are the slowest fair rules** (Theorem 3.1). When the left-out coupons can form a Steiner 2-design,
   sampling that design is the slowest fair rule after every number of draws, and only the design achieves this.
   Seven coupons in boxes of four: 47/12 boxes on average, against 257/68 for the full model.
2. **Every population size, in every critical window** (Theorem 4.1). If λ is the expected number of coupons still
   missing after k boxes, the slowest fair mean is k + min(1, λ), against k + 1 − e^(−λ) for the full model (both up to
   terms that vanish as n grows). Barak-Pelleg and Berend's star mechanism already reaches k + 1 in its own windows,
   where λ > 1; the new parts are the matching upper bound, every λ (including λ < 1), every n, and the peak excess
   1/e at λ = 1.
3. **A universal bound on the excess** (Theorem 5.4). No fair rule is ever more than 1/e + 0.42/ln(n/r) boxes slower
   on average than the full model (0.42 is 1 − γ, with γ Euler's constant). This is less than one box whenever boxes
   hold at least half the coupons, and it tends to 1/e ≈ 0.37 boxes when boxes hold almost everything. That limit is
   reached.
4. **Exact answers for small cases** (Proposition 6.1). An exhaustive exact search of every fair rule with n ≤ 7 (and
   n = 8 with s = 2 or 6), up to 2,505,121 rules for one pair (n, s), shows that the Fano plane is the slowest fair rule at
   Barak-Pelleg and Berend's own example (mean 163/30), and that six coupons in boxes of three is the smallest case
   where the full model is not slowest.
5. **The fastest rules** (Theorems 7.3 and 7.5). Every rule on boxes of at most s coupons needs at least
   max{x·H(x), 1 + x} boxes on average, with x = n/s. If s divides n, equal disjoint groups are uniquely fastest, with
   (n/s)·H(n/s) boxes on average; this proves the Fang–Chang conjecture. If n − s divides n, complementary partitions
   are uniquely fastest, with 1 + n/s.

**Credit.** The degree-two counting bound on the slow side is classical. The h = 1 case of the product bound on the
fast side is Pelekis, Ramon and Wang's Theorem 2.6 after Poissonisation, an instance of Finner's generalized Hölder
inequality. Berend and Sher introduced the complementary-decomposition law and computed its mean.

**The idea.** Every fair rule leaves the same expected number of coupons missing. Slow rules make the missing coupons
come one at a time, which designs and projective geometry do; fast rules make them disappear in clumps, which
partitions do. The slow side uses the first two moments of the number missing; the fast side runs each box type on
its own Poisson clock and applies a Hölder-type product inequality.

## Limits

- The critical-window result is asymptotic and converges slowly: at n = 1600 the full model is still 0.03 boxes above
  its limit. The slow construction is existential.
- The exact slowest rule without a design is known only for small n.
- Whether the excess can grow without limit for very small boxes is open.
- The fastest rule is open when neither s nor n − s divides n.
- All results concern idealised independent draws.

## Contents

| Path | What it is |
|---|---|
| [manuscript.pdf](manuscript.pdf), [manuscript.tex](manuscript.tex) | The paper (14 pages; LaTeX source, reads `figures/critical-window.pdf`) |
| [figures/critical-window.pdf](figures/critical-window.pdf), [figures/critical-window.png](figures/critical-window.png) | Figure 1 |
| [code/verify_coverage.py](code/verify_coverage.py) | Exact-arithmetic checks of the finite statements (standard library) |
| [code/fair_maxima.c](code/fair_maxima.c), [code/certify_fair_maxima.py](code/certify_fair_maxima.py) | Exhaustive enumeration of small fair mechanisms and its exact-rational certificate (Proposition 6.1) |
| [code/make_figure.py](code/make_figure.py) | Regenerates Figure 1 (numpy, matplotlib) |
| [results/verification.json](results/verification.json), [results/fair_maxima.json](results/fair_maxima.json) | Recorded outputs |
| [requirements.txt](requirements.txt) | Figure packages; the checks need only the standard library and a C compiler |
| [refs.bib](refs.bib) | Bibliography of the paper |
| [AI_INDEX.md](AI_INDEX.md), [RESEARCH_GATES.json](RESEARCH_GATES.json), [REVIEW_SUMMARY.md](REVIEW_SUMMARY.md), [REPLAY_RECEIPT.md](REPLAY_RECEIPT.md), [ENVIRONMENT.txt](ENVIRONMENT.txt) | Machine-readable index, research-gate record, review summary, replay receipt, environment |
| [MANIFEST.sha256](MANIFEST.sha256) | SHA-256 of every file |

## Reproducing the checks

From the package root, with Python 3.12 or later:

```sh
python3 -I -B -O code/verify_coverage.py --output results/verification.json       # about 1 s; ALL CHECKS PASSED
python3 -I -B -O code/certify_fair_maxima.py --output results/fair_maxima.json    # about 40 s; needs cc; ALL CHECKS PASSED
python3 -I -B code/make_figure.py                                                 # needs numpy and matplotlib
```

Both checking scripts test explicitly (no `assert`) and exit 1 on failure, also under `python -O`.

Comparison policy (declared before tagging; the same in CI, ENVIRONMENT.txt and REPLAY_RECEIPT.md): the `python`
field (interpreter version) is not compared; exact rational values (stored as strings such as "47/12"), counts and
structures must match exactly; floats in `verification.json` within absolute 1e-12 (the gap-series ratio, 1/e,
1 − γ, the bound at r = n/2), except `minimum.smallest_slack`, a floating-point equality case near zero, within
absolute 1e-9; double values in `fair_maxima.json` within relative 1e-9 (they may differ across platforms in the last
bits; the certificate needs a separation above 1e-6, and the observed separation is at least 6.1e-3). GitHub CI
(`.github/workflows/replay.yml`) checks the manifest, runs both checking scripts on Linux, compares under this policy
and runs a negative control.

The computations test the stated finite cases; the general results rest on the written proofs.

## Assurance

Internal AI-assisted review only: a combined five-role Claude review panel, one revision round, a re-review, a proof
audit of the new proofs, and a clean replay with negative controls. No Astra/Codex review took place. This is not peer
review, independent reproduction or formal verification. See [REVIEW_SUMMARY.md](REVIEW_SUMMARY.md).

## Citation

Anonymous (2026). *Extremal laws for coupon collection with group drawings* (version 0.1.0-candidate). Evidence Press.
https://doi.org/10.5281/zenodo.24534721
