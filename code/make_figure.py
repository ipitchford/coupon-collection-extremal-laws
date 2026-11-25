"""Render Figure 1 (limiting tail at the critical horizon) from the formulas of Theorem 4.1.

Run from the package root: python3 code/make_figure.py
Writes figures/critical-window.pdf and figures/critical-window.png.
"""
from pathlib import Path
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
mpl.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 9,
                     'axes.spines.top': False, 'axes.spines.right': False,
                     'axes.labelcolor': '#263735', 'xtick.color': '#425754',
                     'ytick.color': '#425754', 'pdf.fonttype': 42, 'svg.hashsalt': 'ep',
                     'path.simplify': False})
lam = np.linspace(0, 3, 601)
extreme = np.minimum(lam, 1)          # slowest fair law: Pr(T > k) -> min(1, lambda)
full = -np.expm1(-lam)                # full model: Pr(T > k) -> 1 - exp(-lambda)
fig, ax = plt.subplots(figsize=(6.7, 2.55), layout='constrained')
ax.fill_between(lam, full, extreme, color='#efe8dc', zorder=1)
ax.plot(lam, extreme, color='#006d67', linewidth=2.4, label='Slowest fair sampling', zorder=3)
ax.plot(lam, full, color='#934b65', linewidth=2.1, label='Uniform over all packages (full model)', zorder=3)
ax.annotate('', xy=(1, 1), xytext=(1, 1 - np.exp(-1)),
            arrowprops={'arrowstyle': '<->', 'color': '#534237', 'lw': 1.1})
ax.text(1.045, 0.78, 'gap 1/e', color='#534237', fontsize=9)
ax.set(xlim=(0, 3), ylim=(0, 1.07), xlabel=r'Limiting mean number of missing coupons after $k$ draws, $\lambda$',
       ylabel=r'Pr(unfinished after $k$ draws)')
ax.set_yticks([0, .25, .5, .75, 1]); ax.set_xticks([0, .5, 1, 1.5, 2, 2.5, 3])
ax.legend(loc='lower right', frameon=False, fontsize=8.5)
fig.savefig(ROOT / 'figures' / 'critical-window.pdf', metadata={'CreationDate': None, 'ModDate': None})
fig.savefig(ROOT / 'figures' / 'critical-window.png', dpi=200, metadata={'Software': None})
print('wrote figures/critical-window.pdf and figures/critical-window.png')
