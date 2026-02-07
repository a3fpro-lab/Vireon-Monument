

# VIREON ProofPack Standard v1 (Alpha)
**Status:** Alpha (stable contract for public OSS release)  
**License:** Apache-2.0 (repo-level)  
**Authors:** The Architects (Inkwon Song Jr. + collaborators)

This document defines the **minimum required structure, semantics, and verification rules** for a VIREON ProofPack.

A ProofPack is a **proof-carrying evidence bundle**:
- history is tamper-evident (hash chain),
- files are content-bound (SHA-256),
- derived certificates are replayable (derivation integrity),
- and the verifier can independently reproduce the acceptance gate.

---

## 1) Definitions

### ProofPack
A directory containing:
- a run anchor (`run.json`),
- an append-only update ledger (`updates.jsonl`),
- artifacts referenced by ledger rows (e.g., batch samples),
- checkpoints referenced by ledger rows,
- a cryptographic closure (`sha256sum.txt`, `manifest.json`, optional signature).

### Verified
A ProofPack is **Verified** if a compliant verifier:
1. validates schemas,
2. validates hash chain (no reorder/delete/insert),
3. validates SHA-256 of every referenced file,
4. recomputes every derived certificate from raw artifacts and matches logged values,
5. validates acceptance semantics, and
6. validates manifest closure (and signature if present).

---

## 2) Required Directory Layout

A compliant ProofPack directory MUST contain:

<PACK_ROOT>/
run.json
updates.jsonl
artifacts/
… (artifact files referenced by ledger)
checkpoints/
… (checkpoint files referenced by ledger)
sha256sum.txt            (optional but strongly recommended)
manifest.json            (optional but strongly recommended)
signing/                 (optional)
PUBLIC_KEY_B64.txt
PRIVATE_KEY_B64_DO_NOT_SHARE.txt   (optional; must never be published)

### Path rules
- All paths referenced inside ledger rows MUST be **relative to `<PACK_ROOT>`**.
- Verifiers MUST reject absolute paths or `..` path traversal.

---

## 3) File Formats

### 3.1 `run.json` (required)
**Purpose:** Genesis anchor + run configuration.

Minimum required fields:

```json
{
  "schema": "vireon_run_v1",
  "created_utc": "YYYY-MM-DDTHH:MM:SSZ",
  "run_id": "string",
  "algo": "string",
  "env_id": "string",
  "seed": 1,
  "pac": { "alpha_total": 0.01, "...": "..." },
  "notes": "string"
}

Genesis definition:
genesis_hash = sha256(run.json bytes)

Verifiers MUST compute genesis hash and use it as the starting prev_row_hash.

⸻

3.2 updates.jsonl (required)

Purpose: Append-only, hash-chained ledger of steps.

Each line is one JSON object.
Minimum required fields per row:

{
  "schema": "vireon_update_row_v2",
  "created_utc": "YYYY-MM-DDTHH:MM:SSZ",
  "run_id": "string",
  "step_index_1based": 1,

  "prev_row_hash": "hex_sha256",
  "row_hash": "hex_sha256",

  "theta_old_path": "checkpoints/...",
  "theta_old_sha256": "hex_sha256",
  "theta_try_path": "checkpoints/...",
  "theta_try_sha256": "hex_sha256",

  "artifact_deltaL_path": "artifacts/...",
  "artifact_deltaL_sha256": "hex_sha256",
  "artifact_eps_path": "artifacts/...",
  "artifact_eps_sha256": "hex_sha256",
  "artifact_kl_path": "artifacts/...",
  "artifact_kl_sha256": "hex_sha256",

  "pac": { "p_pac": 0.0, "...": "..." },
  "accepted": true,
  "extra": {}
}

Row hash rule (required)
row_hash MUST equal:
	•	sha256(canonical_json(row_without_row_hash))

Where:
	•	canonical JSON uses sort_keys=true and separators (",", ":"),
	•	UTF-8 encoding,
	•	and the row_hash field is omitted for hashing.

Verifiers MUST recompute and compare exactly.

Chain rule (required)
	•	For row 0: prev_row_hash == genesis_hash
	•	For row i>0: prev_row_hash == rows[i-1].row_hash

Any mismatch => FAIL.

⸻

3.3 Artifact files (required if referenced)

Purpose: Raw evidence used to derive the certificate.

For Alpha v1, artifact schema is JSON:

{
  "schema": "vireon_artifact_v1",
  "meta": {
    "created_utc": "YYYY-MM-DDTHH:MM:SSZ",
    "bounds": { "min_val": -1.0, "max_val": 1.0 },
    "n_samples": 1000,
    "n_clipped": 12
  },
  "samples": [ ... floats ... ]
}

Verifiers MUST check:
	•	schema string matches,
	•	n_samples == len(samples),
	•	file SHA-256 matches ledger.

⸻

3.4 Checkpoints (required if referenced)

Checkpoints may be .pt, .safetensors, or other binary formats.

Verifiers MUST:
	•	check file exists,
	•	check file SHA-256 matches ledger,
	•	enforce checkpoint lineage rule (see Section 5).

⸻

4) Certificate Derivation Integrity (required)

A ProofPack is only meaningful if the derived certificate is replayable.

Required rule

For each row, verifiers MUST recompute the certificate fields from the raw artifacts, step index, and the run.json configuration.
	•	Recomputed certificate MUST match the logged row["pac"] values.
	•	Tolerance SHOULD be ≤ 1e-9 for floats (unless explicitly specified in run.json).

If certificate derivation cannot be reproduced deterministically => FAIL.

⸻

5) Acceptance Semantics (required)

The ledger MUST encode the accept/reject gate result in accepted.

Required rule

Verifier recomputes the certificate and then checks that:
	•	accepted matches the recomputed acceptance rule.

Checkpoint lineage (required)

Let theta_old_sha256 be the old checkpoint hash in row k.
Let theta_try_sha256 be the proposed checkpoint hash in row k.

If row k is accepted:
	•	row k+1 MUST have theta_old_sha256 == theta_try_sha256 of row k.

If row k is rejected:
	•	row k+1 MUST have theta_old_sha256 == theta_old_sha256 of row k.

Any mismatch => FAIL.

This prevents “silent policy swapping” and forces a coherent causal history.

⸻

6) Cryptographic Closure (strongly recommended)

6.1 sha256sum.txt

A text file where each line is:

<hex_sha256><two spaces><relative/path>

Verifiers SHOULD check it if present.
If present and mismatched => FAIL.

6.2 manifest.json

A JSON file containing:
	•	list of all files (paths, sha256, bytes),
	•	pack metadata,
	•	optional signature block.

If present, verifiers SHOULD check:
	•	file list integrity (sha256 matches disk),
	•	signature validity (if present and verifier supports it).

⸻

7) Optional Signatures (Ed25519)

If manifest.json.signature exists:
	•	it MUST include scheme, public_key_b64, signature_b64,
	•	and it MUST be a signature over the canonical JSON bytes of the manifest without the signature block.

Verifiers that support Ed25519 MUST verify it.
If verification fails => FAIL.

If a verifier does not support signatures, it MAY warn and continue.

⸻

8) Security Model (Honest Disclosure)

This standard guarantees:
	•	tamper-evidence for history ordering,
	•	artifact and checkpoint content binding,
	•	replayable certificate derivation,
	•	and optional authenticity via signatures.

This standard does NOT guarantee:
	•	truth of the environment, simulator, or hardware,
	•	absence of bias from clipping,
	•	i.i.d. assumptions in all RL sampling regimes,
	•	global convergence of deep policies.

It guarantees auditability, not metaphysical certainty.

⸻

9) Compliance Checklist

A ProofPack is compliant if it satisfies:
	•	Contains run.json with schema vireon_run_v1
	•	Contains updates.jsonl with rows schema vireon_update_row_v2
	•	Hash chain verified from genesis
	•	All referenced files exist and match SHA-256 in ledger
	•	Artifacts satisfy schema and n_samples consistency
	•	Certificates recompute and match logged values
	•	Accepted flag matches recomputed acceptance rule
	•	Checkpoint lineage verified
	•	(If present) sha256sum.txt matches disk
	•	(If present) manifest.json matches disk and signature verifies

⸻

10) Versioning Policy
	•	v1 (Alpha) means schemas may evolve, but verification rules are stable.
	•	Any schema change MUST bump schema string (e.g., vireon_update_row_v3).
	•	Verifiers MUST refuse unknown schema versions unless explicitly configured otherwise.

