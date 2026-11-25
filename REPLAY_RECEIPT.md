# Replay receipt (release 0.1.0-candidate, 25 November 2026)

The publisher replayed the approved candidate from a fresh copy before adding the DOI line. Only `manuscript.tex`
(the DOI line under the author), the rebuilt `manuscript.pdf` and the release records changed afterwards; every
script, figure and result file is byte-identical to the replayed copy (checked by SHA-256 in the frozen-archive gate).

Interpreters were printed inside the run (see [ENVIRONMENT.txt](ENVIRONMENT.txt)): `uv run --python 3.12` resolved
to CPython 3.14.7 through the host's python3 shim, so `verify_coverage.py` was also run under CPython 3.12.11 (same
result).

## Runs (fresh copy, cwd = package root, macOS arm64, Apple clang 21, PYTHONDONTWRITEBYTECODE=1)

| Command | Exit | Time | Output |
|---|---|---|---|
| `python3 -I -B -O code/verify_coverage.py --output results/verification.json` | 0 | about 1 s | `ALL CHECKS PASSED`; results/verification.json byte-identical to the recorded file (also `ALL CHECKS PASSED` under 3.12.11) |
| `python3 -I -B -O code/certify_fair_maxima.py --output results/fair_maxima.json` | 0 | 36 s | `ALL CHECKS PASSED`; results/fair_maxima.json byte-identical to the recorded file |
| `python3 -I -B code/make_figure.py` (numpy 2.3.5, matplotlib 3.10.8) | 0 | 2 s | figures/critical-window.pdf and .png byte-identical to the recorded files |

Every run wrote nothing to stderr.

## Negative controls (fresh copies, `python3 -I -B -O`)

| Mutation | Result |
|---|---|
| `verify_coverage.py`: seven-point design mean 47/12 replaced by 47/13 | `CHECK FAILED: seven-point means`, exit 1 |
| `certify_fair_maxima.py`: (7,3) maximum 163/30 replaced by 163/31 | `CHECK FAILED: (7,3) maximum is 163/30`, exit 1 |

## Comparison policy (declared before tagging; also in README.md, ENVIRONMENT.txt and the CI workflow)

- The `python` field (interpreter version) is not compared; timings are not recorded.
- Exact rational values (strings such as "47/12", "163/30"), counts, structures and status: exactly.
- `verification.json` floats: within absolute 1e-12, except `minimum.smallest_slack` (a floating-point equality case
  near zero) within absolute 1e-9.
- `fair_maxima.json` double values: within relative 1e-9. The certificate requires a separation above 1e-6 between the
  largest and second-largest values; the observed separation is at least 6.1e-3, and every maximiser is recomputed in
  exact rational arithmetic.

The comparison script is `.github/ci/compare_outputs.py`. The figure is regenerated on the release host only; CI does
not install numpy or matplotlib.
