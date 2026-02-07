# Contributing to Vireon-Monument (Version Alpha)

This repo is a public, open-source **monument**: proofs, theorems, kernels, and verifiable artifacts built under the VIREON framework.

We accept contributions—but only if they meet the same standard we demand from ourselves:
**steel foundations, not vibes.**

---

## 1) What this repo is (and is not)

### ✅ This repo is for:
- Formal theorems, definitions, and proofs (math / CS / systems theory).
- Reproducible “proofpacks” (hashable artifacts, manifests, verification scripts).
- Clear links between theory ↔ implementation (kernel → binding → certificate).
- Minimal, verifiable demos (small environments like CartPole or synthetic tests).

### ❌ This repo is NOT for:
- Placeholder text, “TODO later,” or hand-wavy claims.
- Unverifiable “trust me” results.
- Copy-pasted content without citation and ownership clarity.
- Anything that cannot be independently checked.

---

## 2) Contribution types

### A. Theorem/Proof contributions
A theorem contribution must include:
1. **Statement** (precise assumptions + conclusion)
2. **Definitions** (all symbols defined)
3. **Proof** (complete, checkable, no missing steps)
4. **Dependencies** (what prior lemmas/results it uses)
5. **Verification notes** (what would falsify it; edge cases)

### B. Proofpack contributions (recommended)
A proofpack contribution must include:
- An **artifact directory** containing:
  - `MANIFEST.json` (required)
  - All referenced files (code, logs, checkpoints, data)
  - A verification script or command that reproduces checks
- A **verifier** that can be run by an outsider, without private context.

We prefer: deterministic code + fixed seeds + explicit environment notes.

---

## 3) File/Directory conventions (Alpha)

Use this structure:

- `theorems/`
  - `T0001_<short_name>/`
    - `theorem.md` or `theorem.tex`
    - `proof.md` or `proof.tex`
    - `references.bib` (optional but encouraged)
    - `NOTES.md` (optional)

- `proofpacks/`
  - `P0001_<short_name>/`
    - `PROOFPACK/`
      - `MANIFEST.json`
      - `ARTIFACTS/` (raw outputs)
      - `CODE/` (scripts used)
      - `VERIFY/` (verification instructions)
    - `README.md` (what this pack demonstrates, how to verify)

- `tools/`
  - `make_manifest.py` (creates/updates manifests)
  - `verify_manifest.py` (verifies manifests)
  - other verifiers/checkers

No random top-level dumps. Keep it clean.

---

## 4) The MANIFEST rule (no exceptions)

If your contribution includes a `PROOFPACK/` directory, it must include:

- `PROOFPACK/MANIFEST.json`

The manifest must list:
- every file path included in the pack
- sha256 for each file
- created timestamp
- pack schema version

If CI fails because MANIFEST is missing or wrong, the PR will not be merged.

---

## 5) Reproducibility requirements

If you claim “this produces result X,” you must provide:
- exact command(s) to run
- required dependencies
- expected output files
- expected verification command

If it’s stochastic:
- set seeds
- log seeds
- document variance and failure modes

---

## 6) Citations and attribution

If you build on existing work:
- cite the paper/book/link
- clearly state what is new vs. what is standard
- do not plagiarize (ever)

---

## 7) PR checklist (required)

Before opening a PR, confirm:
- [ ] No placeholders / no TODOs
- [ ] All symbols defined
- [ ] Proof is complete OR explicitly labeled as “conjecture” (rare)
- [ ] Proofpack has `MANIFEST.json` if applicable
- [ ] Verification command works
- [ ] CI passes

---

## 8) Style: “Frank, not Judy”

We write:
- direct
- exact
- falsifiable

No fluff.

---

## 9) License

By contributing, you agree your contribution is licensed under:
**Apache License 2.0** (see `LICENSE`).

---

## 10) Maintainers

**The Architects**  
Primary: Inkwon Song Jr.  
Co-creator: Inkwon Song
