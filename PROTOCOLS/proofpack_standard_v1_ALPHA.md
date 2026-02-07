# ProofPack Standard v1 (Vireon Monument)
**Status:** Alpha / enforceable  
**Purpose:** Define an evidence bundle that can be independently verified with *no trust* in the author.

This standard is intentionally conservative: if something is not mechanically checkable, it is not part of the proof.

---

## 0) Definitions

- **Pack Root**: a directory containing the full evidence bundle.
- **Row**: one logged update step (a JSON object).
- **Artifact**: raw data used to compute certificate values (returns, advantages, KL samples, loss deltas, etc.).
- **Checkpoint**: model state referenced by a row (policy/value weights or any state snapshot).
- **Certificate**: a deterministic computation from artifacts producing acceptance/metrics fields.
- **Verifier**: independent program that re-checks integrity + recomputes certificates.

---

## 1) Required Files (Pack Root)

A valid pack MUST contain:

1. `run.json`  
2. `updates.jsonl`  
3. `sha256sum.txt`  
4. `manifest.json`  
5. A verifier output report (one of):
   - `VERIFY_REPORT.json`, or
   - `VERIFIER/report.json`

And directories:

- `artifacts/` (raw samples)
- `checkpoints/` (state snapshots)

Optional:

- `signing/` (authenticity material)
- `meta/` (environment, versions, reproducibility notes)

---

## 2) run.json (Run Header)

### Required fields
- `schema`: `"vireon_run_v1"`
- `created_utc`: ISO-8601 UTC string
- `run_id`: stable identifier
- `algo`: e.g. `"PPO_certified"` / `"TRPO_certified"`
- `seed`: integer
- `pac`: object describing the certification gate config

### pac object (minimum)
- `alpha_total`: float in (0,1)
- `alpha_split_L`, `alpha_split_eps`, `alpha_split_kl`: floats summing to 1
- `lam_eps`, `lam_kl`: nonnegative floats
- `kl_target`: float or null

No hidden defaults: everything used by the gate must appear in `run.json`.

---

## 3) updates.jsonl (Append-Only Ledger)

A pack’s core history is a JSONL file: one JSON object per line.

### Required row fields (v2)
- `schema`: `"vireon_update_row_v2"`
- `created_utc`: ISO-8601 UTC string
- `run_id`: must match `run.json`
- `step_index_1based`: integer >= 1
- `prev_row_hash`: hash linking to previous row
- `row_hash`: hash of the row content (excluding `row_hash` itself)

### Required linkage fields
Each row MUST reference:
- `theta_old_path`, `theta_old_sha256`
- `theta_try_path`, `theta_try_sha256`

And artifacts used for certificate recomputation:
- `artifact_deltaL_path`, `artifact_deltaL_sha256`
- `artifact_eps_path`, `artifact_eps_sha256`
- `artifact_kl_path`, `artifact_kl_sha256`

### Required decision fields
- `pac`: object containing computed certificate fields
- `accepted`: boolean, MUST equal `pac.accepted`

### Hash chaining rule
- Genesis hash = `sha256(run.json)`
- For row k=1: `prev_row_hash == genesis_hash`
- For row k>1: `prev_row_hash == row_hash(previous row)`

### Checkpoint lineage rule
Let `A_k` be whether row k was accepted.
- If `A_k == true`, then the *next* row’s `theta_old_sha256` MUST equal this row’s `theta_try_sha256`.
- If `A_k == false`, then the *next* row’s `theta_old_sha256` MUST equal this row’s `theta_old_sha256`.

This prevents “rewriting history” by switching starting checkpoints.

---

## 4) Artifacts

Artifacts are raw evidence used to compute certificate fields.

### Required properties
- Deterministic parse format
- Explicit bounds (for concentration / confidence sequences)
- Raw sample list present (no summaries-only)

### Recommended minimal format (JSON)
Artifact files SHOULD be JSON with:
- `schema`: `"vireon_artifact_v1"`
- `meta`:
  - `created_utc`
  - `bounds`: `{min_val, max_val}`
  - `n_samples`
  - `n_clipped`
- `samples`: array of floats

Artifacts MUST be content-addressed by SHA-256 in ledger rows.

---

## 5) Certificates and Derivation Integrity

A verifier MUST be able to recompute `row.pac` from raw artifacts and `run.json` parameters.

### Determinism requirements
- Given:
  - the three artifact files for that row
  - `step_index_1based`
  - `run.json.pac`
- The function `compute_pac_from_artifacts(...)` MUST produce identical results within a declared tolerance.

### “Derivation integrity” means:
- If artifacts change, recomputation changes, and verifier fails.
- If row fields change, row hash chain breaks, and verifier fails.

No “manual edits” to derived values are permitted.

---

## 6) sha256sum.txt and manifest.json

### sha256sum.txt
Contains lines:
`<sha256>␠␠<relative_path>`

It SHOULD cover all files in the pack except itself and MUST match file contents.

### manifest.json
Contains:
- `schema`: `"vireon_manifest_v1"`
- `created_utc`
- `root` (directory name)
- `files`: list of `{path, sha256, bytes}`

Optional: `signature` block for authenticity.

---

## 7) Optional Authenticity (Ed25519)

If included, `manifest.json.signature` SHOULD contain:
- `scheme`: `"ed25519"`
- `public_key_b64`
- `signature_b64`
- `signed_over`: description of what was signed

Verifier SHOULD check the signature if crypto dependency is installed; otherwise warn.

Integrity (hashes) != authenticity (identity). Signature is optional but recommended.

---

## 8) Security Model (What this stops / doesn’t stop)

### Stops (if verifier passes)
- Reordering, insertion, deletion of ledger rows
- Substituting checkpoints or artifacts without detection
- Faking certificate fields without changing underlying artifacts

### Does not stop
- A malicious trainer that *generates* bad artifacts honestly
- A compromised RNG or environment producing biased data
- “Correctness of the world model” beyond what the artifacts encode

This is a *forensic-grade integrity and replay* standard, not metaphysical truth.

---

## 9) Minimal Verifier Checklist

A compliant verifier MUST:
1. Validate `run.json` schema
2. Compute genesis hash = `sha256(run.json)`
3. Parse all rows and verify:
   - schema + required fields
   - `prev_row_hash` chain
   - `row_hash` correctness
4. For each referenced file:
   - existence
   - sha256 matches the logged value
5. Enforce checkpoint lineage rule
6. Recompute `pac` from artifacts and compare within tolerance
7. Check `sha256sum.txt` and `manifest.json` if present
8. Output a machine-readable report containing:
   - `ok: true/false`
   - errors list
   - summary (rows, accepted_rows, run_id)

---

## 10) Versioning
Breaking changes MUST bump:
- `proofpack_standard_v2.md`

Packs MUST declare their schema versions in-file (`schema` fields) so old verifiers can fail loudly.

---
