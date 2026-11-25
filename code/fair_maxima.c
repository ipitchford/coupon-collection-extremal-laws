/* Exhaustive search over all fair mechanisms (uniform laws on families of distinct
   s-subsets of [n] in which every point has the same degree) for small n.
   For each family it computes E T, the mean number of draws needed to cover [n], by
   the exact hitting-time recursion on covered sets, evaluated in double precision.
   Output (one block per (n,s)): number of families, the largest and second-largest
   distinct means, the smallest mean, and every family within 1e-9 of the largest
   mean (as block bitmasks). The companion script certify_fair_maxima.py re-evaluates
   the reported maximisers and the full model in exact rational arithmetic.
   Public domain (CC0) / MIT, Evidence Press. */
#include <stdio.h>
#include <stdlib.h>
#define MAXB 128
#define MAXKEEP 4096
static int n, s, m, size, target, nch;
static int blk[MAXB], deg[16], rem[MAXB + 1][16], chosen[MAXB];
static long long cnt;
static double best, second, worst;
static int nkeep;
static int keep[MAXKEEP][MAXB], keepsize[MAXKEEP];
static double keepval[MAXKEEP];

static double mean_time(void) {
    static double E[1 << 12];
    int full = (1 << n) - 1;
    E[full] = 0.0;
    for (int S = full - 1; S >= 0; S--) {
        int moves = 0;
        double sum = 0.0;
        for (int i = 0; i < nch; i++) {
            int T = S | chosen[i];
            if (T != S) { moves++; sum += E[T]; }
        }
        if (moves == 0) return -1.0;
        E[S] = (nch + sum) / moves;
    }
    return E[0];
}

static int pass;  /* 1: find the extreme values; 2: list the maximisers */

static void record(void) {
    double e = mean_time();
    if (pass == 1) {
        cnt++;
        if (e < worst) worst = e;
        if (e > best + 1e-9) { second = best; best = e; }
        else if (e < best - 1e-9 && e > second + 1e-9) second = e;
        return;
    }
    if (e > best - 1e-9) {
        if (nkeep >= MAXKEEP) { fprintf(stderr, "too many maximisers\n"); exit(2); }
        keepval[nkeep] = e; keepsize[nkeep] = nch;
        for (int i = 0; i < nch; i++) keep[nkeep][i] = chosen[i];
        nkeep++;
    }
}

static void search(int i) {
    if (nch == size) {
        for (int v = 0; v < n; v++) if (deg[v] != target) return;
        record();
        return;
    }
    if (i == m) return;
    for (int v = 0; v < n; v++) if (deg[v] + rem[i][v] < target) return;
    int t = blk[i], ok = 1;
    for (int v = 0; v < n; v++) if (((t >> v) & 1) && deg[v] >= target) ok = 0;
    if (ok) {
        for (int v = 0; v < n; v++) if ((t >> v) & 1) deg[v]++;
        chosen[nch++] = t;
        search(i + 1);
        nch--;
        for (int v = 0; v < n; v++) if ((t >> v) & 1) deg[v]--;
    }
    search(i + 1);
}

int main(int argc, char **argv) {
    if (argc != 3) { fprintf(stderr, "usage: fair_maxima n s\n"); return 2; }
    n = atoi(argv[1]); s = atoi(argv[2]);
    if (n < 2 || n > 12 || s < 1 || s >= n) { fprintf(stderr, "bad n,s\n"); return 2; }
    m = 0;
    for (int t = 0; t < (1 << n); t++) if (__builtin_popcount(t) == s) blk[m++] = t;
    if (m > MAXB) { fprintf(stderr, "too many blocks\n"); return 2; }
    for (int v = 0; v < n; v++) rem[m][v] = 0;
    for (int i = m - 1; i >= 0; i--)
        for (int v = 0; v < n; v++) rem[i][v] = rem[i + 1][v] + ((blk[i] >> v) & 1);
    best = -1.0; second = -1.0; worst = 1e300; cnt = 0; nkeep = 0;
    for (pass = 1; pass <= 2; pass++)
        for (size = 1; size <= m; size++) {
            if ((size * s) % n) continue;
            target = size * s / n;
            search(0);
        }
    printf("n %d s %d families %lld max %.17g second %.17g min %.17g maximisers %d\n",
           n, s, cnt, best, second, worst, nkeep);
    for (int k = 0; k < nkeep; k++) {
        printf("family");
        for (int i = 0; i < keepsize[k]; i++) printf(" %d", keep[k][i]);
        printf("\n");
    }
    return 0;
}
