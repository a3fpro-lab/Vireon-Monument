# Theorem Pack 00 — ProofPack Integrity (Alpha)

**Status:** Alpha (foundation steel)  
**License:** Apache-2.0  
**Authors:** The Architects (Inkwon Song Jr. et al.)  
**Scope:** This theorem formalizes what a “ProofPack” guarantees when built with (i) per-file hashing, (ii) append-only row chaining, and (iii) deterministic recomputation rules.

---

## 0. Definitions

### 0.1 Canonical JSON
A JSON object is **canonicalized** by:
- Sorting keys lexicographically
- No extra whitespace
- UTF-8 encoding

We write:
- `canon(x)` = canonical JSON bytes for object `x`
- `H(b)` = SHA-256 hex digest of bytes `b`

### 0.2 ProofPack Directory
A **ProofPack** is a directory `D` containing:

1. **run.json** — the run configuration and declared semantics  
2. **updates.jsonl** — newline-delimited JSON rows (append-only ledger)  
3. **artifacts/** — raw evidence files referenced by ledger rows  
4. **checkpoints/** — model/policy snapshots referenced by ledger rows  
5. **sha256sum.txt** — optional file hash list (redundant but useful)  
6. **manifest.json** — a final closure list of all files with hashes (may be signed)

### 0.3 Update Row (Ledger Entry)
Each ledger row `r_k` (k = 1..N) includes at minimum:

- `prev_row_hash` (string)
- `row_hash` (string)
- `theta_old_path`, `theta_old_sha256`
- `theta_try_path`, `theta_try_sha256`
- `artifact_*_path`, `artifact_*_sha256` (for each required artifact)
- `pac` (or certificate fields)
- `accepted` (boolean)

**Row hash rule:**
Let `r_k^-` be `r_k` with `row_hash` field removed.
Then:
- `row_hash = H(canon(r_k^-))`

**Chain rule:**
Let `g = H(run.json bytes)` be the genesis hash.
Then:
- `r_1.prev_row_hash = g`
- `r_k.prev_row_hash = r_{k-1}.row_hash` for all k > 1

### 0.4 Deterministic Derivation Rule (Replayability)
A ProofPack declares a deterministic function:

`DERIVE(run.json, row_k, referenced_artifacts) -> certificate_fields`

The verifier recomputes the certificate fields from artifacts and requires exact match
(up to a declared tolerance if using floating point).

---

## 1. Theorem — ProofPack Integrity

### Theorem 1 (ProofPack Integrity Theorem)
Assume a ProofPack `D` satisfies:

**(A) File Binding**
Every referenced checkpoint/artifact file path in each row exists,
and its SHA-256 matches the hash recorded in the row.

**(B) Row Chaining**
`prev_row_hash` is correct for every row, starting from genesis `g = H(run.json)`.

**(C) Row Hash Correctness**
For every row `r_k`, `row_hash = H(canon(r_k^-))`.

**(D) Deterministic Derivation Integrity**
For every row `r_k`, the verifier recomputes the certificate fields by
`DERIVE(...)` from the referenced artifacts and obtains the same values as logged.

Then the ProofPack guarantees:

1. **(History Non-Rewriteability)**  
   No adversary can delete, reorder, or insert ledger rows in `updates.jsonl`
   without detection by the verifier.

2. **(Artifact/Checkpoint Non-Substitutability)**  
   No adversary can swap any referenced artifact/checkpoint content
   without detection by the verifier.

3. **(Certificate Non-Forgery under Replay Rule)**  
   No adversary can alter logged certificate fields while keeping artifacts unchanged
   without detection by the verifier.

---

## 2. Proof

### Proof of (1): History Non-Rewriteability
Assume an adversary modifies `updates.jsonl` by deleting, reordering, or inserting rows.

- If any row content changes, then by (C) the `row_hash` must equal
  `H(canon(r_k^-))`. Any mismatch is detected.
- By (B), each row `r_k` must point to the *exact* hash of the previous row.
  Reordering or insertion breaks at least one `prev_row_hash` equality.
- Deleting any row makes the next row’s `prev_row_hash` refer to a missing hash,
  breaking the chain.

Therefore any such modification is detected. ∎

### Proof of (2): Artifact/Checkpoint Non-Substitutability
Suppose an adversary replaces a referenced file `f` with different bytes `f'`.

By (A), the verifier recomputes `H(f')` and compares it to the row’s recorded hash.
Because SHA-256 is collision-resistant in practice, changing bytes changes the digest
with overwhelming probability, so the mismatch is detected. ∎

### Proof of (3): Certificate Non-Forgery under Replay Rule
Suppose an adversary changes certificate fields in row `r_k` but does *not* change artifacts.

- By (D), the verifier recomputes certificate fields from the artifacts using `DERIVE`.
- Since artifacts are unchanged, the recomputed values are unchanged.
- The verifier compares logged vs recomputed and detects any mismatch.

Thus certificate forgery without changing artifacts is detected. ∎

Combining (1)–(3) establishes the theorem. ∎

---

## 3. Practical Meaning (What This Lets You Claim)

If a ProofPack verifies, you can truthfully state:

- “The ledger is append-only: the sequence of updates is fixed.”
- “The logged artifacts/checkpoints are content-bound: no silent substitution.”
- “The logged certificates are replayable from raw evidence: no ‘trust me’ fields.”

**Important boundary:**  
This does **not** prove the environment or hardware was honest — it proves that whatever
was logged is internally consistent, non-rewritable, and replayable under the declared rules.

---

## 4. Minimal Verifier Checklist (Executable Spec)
A verifier MUST:

1. Compute `genesis = sha256(run.json)`
2. For each row in order:
   - Check `prev_row_hash` matches expected
   - Recompute `row_hash` from canonicalized row-without-row_hash
   - For each referenced file: check existence + sha256 match
   - Recompute `certificate = DERIVE(...)` and compare to logged certificate
3. Optionally verify `manifest.json` + signature if present

---

## 5. Versioning
- **Alpha:** establishes integrity + replayability logic (this file).
- **Beta:** adds signatures (authenticity) and stronger statistical certificates.
- **v1:** merges into a unified “Monument Standard” with multiple theorem packs.

---

## 6. Attribution
**The Architects**  
- Inkwon Song Jr.
