# Vireon Monument — Version Alpha

[![verify](https://github.com/a3fpro-lab/Vireon-Monument/actions/workflows/verify.yml/badge.svg)](https://github.com/a3fpro-lab/Vireon-Monument/actions/workflows/verify.yml)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Release](https://img.shields.io/github/v/release/a3fpro-lab/Vireon-Monument?include_prereleases=true)](https://github.com/a3fpro-lab/Vireon-Monument/releases)
[![Stars](https://img.shields.io/github/stars/a3fpro-lab/Vireon-Monument?style=social)](https://github.com/a3fpro-lab/Vireon-Monument/stargazers)
**Vireon Monument** is an open, proof-first repository: a growing foundation of *theorems, proofs, and verification artifacts* developed under the Vireon logic.

This repo is built to be:
- **Steel-core**: every claim lives beside a checkable artifact
- **Tamper-evident**: proofpacks are hashed and tracked
- **Reproducible**: anyone can re-run the verification on their own machine
- **Open**: Apache-2.0 licensed for broad use and extension

**Authors:** The Architects (Inkwon Song Jr. and collaborators)

---

## What’s in this repo

### 1) Proof Library (Theorems + Proofs)
A curated, structured set of documents containing:
- Definitions and axioms
- Theorems and proofs
- Bridge theorems that connect to optimization, learning, and dynamical systems
- “Kernel” structure: reusable proof patterns you can bind to real systems

### 2) Proofpacks (Verification Artifacts)
A **proofpack** is a directory-level evidence bundle that can be independently verified.

This repo includes a manifest system:
- `tools/make_manifest.py` generates `PROOFPACK/MANIFEST.json`
- `tools/verify_manifest.py` verifies every file hash listed in the manifest


- Theorems Index: `THEOREMS/INDEX.md`
This makes the repository state *audit-friendly* and *tamper-evident*.

---

## Quickstart: Verify the repository state

### A) Build the manifest
```bash
python tools/make_manifest.py

B) Verify the manifest

python tools/verify_manifest.py

If verification passes, your local working tree matches the cryptographic manifest.

⸻

CI (GitHub Actions)

This repository runs an automated check on every push and pull request:
	•	builds the manifest
	•	verifies the manifest

If anything is inconsistent, CI fails.

⸻

License

Apache License 2.0 — see LICENSE.

⸻

Roadmap (Alpha)
	•	Add a structured theorem directory and index
	•	Add the first canonical proofpack(s) for:
	•	Descent / progress certificates
	•	PAC-certified improvement gates
	•	Chain integrity + derivation integrity rules
	•	Add a “monument index” that lists every theorem, its status, and its verification links

⸻

Integrity Statement

This repo is not built for vibes.
It is built for truth you can re-check.

