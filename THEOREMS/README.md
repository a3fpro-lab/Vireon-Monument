# Vireon Monument — Theorems Index (Alpha)

This folder contains **ProofPacks**: self-contained theorem units built to be:
- readable (definitions → theorem → proof),
- auditable (verification boundary stated explicitly),
- expandable (each pack can evolve without breaking the Monument).

## How ProofPacks are structured

Every pack **must** include these sections:

1. **Definitions**
2. **Theorem**
3. **Proof**
4. **Practical Meaning**
5. **Verification Boundary** (what is guaranteed, under what assumptions, what is *not* claimed)

The canonical list of packs and required structure is in:
- `MONUMENT_MANIFEST.json`

---

## Packs (Alpha)

### 00 — ProofPack Integrity Theorem
**Path:** `THEOREMS/00_PROOFPACK_INTEGRITY/README.md`

**Claims (high level):**
- History non-rewriteability via row chaining (append-only, reorder-resistant).
- Artifact/checkpoint non-substitutability via SHA-256 binding.
- Certificate non-forgery via deterministic derivation replay from raw artifacts.

Status: **Alpha**

---

## Roadmap (Alpha → Steel)

Next packs planned (titles only, content will be added as complete packs — no placeholders):
- **01 — Descent Kernel (VIREON core fold → progress)**
- **02 — Gap-to-Progress Rate Theorem (power-law rates)**
- **03 — Attention as Hopfield Retrieval (energy descent binding)**
- **04 — Diffusion as Correspondence Inversion (training + sampling)**
- **05 — PAC-Certified Policy Improvement (RL gate)**
- **06 — Anytime-Valid Confidence Sequences (α-spending without horizon)**
- **07 — Derivation Integrity Law (recompute-from-raw, verifier replay)**

Each will arrive as a full ProofPack with proof + boundary.
