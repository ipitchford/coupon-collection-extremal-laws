"""Compare regenerated outputs with the outputs recorded at release (25 November 2026).
Policy (declared before tagging; also in README.md, ENVIRONMENT.txt and REPLAY_RECEIPT.md):
- The "python" field (interpreter version) is not compared.
- Strings (all exact rational values such as "47/12" and "163/30", structures, status), integers and booleans: exactly.
- verification.json floats: within absolute 1e-9 for minimum.smallest_slack (a float equality case near 0) and within
  absolute 1e-12 for every other float (gap-series ratio, 1/e, 1 - gamma, the bound at r = n/2, rounded exact means).
- fair_maxima.json floats (double-precision values of the C enumeration, which may differ across platforms in the last
  bits): within relative 1e-9. The certificate itself only needs separation above 1e-6 (observed at least 6.1e-3) and
  recomputes every maximiser in exact rational arithmetic.
usage: compare_outputs.py [--only verification.json] NEWDIR RECORDEDDIR"""
# SPDX-License-Identifier: MIT
import json, sys
from pathlib import Path
args = sys.argv[1:]
only = None
if args[:1] == ['--only']: only, args = args[1], args[2:]
new, rec = Path(args[0]), Path(args[1])
bad = []
def tol(name, path, ref):
    if name == 'verification.json':
        return 1e-9 if path.endswith('.minimum.smallest_slack') else 1e-12
    return 1e-9 * abs(ref)
def cmp(name, a, b, path, worst):
    if isinstance(a, dict) and isinstance(b, dict):
        ka, kb = sorted(k for k in a if k != 'python'), sorted(k for k in b if k != 'python')
        if ka != kb: bad.append(f'{name}{path}: keys differ'); return
        for k in ka: cmp(name, a[k], b[k], f'{path}.{k}', worst)
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b): bad.append(f'{name}{path}: length differs'); return
        for i, (x, y) in enumerate(zip(a, b)): cmp(name, x, y, f'{path}[{i}]', worst)
    elif isinstance(a, float) or isinstance(b, float):
        if isinstance(a, bool) or isinstance(b, bool) or not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            bad.append(f'{name}{path}: {a!r} vs {b!r}'); return
        d = abs(a - b); worst[0] = max(worst[0], d)
        if d > tol(name, path, b): bad.append(f'{name}{path}: {a!r} vs {b!r}')
    elif type(a) is not type(b) or a != b:
        bad.append(f'{name}{path}: {a!r} vs {b!r}')
for name in ('verification.json', 'fair_maxima.json'):
    if only and name != only: continue
    worst = [0.0]
    cmp(name, json.loads((new / name).read_text()), json.loads((rec / name).read_text()), '', worst)
    same = (new / name).read_bytes() == (rec / name).read_bytes()
    print(f'{name}: largest absolute float difference {worst[0]:.2e}; {"byte-identical" if same else "not byte-identical"}')
if bad: print('FAIL', bad[:20]); sys.exit(1)
print('PASS outputs agree with the recorded outputs under the declared policy')
