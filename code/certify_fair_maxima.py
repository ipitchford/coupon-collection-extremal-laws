"""Certify the exhaustive fair-mechanism maxima of Section 6.

Run from the package root (needs a C compiler on PATH as `cc`):
    python3 -I -B -O code/certify_fair_maxima.py --output results/fair_maxima.json

Steps
1. Compile code/fair_maxima.c into a temporary directory and run it for every (n, s) in CASES. The C
   program enumerates every fair mechanism (uniform law on a family of distinct s-sets
   with all point degrees equal) and evaluates E T in double precision.
2. Separation: the largest and second-largest distinct double values must differ by more
   than SEPARATION. Each E[S] comes from at most n <= 8 levels of the recursion, each a sum of
   at most 71 positive terms and one division, so its relative rounding error is at most about
   75 n units in the last place (below 1e-12); SEPARATION = 1e-6 therefore certifies that no
   family outside the reported list attains the maximum. Observed separations exceed 6e-3.
3. Exact re-evaluation in rational arithmetic of every reported maximiser and of the full
   model, and structural identification of the maximisers.
Every check raises SystemExit on failure; nothing relies on assert.
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile
from collections import Counter
from fractions import Fraction as F
from functools import cache
from itertools import combinations

CASES = [(4, 2), (5, 2), (5, 3), (6, 2), (6, 3), (6, 4), (7, 2), (7, 3), (7, 4), (7, 5), (8, 2), (8, 6)]
SEPARATION = 1e-6
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def check(condition, message):
    if not condition:
        raise SystemExit(f"CHECK FAILED: {message}")


def mean_time(n, packages):
    """Exact E T for the uniform law on `packages` (bitmasks), by recursion on covered sets."""
    full = (1 << n) - 1

    @cache
    def visit(covered):
        if covered == full:
            return F(0)
        moves = Counter(covered | b for b in packages)
        stay = moves.pop(covered, 0)
        check(stay < len(packages), "uncoverable state")
        return (len(packages) + sum(c * visit(t) for t, c in moves.items())) / F(len(packages) - stay)
    return visit(0)


def pair_counts(n, blocks):
    counts = Counter()
    for b in blocks:
        pts = [i for i in range(n) if b >> i & 1]
        for a, c in combinations(pts, 2):
            counts[(a, c)] += 1
    return [counts[(a, c)] for a, c in combinations(range(n), 2)]


def is_pair_design(n, blocks, lam):
    return all(c == lam for c in pair_counts(n, blocks))


def splits_into_two_designs(n, blocks):
    """True if a lambda=2 family of triples is the union of two block-disjoint Steiner triple systems."""
    blocks = sorted(blocks)
    k = len(blocks) // 2
    first = blocks[0]
    for rest in combinations(blocks[1:], k - 1):
        part = (first,) + rest
        other = [b for b in blocks if b not in part]
        if is_pair_design(n, part, 1) and is_pair_design(n, other, 1):
            return True
    return False


def run_case(binary, n, s):
    out = subprocess.run([binary, str(n), str(s)], capture_output=True, text=True, check=False)
    check(out.returncode == 0, f"search failed for ({n},{s}): {out.stderr}")
    lines = out.stdout.strip().splitlines()
    head = lines[0].split()
    info = dict(zip(head[0::2], head[1::2]))
    families = [tuple(int(t) for t in line.split()[1:]) for line in lines[1:]]
    check(len(families) == int(info["maximisers"]), "maximiser count")
    return int(info["families"]), float(info["max"]), float(info["second"]), float(info["min"]), families


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=None)
    args = parser.parse_args()
    build = tempfile.mkdtemp(prefix="fair_maxima_")
    binary = os.path.join(build, "fair_maxima")
    comp = subprocess.run(["cc", "-O2", "-o", binary, os.path.join(ROOT, "code", "fair_maxima.c")],
                          capture_output=True, text=True, check=False)
    check(comp.returncode == 0, f"compilation failed: {comp.stderr}")
    report = {}
    for n, s in CASES:
        count, best, second, worst, families = run_case(binary, n, s)
        check(best - second > SEPARATION, f"({n},{s}) maximum not separated")
        full = [sum(1 << i for i in c) for c in combinations(range(n), s)]
        full_mean = mean_time(n, full)
        exact = {mean_time(n, fam) for fam in families}
        check(len(exact) == 1, f"({n},{s}) maximisers disagree in exact arithmetic")
        value = exact.pop()
        check(abs(float(value) - best) < 1e-9, f"({n},{s}) exact and double maxima disagree")
        sizes = Counter(len(f) for f in families)
        if (n, s) == (7, 3):
            fano = [f for f in families if len(f) == 7]
            double = [f for f in families if len(f) == 14]
            check(value == F(163, 30), "(7,3) maximum is 163/30")
            check(len(fano) == 30 and all(is_pair_design(7, f, 1) for f in fano), "30 Fano planes")
            check(len(double) == 120 and all(splits_into_two_designs(7, f) for f in double),
                  "120 unions of two block-disjoint Fano planes")
            structure = "30 Fano planes (lines as packages) and 120 unions of two block-disjoint Fano planes"
        elif (n, s) == (7, 4):
            check(value == F(47, 12), "(7,4) maximum is 47/12")
            omitted = [[127 ^ b for b in f] for f in families]
            check(len(families) == 30 and all(is_pair_design(7, f, 1) for f in omitted),
                  "30 complements of Fano planes")
            structure = "30 complements of Fano planes (Theorem 2.1)"
        elif (n, s) == (6, 3):
            check(len(families) == 12 and all(len(f) == 10 and is_pair_design(6, f, 2) for f in families),
                  "12 copies of the 2-(6,3,2) design")
            check(value == F(157, 36), "(6,3) maximum is 157/36")
            structure = "12 labelled copies of the 2-(6,3,2) design"
        else:
            check(len(families) == 1 and sorted(families[0]) == sorted(full), f"({n},{s}) full model unique maximiser")
            structure = "full model, uniquely"
        check(value >= full_mean, "maximum at least the full model")
        report[f"({n},{s})"] = {"fair_mechanisms": count, "max_mean": str(value), "max_float": float(value),
                               "full_model_mean": str(full_mean), "full_float": float(full_mean),
                               "excess": str(value - full_mean), "excess_float": float(value - full_mean),
                               "second_largest_float": second, "min_regular_float": worst,
                               "maximisers": len(families), "maximiser_sizes": dict(sizes),
                               "structure": structure}
        print(f"({n},{s}): {count} fair mechanisms; max {value} = {float(value):.6f}; "
              f"full {float(full_mean):.6f}; excess {float(value - full_mean):.6f}; {structure}")
    report["status"] = "ALL CHECKS PASSED"
    report["python"] = sys.version.split()[0]
    if args.output:
        with open(args.output, "w") as handle:
            json.dump(report, handle, indent=1, sort_keys=True)
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    main()
