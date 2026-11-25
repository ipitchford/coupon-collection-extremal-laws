# Review summary (internal, AI-assisted)

This file records the internal checking of this candidate before release, without any ratings. It is not peer review,
independent reproduction or formal verification. All review steps were carried out by AI systems (Claude) under the
Evidence Press publication protocol; no external referee has seen the paper.

## What was done (24–25 November 2026)

1. **Combined five-role review panel** (editor, methodology, domain, perspective and devil's-advocate roles in one
   Claude review). No role found an error in a stated result. The main objections concerned credit, positioning and
   scope (below).
2. **Exact checks** by the lead: the source bundle's checks relied on `assert` (which `python -O` disables), so they
   were rewritten with explicit checks in `code/verify_coverage.py` and extended (random competitor laws, the 1 + n/s
   family, Lemma 5.1 and Proposition 5.2 in exact arithmetic, the gap series, finite full-model values). Negative
   controls (47/12 changed to 47/13; 163/30 changed to 163/31) make the scripts exit 1 under `-O`.
3. **One revision round** with three extensions: the universal excess bound (Theorem 5.4 with Lemmas 5.1 and 5.3 and
   Proposition 5.2), the exhaustive exact search of small fair mechanisms (Proposition 6.1, Table 2, with its C
   enumeration and exact-rational certificate) and a second exact minimum family (Theorem 7.5). A new introduction,
   a summary table, a notation section and an opening sentence for every section were added.
4. **Re-review** of every revision item, and a **proof audit** of the new proofs. The audit found one description
   error (the account of the star mechanism in Remark 4.2) and two gaps (the derivation of the rounding-error bound in
   Section 6; "the" versus "a" slowest law at (7,3)); all three were fixed. All other new proofs passed.
5. **Source update.** Finner (1992) was obtained and read; Lemma 7.1 now cites Finner's Theorem 2.1 and (3.1)
   directly, with Pelekis, Ramon and Wang kept as a restatement. Only the manuscript changed.

No Astra/Codex review took place for this candidate.

## Main objections and how they were resolved

| Objection | Resolution |
|---|---|
| Barak-Pelleg and Berend's star mechanism already reaches k + 1 in its windows | Credited in Remark 4.2, the introduction and Table 1; the new content is stated as the matching upper bound, every λ including λ < 1, every n and the 1/e peak |
| The fast-side result proves a named conjecture but did not say so | The Fang–Chang conjecture is stated as proved with uniqueness, including the pairing case, in the abstract, introduction and Section 7 |
| The h = 1 product bound is known | Stated plainly: it is Pelekis–Ramon–Wang Theorem 2.6 after Poissonisation, and the inequality is cited to Finner |
| A second exact minimum (1 + n/s when n − s divides n) was missed | New Theorem 7.5, with the combined bound max{xH_x, 1 + x}; Berend and Sher credited for the law and its mean |
| Literature gaps | Falgas-Ravry–Larsson–Markström added; the Bonferroni-type bound presented as classical with no novelty claimed; the pairing-conjecture history attributed through Fang–Chang, which was read |
| Proofs compressed in places | The mean-maximiser characterisation, the difference argument in Theorem 3.4 and the j = k term in the critical upper bound were written out |
| Finite-size meaning of 1/e | Finite-n values and a slow-convergence remark added: 1/e is a limit, not a finite-n guarantee |
| Checks would pass vacuously under `python -O` | Rewritten with explicit checks and negative controls |

## What remains open or unchecked

- Quantitative rates for the critical windows; the thinned projective construction is existential and was not
  instantiated.
- The exact slowest fair law without a design beyond the small cases searched.
- Whether the excess over the full model can grow without bound for small packages.
- The exact minimum when neither s nor n − s divides n, and tail ordering for general divisible capacities.
- The novelty check rests on searches of limited scope ([RESEARCH_GATES.json](RESEARCH_GATES.json)).
- No human specialist has checked the proofs.
