# Theorem 004 — Derivation Integrity (Replay-Correct Certificates)

Status: Alpha  
License: Apache-2.0  
Authors: The Architects

---

## 1) Purpose

Theorem 003 makes a *probabilistic* statement: if the certificate passes, then the true update value is nonnegative with confidence \(1-\alpha\), **assuming the logged artifacts are the ones actually used**.

But a second failure mode exists:

> A training process could log “nice looking” certificate values even if they were not computed from the raw artifacts.

Theorem 004 eliminates that loophole by enforcing:

- **Artifact binding** (raw files are hash-locked)
- **Derivation binding** (the computation code is hash-locked)
- **Replay correctness** (a verifier recomputes and must match)

This is correctness under audit, not trust.

---

## 2) Objects and Hashes

Fix a step \(k\). Let the raw evidence set be:

- Artifact files \(A_k := \{a_{k,1},\dots,a_{k,m}\}\) (e.g., deltaL/eps/KL sample logs)
- Checkpoint files \(C_k := \{c_{k,old},c_{k,try}\}\)
- A deterministic derivation program \(D\) that computes certificate fields from artifacts
  - Example: `compute_pac_from_artifacts()` in a repository file

Define SHA-256 hashing:

- \(h(\cdot)\) = SHA-256 hex digest of the exact file bytes.
- For a set of files \(S\), define its **multihash**:
  \[
  H(S) := h\big(\text{canonical\_json}(\{(p, h(p)) : p\in S\})\big).
  \]
(Equivalently: hash the sorted list of file paths + file hashes.)

The update row \(R_k\) MUST record:

1. The per-file hashes \(h(a_{k,i})\) for all artifacts
2. The per-file hashes \(h(c_{k,old}), h(c_{k,try})\)
3. The derivation program hash \(h(D)\) (exact bytes of the derivation script/function source bundle)
4. The derived certificate fields \(Z_k\) (the PAC fields, acceptance, etc.)

---

## 3) Deterministic Derivation Rule

Assume the derivation program \(D\) is deterministic:

\[
Z_k = D(A_k; \theta),
\]

where \(\theta\) are parameters embedded in the run configuration (e.g., \(\alpha,\lambda_\epsilon,\lambda_\delta\), clipping bounds).

Deterministic means:

- same input files + same config + same code bytes ⇒ identical output bytes (or numerically identical up to declared tolerance)

---

## 4) Verifier Rule (Replay)

A verifier takes a proofpack directory and performs:

1. **Hash validation**
   - Recompute every file hash and confirm it matches what is recorded in each row.
2. **Derivation validation**
   - Confirm the derivation program hash \(h(D)\) matches the recorded hash.
3. **Replay**
   - Recompute \(Z_k' := D(A_k; \theta)\).
4. **Exact-match check**
   - Require \(Z_k' = Z_k\) (or \(|Z_k' - Z_k|\le \tau\) for declared numeric fields).

If any check fails, verification fails.

---

## 5) Theorem (Replay-Correctness and Non-Fabrication)

### Theorem 004 (Derivation Integrity)

Assume:
1. Each row records the SHA-256 hashes of all artifact and checkpoint files it references.
2. Each row records the SHA-256 hash of the deterministic derivation program \(D\).
3. The verifier enforces the replay rule in §4.

Then:

**(A) Non-fabrication:**  
No party can alter the logged derived certificate fields \(Z_k\) without detection **unless** they also change the referenced artifacts or derivation program in a way that breaks recorded hashes.

**(B) Replay correctness:**  
If verification passes, then for every step \(k\), the logged certificate fields \(Z_k\) are exactly the output of the derivation program \(D\) applied to the hash-locked artifacts \(A_k\) under the recorded run configuration.

---

## 6) Proof

(A) Suppose an adversary changes \(Z_k\) while leaving the referenced files unchanged.

- The row hash (if chained) changes, and verification fails at chain check.
- Even if chain were absent, replay would compute \(Z_k' = D(A_k;\theta)\) from unchanged files.
- Since \(D\) is deterministic, \(Z_k'\) is fixed.
- If \(Z_k \ne Z_k'\), the verifier’s exact-match check fails.

Therefore any mismatch is detected.

If the adversary tries to also change artifacts or code to force a new \(Z_k\), then at least one file hash changes, and the verifier detects a SHA-256 mismatch unless the row is rewritten; rewriting breaks chained history (if present).

Thus, fabrication is blocked by hash-binding + replay.

(B) If verification passes, then the verifier has confirmed:
- every referenced file matches its recorded hash, hence the artifacts are exactly \(A_k\),
- the derivation code matches \(h(D)\),
- and replay output matches logged \(Z_k\).

Therefore \(Z_k = D(A_k;\theta)\) for every \(k\). ∎

---

## 7) Operational Meaning (Steel Statement)

After Theorem 004 is enforced, an auditor can say:

- “These exact raw samples were used.”
- “This exact derivation code was used.”
- “The logged PAC certificate values are not claims; they are forced consequences.”

This is the difference between **tamper-evident** and **replay-correct**.

---

## 8) Monument Linkage

This binds directly to:

- Theorem 003: ensures the PAC gate’s computed fields are not fabricated.
- Proofpack ledgers: chaining prevents rewriting the past; derivation integrity prevents lying in the present.
- Any future theorem: if it relies on computed statistics, it must use the same pattern (hash + derivation hash + replay).
