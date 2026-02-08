# Theorem 006 — Chained Ledger Integrity (Non-Reorderable History)

Status: Alpha  
License: Apache-2.0  
Authors: The Architects  

---

## 1) Setup

Let a **run** be defined by a JSON object `run` (the “genesis record”).  
Define:

- `G := sha256(canonical_json(run))`  (the **genesis hash**)
- A sequence of **rows** `r_1, r_2, ..., r_n`, where each row is a JSON object.

Each row has fields:

- `prev_hash` (a hex digest string)
- `payload` (arbitrary structured content)
- `row_hash` (a hex digest string)

Define the canonical hash of a row by:

- `H(r) := sha256(canonical_json(r_without_row_hash))`

The ledger rule is:

- `r_k.prev_hash = G` if `k=1`, and `r_k.prev_hash = r_{k-1}.row_hash` if `k>1`
- `r_k.row_hash = H(r_k)`

A **verifier** checks these equalities for all rows in order.

---

## 2) Theorem (Chaining Prevents Reorder / Deletion / Insertion)

**Theorem 006 (Ledger Order Integrity).**  
Assume `sha256` is collision-resistant. If a verifier accepts a ledger `(run, r_1, ..., r_n)` under the rules above, then:

1. **No reordering**: Any permutation of rows (that changes their order) will be rejected.
2. **No deletion**: Removing any row will be rejected (unless all subsequent rows are also removed, truncation).
3. **No insertion**: Inserting any additional row anywhere will be rejected unless the adversary can produce a collision for `sha256`.

Equivalently: the accepted ledger uniquely defines a single hash-linked history from `G` to `r_n.row_hash`.

---

## 3) Proof

### (1) No reordering
Suppose we reorder rows. Then there exists some index `k` where the row occupying position `k` is not the original `r_k`.  
But the verifier requires `row.prev_hash` at position `k` to equal the `row_hash` of position `k-1`. Since the reordered row’s `prev_hash` was committed for a different predecessor, the equality fails unless two different predecessors share the same `row_hash`, which would imply a collision (or second-preimage) against `sha256` under canonical encoding.

### (2) No deletion (except truncation)
If row `r_j` is removed while keeping `r_{j+1}`, then the verifier checks:
`r_{j+1}.prev_hash == r_j.row_hash`.  
But `r_j` is missing, so the predecessor hash that should be present in the chain is absent. To fix it, the adversary must change `r_{j+1}.prev_hash`, which changes `H(r_{j+1})` and therefore requires changing `r_{j+1}.row_hash`, and then similarly all later rows. That creates a new ledger, not the same accepted ledger.

If instead all rows after `r_{j-1}` are removed, this is truncation and remains a valid prefix ledger.

### (3) No insertion
If a new row is inserted between `r_{k-1}` and `r_k`, then either:
- `r_k.prev_hash` no longer matches its predecessor, so verification fails, or
- the adversary changes `r_k.prev_hash` to match the inserted row, which changes `H(r_k)` and forces a cascade of changes to all subsequent rows.

To insert without changing later rows would require making the inserted row’s hash equal to the original `r_{k-1}.row_hash` while also preserving `r_k.prev_hash`, which again demands a collision/second-preimage against `sha256` under canonical encoding.

Therefore accepted ledgers are non-reorderable, non-insertable, and non-deletable except by truncation. ∎

---

## 4) Operational Meaning

This theorem is the *history backbone* for all Monument proofpacks:

- If your update log is chained, auditors can verify you didn’t rewrite history.
- “Truth” is not “someone said it happened”; it is a verifiable path of hashes.
- This guarantees **sequence integrity**, not **value correctness** (that is handled by derivation integrity in a separate theorem).

---

## 5) Monument Linkage

This theorem binds directly to:
- **Theorem 004 — Derivation Integrity (Replay-Correct Certificates)** (value correctness)
- **Theorem 005 — PAC-Certified Policy Improvement** (accept/reject semantics logged per step)

Together: chained history + replayed derivations = audit-grade certification.
