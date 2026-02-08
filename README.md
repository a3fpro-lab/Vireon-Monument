# Vireon Monument — Version Alpha

[![monument-ci](https://github.com/a3fpro-lab/Vireon-Monument/actions/workflows/monument-ci.yml/badge.svg)](https://github.com/a3fpro-lab/Vireon-Monument/actions/workflows/monument-ci.yml)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Stars](https://img.shields.io/github/stars/a3fpro-lab/Vireon-Monument?style=social)](https://github.com/a3fpro-lab/Vireon-Monument/stargazers)

**Vireon Monument** is an open, proof-first repository: a growing foundation of **theorems, proofs, and verification artifacts** engineered under Vireon logic.

**Engine (rules of the Monument):** [`ENGINES/ENGINE.md`](ENGINES/ENGINE.md)  
**Theorems Index (canonical registry):** [`THEOREMS/INDEX.md`](THEOREMS/INDEX.md)

**Start here:** [`THEOREMS/INDEX.md`](THEOREMS/INDEX.md)

**Authors:** The Architects (Inkwon Song Jr. and collaborators)  
**License:** Apache-2.0

---

## What this repository is

This repo is built to be:

- **Steel-core** — every claim lives beside a checkable structure
- **Tamper-evident** — changes are detectable (manifest + audit rules)
- **Reproducible** — others can re-run checks and reach the same pass/fail outcome
- **Open** — Apache-2.0 for broad use, extension, and downstream integration

This is **not** a vibes repo.  
It is a repository for truth you can re-check.

---

## Structure

### 1) Theorems (Proof Library)
All canonical entries live under:

- `THEOREMS/NNN-<slug>/README.md`
- `THEOREMS/INDEX.md` is the canonical entry point

Each theorem entry is intended to be:
- clearly stated
- proven (or explicitly marked as queued/draft)
- linked to what it binds to (optimization, learning, certificates, etc.)

### 2) Proofpack / Integrity Tooling
This repository includes tooling to make tampering detectable via a cryptographic manifest:

- `tools/make_manifest.py` builds `PROOFPACK/MANIFEST.json`
- `tools/verify_manifest.py` verifies every file hash listed in the manifest

This makes a repository state **audit-friendly**: anyone can confirm whether their checkout matches the recorded manifest.

> Note: the Monument repo is intentionally docs-first. It is not required to be installable as a Python package.

---

## Quickstart: Verify repository integrity

### A) Build the manifest
```bash
python tools/make_manifest.py
