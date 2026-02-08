# Vireon Monument Engine — Version Alpha

This file defines the non-negotiable operating rules of **Vireon Monument**.
It is the “steel-core contract” of the repository: what counts as a real entry, what is canonical, and what must be checkable.

**Authors:** The Architects (Inkwon Song Jr. and collaborators)  
**License:** Apache-2.0

---

## 0) Purpose

Vireon Monument is a proof-first repository. It is not built to “host writing.”
It is built to host **claims that remain checkable under adversarial review**.

This engine enforces three things:

1. **Canonical indexing** (nothing “exists” unless indexed)
2. **Audit structure** (every theorem has a fixed home and format)
3. **CI sanity** (no placeholder text leaking into real entries)

---

## 1) Core Objects

### 1.1 Monument Entry
A Monument Entry is a theorem/proof package that lives at:

- `THEOREMS/NNN-<slug>/README.md`

Where:
- `NNN` is a 3-digit permanent ID.
- `<slug>` is a short, stable name.

A valid entry includes:
- Title + status + authors + license
- Definitions / assumptions
- Theorem statement
- Proof (or proof sketch, explicitly labeled)
- “Operational meaning” (what it certifies / what it can be used to verify)

### 1.2 Canonical Index
The file `THEOREMS/INDEX.md` is the canonical registry.
If an entry is not referenced there, it is not part of the Monument.

Index rules:
- Every listed entry must match an existing folder path.
- IDs are never reused.
- IDs never change once assigned.

### 1.3 Proofpack (optional but preferred)
A proofpack is an evidence bundle that can be verified independently.

Typical properties (when present):
- File hashes (sha256)
- Manifest binding the exact content
- Replay or recomputation path (when computation is involved)
- Chain integrity for sequences of steps (when applicable)

---

## 2) Steel Rules (Non-Negotiable)

### Rule A — No Silent Claims
A claim is not valid unless it is written in a theorem entry and referenced in the index.

### Rule B — IDs Are Permanent
Once `NNN` is assigned, it is permanent. Never renumber old entries.
If order changes, fix the index ordering, not the IDs.

### Rule C — Checkability Over Style
Clarity matters, but checkability is mandatory.
If the reader cannot identify assumptions and verify the logical steps, the entry is not Monument-grade.

### Rule D — No Placeholder Leakage
Placeholder text must never appear inside real theorem entries or the index.
Place drafts in a separate scratch area (outside THEOREMS) until ready.

### Rule E — Deterministic Repro When Computation Exists
If an entry includes computed quantities, the entry must define:
- the inputs (artifacts)
- the deterministic derivation procedure
- how an external party reruns it

---

## 3) Repository Layout

- `README.md` — front door
- `ENGINES/ENGINE.md` — this contract
- `THEOREMS/INDEX.md` — canonical registry
- `THEOREMS/NNN-<slug>/README.md` — theorem bodies

Optional folders (as the Monument grows):
- `TOOLS/` or `tools/` — verification scripts for proofpacks
- `PROOFPACKS/` — evidence bundles, one per system or experiment

---

## 4) CI Sanity Policy

The CI exists to prevent the repository from drifting into “looks good” territory.

Minimum checks (Alpha):
- Index file exists.
- THEOREMS directory exists.
- Placeholder text does not appear in theorem entries or the index.

As the Monument grows, CI should expand to:
- enforce directory naming conventions
- verify proofpack manifests (sha256)
- run replay verifiers for computational certificates

---

## 5) Contribution Standard

Every PR should do at least one of the following:
- Add a new indexed theorem entry with a full proof (or explicitly labeled proof sketch)
- Strengthen a proof (tighten assumptions, remove ambiguity, improve auditability)
- Add verification artifacts (hash manifests, replay code, deterministic derivation)

If it doesn’t increase checkability, it doesn’t belong here.

---

## 6) Alpha Definition

Alpha means:
- The structure is stable enough to build on.
- The rules are enforced.
- Theorem count is still small, but the standards are already strict.

This repo is intended to grow without relaxing standards.
That is the point.
