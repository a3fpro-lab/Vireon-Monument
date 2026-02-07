# Vireon Monument — Core Charter (Version Alpha)

**Repository:** Vireon-Monument  
**License:** Apache-2.0  
**Authors:** The Architects (Inkwon Song Jr. + collaborators)  
**Status:** Version Alpha — foundations only, no placeholders.

---

## 1) What This Is

**Vireon Monument** is a public, auditable structure for:
- **Theorems, proofs, and bindings** Vireon has touched
- **Verification-first artifacts** (“proofpacks”) that make claims replayable
- A **steel-core standard**: every claim must be either proven, or explicitly labeled as a conjecture + evidence protocol

This repo is not a blog.  
It is a **monument**: curated, verifiable, and built to survive hostile review.

---

## 2) What This Is NOT

- Not “trust me” theory.
- Not motivational writing.
- Not vague frameworks.
- Not “AI said so.”
- Not a place for unverified overclaims.

If a claim can’t be defended, it doesn’t go in the Monument.

---

## 3) Ground Rules (Non-Negotiable)

### Rule A — Every claim is classified
Each claim must be one of:
1. **THEOREM (PROVEN):** complete proof included or formally referenced
2. **LEMMA (PROVEN):** supporting result
3. **CONJECTURE:** clearly labeled with falsification / evidence plan
4. **BINDING:** a mapping from a modern system to a rigorous mathematical object + theorems it activates

### Rule B — Every proof must be replayable
A theorem is “Monument-grade” only if:
- the statement is precise
- assumptions are explicit
- proof is complete or references a stable source
- if computation is used, it ships as a **proofpack** with a verifier

### Rule C — No placeholders
No “TODO: proof later.”  
No “fill in later.”  
If it’s not complete, it does not enter the Monument.

---

## 4) The Monument Format (What We Will Add Next)

This repo will contain **entries** that look like:

- `THEOREMS/<ID>_<NAME>/`
  - `THEOREM.md` (statement + assumptions)
  - `PROOF.md` (full proof)
  - `REFERENCES.md` (citations, stable)
  - `PROOFPACK/` (optional)
    - `run.json`
    - `updates.jsonl`
    - `manifest.json`
    - `sha256sum.txt`
    - `VERIFY_REPORT.json`
  - `tools/` (verifier, manifest builder)

**A theorem can be pure math (no proofpack) or computation-assisted (proofpack required).**

---

## 5) Verification Standard (Alpha)

We accept two verification modes:

### Mode 1 — Formal proof only
- Proof must stand alone.
- Any external reference must be stable (book, paper, DOI/arXiv, etc.).

### Mode 2 — Proof + proofpack
- Proofpack must contain:
  - tamper-evident hashes
  - deterministic derivation or recomputation
  - an independent verifier script
- The verifier must output **verified: true** when run in clean CI.

---

## 6) The Vireon Kernel (Why This Exists)

The point of the Monument is to show—cleanly and publicly—that modern systems
can be bound to rigorous structures (descent, correspondence, equilibrium, etc.)
and that the relevant theorems “fire” under explicit conditions.

**If it cannot be audited, it does not count.**

---

## 7) Version Alpha Commitments

Alpha will ship:

1. A clean repo skeleton (done)
2. A single “Monument Entry” template (next)
3. One fully completed entry (no blanks)
4. CI that verifies the entry end-to-end

Alpha’s goal is not breadth.
Alpha’s goal is a **standard that cannot be bullied.**

---

## 8) Contribution Policy

Contributions are welcome if they:
- follow the classification rules
- include complete proofs or complete verification artifacts
- avoid sensational claims

If a contribution weakens the verification bar, it will not be merged.

---

## 9) The Motto

**Steel foundations. No blanks. No placeholders. Replayable truth.**
