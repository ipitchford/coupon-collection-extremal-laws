"""Exact finite checks for "Extremal laws for coupon collection with group drawings".

Run from the package root:
    python3 -I -B -O code/verify_coverage.py --output results/verification.json

Every check raises SystemExit with a message on failure; no check relies on assert,
so the script also fails correctly under python -O. Standard library only.
Probabilities and means are exact rationals (fractions.Fraction) except where a
floating-point tolerance is declared explicitly (FLOAT_TOL).
"""
import argparse
import json
import math
import random
import sys
from collections import Counter
from fractions import Fraction as F
from functools import cache
from itertools import combinations
from math import comb

FLOAT_TOL = 1e-12
EULER_GAMMA = 0.57721566490153286060651209008240243
SUMMARY = {}


def check(condition, message):
    if not condition:
        raise SystemExit(f"CHECK FAILED: {message}")


def mask(items):
    return sum(1 << i for i in items)


def full_family(n, r):
    return [mask(block) for block in combinations(range(n), r)]


def intersection_counts(n, blocks, steps):
    """Ordered omission histories, by the set of coupons still missing after each draw."""
    counts = {(1 << n) - 1: 1}
    result = []
    for _ in range(steps):
        nxt = Counter()
        for missing, count in counts.items():
            for block in blocks:
                nxt[missing & block] += count
        counts = nxt
        result.append(counts)
    return result


def expected_time(n, omitted):
    """Exact E T for the uniform law on the list `omitted` of omitted sets (multiset allowed)."""
    @cache
    def visit(missing):
        if not missing:
            return F(0)
        successors = Counter(missing & block for block in omitted)
        loops = successors.pop(missing, 0)
        if loops == len(omitted):
            raise SystemExit("CHECK FAILED: a coupon can never be collected")
        later = sum(mult * visit(state) for state, mult in successors.items())
        return F(len(omitted) + later) / (len(omitted) - loops)
    return visit((1 << n) - 1)


def tail(counts, h=1):
    """Probability that at least h coupons are still missing."""
    return F(sum(c for state, c in counts.items() if state.bit_count() >= h), sum(counts.values()))


def higher_bound(n, r, h, j):
    c = F(comb(r, h) - 1, comb(r, h + 1))
    return (comb(n, h) * F(comb(r, h), comb(n, h)) ** j
            - c * comb(n, h + 1) * F(comb(r, h + 1), comb(n, h + 1)) ** j)


def harmonic_real(x, steps=20000):
    """H_x = int_0^1 (1-(1-u)^x)/u du by composite Simpson; accurate far below 1e-9 here."""
    f = lambda u: x if u == 0 else (1 - (1 - u) ** x) / u
    hstep = 1.0 / steps
    total = f(0) + f(1)
    for i in range(1, steps):
        total += (4 if i % 2 else 2) * f(i * hstep)
    return total * hstep / 3


def check_designs():
    fano = [mask((a + i) % 7 for i in (0, 1, 3)) for a in range(7)]
    full = full_family(7, 3)
    design_mean, full_mean = expected_time(7, fano), expected_time(7, full)
    check((design_mean, full_mean) == (F(47, 12), F(257, 68)), "seven-point means")
    check(design_mean - full_mean == F(7, 51), "seven-point excess")
    fano_counts = intersection_counts(7, fano, 10)
    full_counts = intersection_counts(7, full, 10)
    for j, (a, b) in enumerate(zip(fano_counts, full_counts), start=1):
        check(tail(a) == higher_bound(7, 3, 1, j), f"design envelope equality at j={j}")
        check(tail(a) - tail(b) == F(1, 7) ** (j - 1) - F(1, 35) ** (j - 1), f"tail difference j={j}")
    check(1 - tail(full_counts[1]) == F(4, 35), "full model finishes at draw two w.p. 4/35")
    planes = [mask(x for x in range(8) if (x & a).bit_count() % 2 == b) for a in range(1, 8) for b in (0, 1)]
    check(len(set(planes)) == 14, "AG(3,2) has fourteen planes")
    for j, counts in enumerate(intersection_counts(8, planes, 8), start=1):
        check(tail(counts, 2) == higher_bound(8, 4, 2, j), f"S(3,4,8) partial-coverage equality j={j}")
    SUMMARY["seven_point"] = {"design_mean": str(design_mean), "full_mean": str(full_mean),
                              "excess": str(design_mean - full_mean), "full_two_draw_finish": "4/35"}
    print(f"seven-point design mean {design_mean}, full model {full_mean}, excess {design_mean - full_mean}")


def check_moment_majorants():
    tests = 0
    for r in range(2, 61):
        for h in range(1, r):
            c = F(comb(r, h) - 1, comb(r, h + 1))
            for z in range(r + 1):
                g = comb(z, h) - c * comb(z, h + 1) - int(z >= h)
                check(g >= 0, f"majorant fails r={r} h={h} z={z}")
                check((g == 0) == (z <= h or z == r), f"equality set r={r} h={h} z={z}")
                tests += 1
    SUMMARY["pointwise_majorant_tests"] = tests
    print(f"{tests} exact pointwise majorant and equality tests, r up to 60")


def check_minimum():
    """Partition and complementary-partition minima, plus random competitors."""
    rng = random.Random(20261124)
    divisible = 0
    for n in range(2, 10):
        for s in range(1, n):
            all_points = (1 << n) - 1
            if n % s == 0:
                parts = [mask(range(a, a + s)) for a in range(0, n, s)]
                m = n // s
                lower = m * sum(F(1, a) for a in range(1, m + 1))
                check(expected_time(n, [all_points ^ b for b in parts]) == lower, f"partition mean n={n} s={s}")
                check(expected_time(n, full_family(n, n - s)) >= lower, f"full model vs partition n={n} s={s}")
                divisible += 1
            b = n - s
            if n % b == 0:
                omitted = [mask(range(a, a + b)) for a in range(0, n, b)]
                check(expected_time(n, omitted) == 1 + F(n, s), f"complementary partition mean n={n} s={s}")
    random_laws = 0
    worst_slack = None
    for n in range(3, 8):
        for s in range(1, n):
            x = n / s
            bound = max(x * harmonic_real(x), 1 + x)
            packages = full_family(n, s)
            for _ in range(60):
                support = rng.sample(packages, rng.randint(1, min(6, len(packages))))
                weights = [rng.randint(1, 3) for _ in support]
                law = [p for p, w in zip(support, weights) for _ in range(w)]
                union = 0
                for p in law:
                    union |= p
                if union != (1 << n) - 1:
                    continue
                value = expected_time(n, [((1 << n) - 1) ^ p for p in law])
                slack = float(value) - bound
                check(slack > -1e-9, f"lower bound violated n={n} s={s}: {value} < {bound}")
                worst_slack = slack if worst_slack is None else min(worst_slack, slack)
                random_laws += 1
    SUMMARY["minimum"] = {"divisible_pairs": divisible, "random_covering_laws": random_laws,
                          "smallest_slack": worst_slack}
    print(f"{divisible} divisible pairs exact; {random_laws} random covering laws respect max(xH_x, 1+n/s)")


def hypergeometric_pgf(n, r, w, x):
    return sum(F(comb(w, k) * comb(n - w, r - k), comb(n, r)) * x ** k for k in range(0, min(r, w) + 1))


def check_negative_dependence():
    """Lemma 5.1 (pgf comparison) and Proposition 5.2 (full-model tails), exactly."""
    lemma = 0
    for n in range(1, 13):
        for r in range(0, n + 1):
            p = F(r, n)
            for w in range(0, n + 1):
                for x in (F(0), F(1, 3), F(1, 2), F(5, 7), F(1)):
                    check(hypergeometric_pgf(n, r, w, x) <= (1 - p + p * x) ** w, f"pgf lemma n={n} r={r} w={w}")
                    lemma += 1
    tails = 0
    for n in range(2, 9):
        for r in range(1, n):
            p = F(r, n)
            for j, counts in enumerate(intersection_counts(n, full_family(n, r), 6), start=1):
                check(tail(counts) >= 1 - (1 - p ** j) ** n, f"full-model tail bound n={n} r={r} j={j}")
                tails += 1
    SUMMARY["negative_dependence"] = {"pgf_cases": lemma, "full_tail_cases": tails}
    print(f"{lemma} exact pgf comparisons and {tails} exact full-model tail bounds hold")


def gap_series(n, r):
    """sum_{j>=1} [min(1, n p^j) - 1 + (1-p^j)^n] in floating point (expm1/log1p for accuracy).

    Terms are summed until n p^j < 1e-9; the omitted remainder is below sum (n p^j)^2 / 2,
    which is added as a conservative upper estimate.
    """
    p = r / n
    total, j = 0.0, 1
    while True:
        pj = p ** j
        mu = n * pj
        total += min(1.0, mu) + math.expm1(n * math.log1p(-pj))
        if mu < 1e-9:
            return total + mu * mu / (1 - p * p)
        j += 1


def check_gap_bound():
    one_minus_gamma = 1 - EULER_GAMMA
    # 1 - gamma = int_0^inf h(mu)/mu dmu, with h(mu) = min(1,mu) - 1 + exp(-mu); series form:
    ein1 = sum((-1) ** (k + 1) / (k * math.factorial(k)) for k in range(1, 40))
    e1_1 = ein1 - EULER_GAMMA  # E_1(1) = Ein(1) - gamma
    integral = (1 - ein1) + e1_1
    check(abs(integral - one_minus_gamma) < FLOAT_TOL, "integral equals 1 - gamma")
    worst = None
    cases = 0
    for n in range(2, 101):
        for r in range(1, n):
            bound = 1 / math.e + one_minus_gamma / math.log(n / r)
            value = gap_series(n, r)
            check(value <= bound + FLOAT_TOL, f"gap bound n={n} r={r}: {value} > {bound}")
            ratio = value / bound
            worst = ratio if worst is None else max(worst, ratio)
            cases += 1
    # Exact excesses of the slowest fair mechanisms over the full model (Section 6 table)
    exact = {"(7,4)": (7, 3, F(47, 12) - F(257, 68)),
             "(7,3)": (7, 4, F(163, 30) - F(85691, 15810))}
    for label, (n, r, excess) in exact.items():
        check(float(excess) <= gap_series(n, r) + FLOAT_TOL, f"exact excess within series bound {label}")
    half = 1 / math.e + one_minus_gamma / math.log(2)
    check(half < 1, "r <= n/2 gives an excess below one draw")
    SUMMARY["gap_bound"] = {"one_minus_gamma": one_minus_gamma, "cases_n_up_to_100": cases,
                            "largest_series_to_bound_ratio": worst, "bound_at_r_eq_n_over_2": half,
                            "inverse_e": 1 / math.e}
    print(f"gap series below 1/e + (1-gamma)/ln(n/r) in {cases} cases (n <= 100); "
          f"bound at r = n/2 is {half:.6f}")


def check_projective_windows():
    """Exact means of uniform hyperplane omissions in PG(k,q) (rank chain)."""
    rows = {}
    for k in (2, 3, 4):
        data = []
        for q in (2, 3, 11, 101):
            n = (q ** (k + 1) - 1) // (q - 1)
            r = (q ** k - 1) // (q - 1)
            mean = sum(F(q ** (k + 1) - 1, q ** (k + 1) - q ** rank) for rank in range(k + 1))
            check(mean >= k + 1, "projective mean at least k+1")
            data.append([q, round(float(mean), 5), round(float(n * F(r, n) ** k), 5)])
        rows[str(k)] = data
        print(f"PG dimension {k}, (field order, exact mean, n*p^k): {data}")
    SUMMARY["projective_windows"] = rows


def full_model_mean(n, r):
    """Exact E T for the full model: inclusion-exclusion over the set of missing coupons."""
    total = F(1)
    j = 1
    while True:
        pj = sum((-1) ** (a + 1) * comb(n, a) * F(comb(n - a, r - a), comb(n, r)) ** j for a in range(1, r + 1))
        total += pj
        if pj < F(1, 10 ** 18):
            # remaining tail is at most sum_{i>j} n p^i < n p^(j+1)/(1-p)
            return total, float(n * F(r, n) ** (j + 1) / (1 - F(r, n)))
        j += 1


def check_critical_finite_values():
    """Finite-n full-model means near the critical window k=2, lambda=1 (diagnostic)."""
    rows = []
    for n in (100, 400, 1600):
        r = round(math.sqrt(n))  # n p^2 = r^2/n close to 1
        lam = r * r / n
        mean, err = full_model_mean(n, r)
        check(err < 1e-12, 'full-model truncation error')
        rows.append([n, r, round(lam, 6), round(float(mean), 6),
                     round(3 - math.exp(-lam), 6)])
    SUMMARY["critical_full_model_finite"] = rows
    print(f"full model near k=2, lambda=1 (n, r, n p^2, exact mean, limit 3-e^-lambda): {rows}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=None)
    args = parser.parse_args()
    check_designs()
    check_moment_majorants()
    check_minimum()
    check_negative_dependence()
    check_gap_bound()
    check_projective_windows()
    check_critical_finite_values()
    SUMMARY["status"] = "ALL CHECKS PASSED"
    SUMMARY["python"] = sys.version.split()[0]
    if args.output:
        with open(args.output, "w") as handle:
            json.dump(SUMMARY, handle, indent=1, sort_keys=True)
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    main()
