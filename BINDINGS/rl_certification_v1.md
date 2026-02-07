# Binding: PPO/TRPO as Certified Folds (PAC + Derivation Integrity) — v1 (Alpha)

This binding turns PPO/TRPO-style updates into **proof-carrying steps** inside the VIREON Kernel.

It is designed to be auditable:
- raw artifacts are hashed,
- derived certificate is recomputed by the verifier,
- update history cannot be reordered or rewritten (hash-chained rows),
- checkpoints are content-bound (checkpoint hashes logged).

---

## 1) Binding to the Kernel

We bind \((\mathcal X,\mathcal C,E,T,P)\) as follows.

### State space
\[
\mathcal X := \Pi
\]
a space of stochastic policies \(\pi(\cdot\mid s)\), e.g., neural network policies.

### Feasible set (trust region)
Choose \(\delta_{\text{tgt}}>0\). Define feasibility by a KL constraint:
\[
\mathcal C := \left\{ \pi \in \Pi:\ D_{\mathrm{KL}}(\pi \,\|\, \pi_{\text{ref}})\le \delta_{\text{tgt}}\right\}
\]
where \(\pi_{\text{ref}}\) is the current “old” policy at the start of the step.

(Operationally we enforce feasibility by *rejecting* updates whose KL UCB exceeds \(\delta_{\text{tgt}}\).)

### Energy (negative of improvement)
Define a step-local “energy” as the negative of a conservative certified improvement:
\[
E(\pi) := -\,p_{\mathrm{PAC}}(\pi_{\text{old}}\to \pi).
\]
So **decreasing** energy corresponds to **increasing** certified improvement.

### Fold (candidate update map)
A fold proposes \(\pi_{\text{try}} = T(\pi_{\text{old}})\) via PPO/TRPO optimization, then applies a gate:
- if certified, accept: \(\pi_{\text{new}}:=\pi_{\text{try}}\),
- else reject: \(\pi_{\text{new}}:=\pi_{\text{old}}\).

### Progress certificate
\[
P(\pi_{\text{old}}) := \max\{0,\ p_{\mathrm{PAC}}(\pi_{\text{old}}\to T(\pi_{\text{old}}))\}.
\]

---

## 2) The Certificate We Log (What the Auditor Verifies)

For each step \(k=1,2,\dots\), we compute from raw batch artifacts:

### Raw empirical samples (artifacts)
From trajectories sampled under \(\pi_{\text{old}}\), we create bounded sample arrays:

- **Surrogate improvement samples** \(\{X_i\}_{i=1}^{n_L}\) approximating per-sample improvement, e.g.
  \[
  X_i := \bigl(r_i(\pi_{\text{try}})-1\bigr)\,A_i
  \quad \text{where } r_i=\frac{\pi_{\text{try}}(a_i\mid s_i)}{\pi_{\text{old}}(a_i\mid s_i)}.
  \]
- **Advantage magnitude samples** \(\{Y_i\}_{i=1}^{n_\epsilon}\) for \(|A|\) control, e.g.
  \[
  Y_i := |A_i|.
  \]
- **KL samples** \(\{Z_i\}_{i=1}^{n_{\mathrm{KL}}}\) measuring per-state KL, e.g.
  \[
  Z_i := D_{\mathrm{KL}}\bigl(\pi_{\text{old}}(\cdot\mid s_i)\,\|\,\pi_{\text{try}}(\cdot\mid s_i)\bigr).
  \]

Each artifact is **bounded by construction** via clipping:
\[
X_i\in[\underline x,\overline x],\quad Y_i\in[\underline y,\overline y],\quad Z_i\in[\underline z,\overline z].
\]
Clipping is logged (counts + bounds) so auditors see exactly what happened.

### Anytime-valid confidence via α-spending
Fix total failure probability \(\alpha_{\text{total}}\in(0,1)\). For step \(k\), use an α-spending schedule:
\[
\alpha_k := \alpha_{\text{total}}\cdot \frac{6}{\pi^2}\cdot \frac{1}{k^2},
\quad \sum_{k=1}^{\infty}\alpha_k=\alpha_{\text{total}}.
\]
Split per-step risk across three quantities:
\[
\alpha_{k,L}=\rho_L\alpha_k,\quad \alpha_{k,\epsilon}=\rho_\epsilon\alpha_k,\quad \alpha_{k,\mathrm{KL}}=\rho_{\mathrm{KL}}\alpha_k,
\]
with \(\rho_L+\rho_\epsilon+\rho_{\mathrm{KL}}=1\).

### Hoeffding bounds (bounded means)
Let \(\bar X=\frac1{n_L}\sum X_i\) with range width \(R_X=\overline x-\underline x\). Then with probability \(\ge 1-\alpha_{k,L}\),
\[
\mu_X \ge \bar X - R_X\sqrt{\frac{\log(2/\alpha_{k,L})}{2n_L}} =: \Delta L^{\mathrm{LCB}}_k.
\]
Similarly for \(\bar Y,\bar Z\), with UCBs:
\[
\epsilon^{\mathrm{UCB}}_k := \bar Y + R_Y\sqrt{\frac{\log(2/\alpha_{k,\epsilon})}{2n_\epsilon}},
\]
\[
\delta^{\mathrm{UCB}}_k := \bar Z + R_Z\sqrt{\frac{\log(2/\alpha_{k,\mathrm{KL}})}{2n_{\mathrm{KL}}}}.
\]

### PAC certificate definition
Choose weights \(\lambda_\epsilon,\lambda_{\mathrm{KL}}>0\). Define
\[
\mathrm{pen}^{\mathrm{UCB}}_k := \lambda_\epsilon\,\epsilon^{\mathrm{UCB}}_k + \lambda_{\mathrm{KL}}\,\delta^{\mathrm{UCB}}_k
\]
and
\[
p^{\mathrm{PAC}}_k := \Delta L^{\mathrm{LCB}}_k - \mathrm{pen}^{\mathrm{UCB}}_k.
\]

**Gate rule (accept/reject):**
Accept step \(k\) iff
\[
p^{\mathrm{PAC}}_k \ge 0
\quad\text{and}\quad
\delta^{\mathrm{UCB}}_k \le \delta_{\text{tgt}}.
\]

---

## 3) Theorem K' (PAC-Certified Update Safety)

**Theorem K' (Per-step PAC safety).**  
Assume the artifacts are i.i.d. samples with the stated bounds and Hoeffding conditions apply. Then for each step \(k\), with probability at least \(1-\alpha_k\),
\[
\mu_X - \lambda_\epsilon \mu_Y - \lambda_{\mathrm{KL}}\mu_Z \ \ge\ p^{\mathrm{PAC}}_k,
\]
and therefore if the gate accepts (\(p^{\mathrm{PAC}}_k\ge 0\) and \(\delta^{\mathrm{UCB}}_k\le \delta_{\text{tgt}}\)), the step is certified “safe” at confidence level \(1-\alpha_k\).

**Proof.** By Hoeffding, with probability \(\ge 1-\alpha_{k,L}\), \(\mu_X\ge \Delta L^{\mathrm{LCB}}_k\).  
With probability \(\ge 1-\alpha_{k,\epsilon}\), \(\mu_Y\le \epsilon^{\mathrm{UCB}}_k\).  
With probability \(\ge 1-\alpha_{k,\mathrm{KL}}\), \(\mu_Z\le \delta^{\mathrm{UCB}}_k\).  
Union bound gives joint event with probability \(\ge 1-(\alpha_{k,L}+\alpha_{k,\epsilon}+\alpha_{k,\mathrm{KL}})=1-\alpha_k\).  
Combine inequalities to get the claim. ∎

**Anytime-valid across indefinite training.**  
Because \(\sum_k \alpha_k = \alpha_{\text{total}}\), the probability that *any* step ever violates the stated confidence control is bounded by \(\alpha_{\text{total}}\) via a union bound over all \(k\).

---

## 4) Theorem L' (Derivation Integrity) — No Fake Certificates

We enforce two integrity layers:

### (i) Artifact integrity (raw data binding)
For each artifact file \(A\), log:
- its relative path,
- its SHA-256 hash.

### (ii) Derivation integrity (replayable computation)
A deterministic function `compute_pac_from_artifacts(artifact_deltaL, artifact_eps, artifact_kl, step_k, cfg)` recomputes all PAC fields.
The verifier re-runs this computation and checks exact match (within tolerance).

**Theorem L' (Derivation integrity).**  
If (a) the verifier confirms the SHA-256 hashes of the artifact files and (b) the verifier recomputes the PAC fields from those artifacts and they match the logged PAC fields, then the logged certificate values cannot be fabricated without changing the raw artifacts (which would break hashes).

**Proof.** The logged PAC fields are a deterministic function of the artifact file bytes, step index, and configuration. If artifact bytes are fixed (hashes match) and the verifier recomputation matches, the logged values equal the recomputation. Any attempt to log false PAC values would fail verifier equality unless the artifacts were altered, which breaks hash checks. ∎

---

## 5) Theorem L (History Integrity) — No Reordering, No Deletion

Each update row contains:
- `prev_row_hash` = hash of the previous row,
- `row_hash` = hash of the current row without `row_hash`.

Genesis is defined as:
\[
\text{genesis\_hash} := \mathrm{sha256}(\texttt{run.json}).
\]

**Theorem L (Row chaining).**  
If a verifier checks the entire hash chain from genesis through the last row, then any insertion, deletion, or reordering of rows is detected.

**Proof.** Hash chaining is a standard append-only construction: each row commits to the full history via `prev_row_hash`. Modifying history changes the hash at the first modified row, which breaks all subsequent links. ∎

---

## 6) Checkpoint Binding (Policy Content Attestation)

For each step we log hashes for:
- `theta_old` checkpoint file,
- `theta_try` checkpoint file.

Verifier checks file hashes match, and enforces lineage:
- If step \(k\) accepted `theta_try`, then step \(k+1\) must start from that accepted checkpoint as `theta_old`.

This prevents “file swapping” attacks where checkpoint contents are replaced while names remain.

---

## 7) What This Binding Claims (and What It Does Not)

### It guarantees (auditable)
- You cannot reorder history without detection (Theorem L).
- You cannot fake logged certificates without altering raw artifacts (Theorem L').
- Each accepted step satisfies the PAC inequality with stated confidence (Theorem K').
- Trust region constraint is enforced conservatively (via KL UCB gate).

### It does NOT claim (honesty)
- Global convergence in nonconvex policy parameterizations.
- That clipping is “free” (it trades bias for boundedness; bias is visible and auditable).
- That trajectory samples are perfectly i.i.d. in all environments (this is a model assumption; we treat the result as a certificate under stated conditions).

This is still groundbreaking because it turns RL training into **proof-carrying training artifacts** that an external auditor can replay.

---

## 8) How This Maps to the ProofPack Engine

A proofpack run produces:
- `run.json` (config + genesis anchor)
- `updates.jsonl` (chained, hashed rows)
- `checkpoints/*.pt` (policy checkpoints)
- `artifacts/*.json` (bounded raw sample arrays)
- `sha256sum.txt` + `manifest.json` (closure + optional signature)

A verifier checks:
1) hash chain (history integrity),
2) file hashes (artifact + checkpoint binding),
3) recomputation of PAC (derivation integrity),
4) acceptance semantics (gate correctness).
