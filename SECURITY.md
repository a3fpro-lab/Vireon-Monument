# Security Policy — Vireon-Monument (Version Alpha)

This repository contains **verification tooling and proofpack artifacts**. Security issues here can mean:
- forged “verified” results
- tampered proofpacks
- supply-chain dependency risk
- CI manipulation

We take that seriously.

---

## Supported Versions

Version Alpha is under active development.
Security fixes may land without warning; keep your fork updated.

---

## Reporting a Vulnerability

If you find a vulnerability that could:
- bypass verification
- forge manifests or hashes
- alter acceptance logic while keeping “verified: true”
- manipulate CI to publish false green checks

**Do NOT open a public issue.**

Instead, report privately:

- **Email:** echoaseternity@gmail.com  
- **Subject:** `SECURITY: Vireon-Monument <short description>`

Include:
1. What you found (clear summary)
2. Where it is (file paths, functions)
3. Impact (what breaks / what can be forged)
4. Reproduction steps (minimal PoC)
5. Suggested fix (if you have one)

---

## Disclosure Policy

We follow responsible disclosure:
- We acknowledge receipt
- We validate the report
- We patch and ship a fix
- We publish a security note after mitigation (when safe)

If the issue affects published proofpacks, we may:
- mark them as compromised
- rotate verification keys
- add a “revoked packs” list

---

## Threat Model (Alpha)

We assume:
- An attacker may modify files inside a proofpack directory
- An attacker may reorder/insert/delete update rows
- An attacker may attempt to forge “certificates” without raw artifacts
- CI logs and build outputs are visible to the public

We defend with:
- sha256 file hashing
- manifests
- chained ledgers (when enabled)
- deterministic recomputation (derivation integrity)
- signature verification (when enabled)

But **Alpha is not forensic-grade** yet.

---

## Hardening Roadmap (High Priority)

1. Content-addressed artifacts / checkpoint hashing
2. Row-chain / merkle commitments at scale
3. Ed25519 signatures with key rotation strategy
4. Reproducible build environments (pinned deps, lockfiles)
5. External verification runner (no GitHub trust required)

---

## Non-goals

This repository does not promise:
- protection against a fully compromised machine producing false raw data
- protection against hardware-level rootkits
- safety guarantees for RL policies in the real world

This repo provides **verification of artifacts and derivations**, not omniscience.

---

## Thanks

If you report a real issue, you’ll be credited (unless you request anonymity).
