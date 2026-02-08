# Proofpack PP001 — Kernel Alpha Attestation (Theorem 001)

**Targets**
- Theorem: `THEOREMS/001-folding-descent-kernel/README.md`
- Index: `THEOREMS/INDEX.md`
- Engine: `ENGINES/ENGINE.md`

**Goal**
This proofpack provides a **tamper-evident closure** over the canonical files defining the Kernel layer.
If any targeted file changes, the manifest verification must fail.

**What is verified**
1. File hash integrity for every file listed in `MANIFEST.json`
2. The proofpack is bound to the theorem ID and canonical index

**Verifier**
- Build: `python tools/make_manifest.py`
- Verify: `python tools/verify_manifest.py`

**Status**
Alpha — integrity closure (hash-based). Authenticity signatures are not required at this stage.
