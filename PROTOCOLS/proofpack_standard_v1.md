# VIREON ProofPack Standard v1 (Alpha)
**Status:** Alpha (stable contract for public OSS release)  
**License:** Apache-2.0 (repo-level)  
**Authors:** The Architects (Inkwon Song Jr. + collaborators)

This document defines the **minimum required structure, semantics, and verification rules** for a VIREON ProofPack.

A ProofPack is a **proof-carrying evidence bundle**:
- history is tamper-evident (hash chain),
- files are content-bound (SHA-256),
- derived certificates are replayable (derivation integrity),
- and the verifier can independently reproduce the acceptance gate.

---

## 1) Definitions

### ProofPack
A directory containing:
- a run anchor (`run.json`),
- an append-only update ledger (`updates.jsonl`),
- artifacts referenced by ledger rows (e.g., batch samples),
- checkpoints referenced by ledger rows,
- a cryptographic closure (`sha256sum.txt`, `manifest.json`, optional signature).

### Verified
A ProofPack is **Verified** if a compliant verifier:
1. validates schemas,
2. validates hash chain (no reorder/delete/insert),
3. validates SHA-256 of every referenced file,
4. recomputes every derived certificate from raw artifacts and matches logged values,
5. validates acceptance semantics, and
6. validates manifest closure (and signature if present).

---

## 2) Required Directory Layout

A compliant ProofPack directory MUST contain:
