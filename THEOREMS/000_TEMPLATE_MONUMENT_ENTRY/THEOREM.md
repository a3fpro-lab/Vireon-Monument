# THEOREM TEMPLATE (Monument Entry)

**ID:** 000  
**Status:** TEMPLATE  
**Type:** THEOREM / LEMMA / CONJECTURE / BINDING  
**Version:** Alpha  
**Authors:** The Architects  
**License:** Apache-2.0

---

## Statement

> **Theorem (Template).**  
> Replace this block with the exact statement.  
> Use explicit quantifiers, domains, constants, and assumptions.

---

## Assumptions

List every assumption explicitly. Examples:
- Smoothness / Lipschitz
- Bounded variance
- Convexity / monotonicity
- Feasibility / non-emptiness
- Measurability / integrability

---

## What this entry guarantees

- What is proven?
- What is not claimed?
- What fails if assumptions fail?

---

## Verification mode

Choose exactly one:

### Mode 1 — Formal proof only
This entry is verified by the proof in `PROOF.md`.

### Mode 2 — Proof + Proofpack
This entry is verified by:
- the proof in `PROOF.md`
- a proofpack in `PROOFPACK/`
- a verifier (CI runs it)

---

## Files

- `THEOREM.md` (this file)
- `PROOF.md`
- `REFERENCES.md`
- optional: `PROOFPACK/` and `tools/`
