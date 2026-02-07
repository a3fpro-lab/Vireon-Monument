# Vireon Monument (Alpha)
**Foundations of Steel.**  
This repository is the public monument: a **verifiable record** of theorems, proofpacks, and certification standards that Vireon touches—built to be replayed, audited, and extended without trust.

**License:** Apache-2.0  
**Authors:** The Architects (Inkwon Song Jr. + collaborators)

---

## What this repo is
A **proof-first** open-source archive with two hard rules:

1) **No claims without a ProofPack.**  
2) **No ProofPack without a verifier.**

If it can’t be independently checked, it doesn’t belong here.

---

## What “Verified” means here
A result is “Verified” if an independent verifier can confirm:

- **History integrity:** no reordering/deletion/insertion of steps (hash chain)
- **Content binding:** artifacts and checkpoints match logged SHA-256
- **Derivation integrity:** all certificate values recompute from raw artifacts
- **Acceptance semantics:** accept/reject decisions match the recomputed gate
- **(Optional) Authenticity:** signature checks if present

The ProofPack standard is the contract:
- `PROTOCOLS/proofpack_standard_v1.md`

---

## Repository map

### 1) Protocols (contracts)
- `PROTOCOLS/proofpack_standard_v1.md`  
  The ProofPack standard: schemas, chaining rules, derivation integrity, acceptance semantics.

### 2) ProofPacks (evidence bundles)
ProofPacks are stored under:
- `PROOFPACKS/`

Each ProofPack must include a verifier output (`VERIFY_REPORT.json` or equivalent).

### 3) Theorems (statements + proofpacks)
Theorems are stored under:
- `THEOREMS/`

Each theorem folder contains:
- a formal statement (`theorem.md` or `.tex`)
- one or more ProofPacks or links to them
- a verifier log / report

### 4) Engines (replay tools)
Engines are stored under:
- `ENGINES/`

These include:
- pack builders
- verifiers
- certificate derivation functions

Everything must be runnable from scratch.

---

## Ground rules (non-negotiable)
- No placeholders.
- No “trust me” numbers.
- Every computed quantity must be reproducible from committed artifacts or from a deterministic script.
- If a claim depends on randomness, the seed, RNG version, and environment must be recorded.

---

## Quick start (reader)
If you just want to verify a ProofPack:
1) Open a pack under `PROOFPACKS/`
2) Read `run.json`
3) Inspect `updates.jsonl`
4) Run the verifier referenced by the pack (engine folder or CLI)
5) Confirm the verifier reports `ok: true`

---

## Why this matters
Most “breakthrough” repos fail because:
- claims can’t be reproduced,
- history is editable,
- numbers are not derivable from raw evidence,
- verification is social, not mechanical.

Vireon Monument is built so that **truth survives the author**.

---

## Status
**Alpha:** structure and contracts are live.  
Next: formal theorem folders + canonical proofpack registry + deterministic replay engines.
