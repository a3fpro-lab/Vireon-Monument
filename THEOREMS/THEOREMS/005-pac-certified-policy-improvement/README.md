# Theorem 005 — PAC-Certified Policy Improvement with Derivation Integrity (Proofpacks)

**Status:** Alpha  
**License:** Apache-2.0  
**Authors:** The Architects

## 0) Purpose (What This Entry Proves)

This theorem turns a policy update into a **proof-carrying step**:

- The update is accepted only if a **PAC lower bound** on improvement exceeds a **PAC upper bound** on penalty.
- All certificate quantities are derived from **raw artifacts** (saved batch data), and an independent verifier can **replay** the derivation.

This binds theory → implementation → audit.

---

## 1) Setup

Let \(\pi\) be a policy in a policy class \(\Pi\). At update \(k\), we consider a candidate \(\pi_{k+1}\) derived from \(\pi_k\).

We define three per-update *true* (population) quantities:

1. **Improvement term** \(\Delta L_k\)  
2. **Advantage magnitude proxy** \(\epsilon_k \ge 0\)  
3. **Distribution shift** \(\delta_k \ge 0\) (typically KL)

We assume a penalty form
\[
\mathrm{pen}_k := \lambda_\epsilon \epsilon_k + \lambda_\delta \delta_k
\]
for fixed \(\lambda_\epsilon,\lambda_\delta > 0\).

Define the **true certified progress**
\[
p_k := \Delta L_k - \mathrm{pen}_k.
\]

---

## 2) Artifact Model (What Gets Logged)

For each update \(k\), we log three raw artifact files:

- \(A^{(L)}_k = \{X^{(L)}_{k,i}\}_{i=1}^{n_L}\)  (samples estimating \(\Delta L_k\))
- \(A^{(\epsilon)}_k = \{X^{(\epsilon)}_{k,i}\}_{i=1}^{n_\epsilon}\)  (samples estimating \(\epsilon_k\))
- \(A^{(\delta)}_k = \{X^{(\delta)}_{k,i}\}_{i=1}^{n_\delta}\)  (samples estimating \(\delta_k\))

Each artifact is stored with:
- exact sample list,
- clipping bounds (so concentration is valid),
- SHA256 hash of the artifact file contents.

We also log:
- SHA256 of \(\theta_k\) (old checkpoint),
- SHA256 of \(\theta_{k+1}\) (candidate checkpoint),
- the derivation function identity (code hash in practice),
- the computed certificate fields.

---

## 3) Anytime-Valid PAC Bounds (Horizon-Free)

Let \(\alpha \in (0,1)\) be a total failure budget for the entire run.

At update \(k\), allocate a per-step budget by an \(\alpha\)-spending schedule
\[
\alpha_k := \alpha \cdot \frac{6}{\pi^2}\cdot \frac{1}{k^2},
\quad\text{so that}\quad \sum_{k=1}^\infty \alpha_k \le \alpha.
\]

Split \(\alpha_k\) across the three quantities:
\[
\alpha_{k,L} + \alpha_{k,\epsilon} + \alpha_{k,\delta} \le \alpha_k.
\]

From artifacts, compute confidence bounds:
- \(\Delta L_k^{\mathrm{LCB}}\) such that \(\Pr(\Delta L_k \ge \Delta L_k^{\mathrm{LCB}}) \ge 1-\alpha_{k,L}\)
- \(\epsilon_k^{\mathrm{UCB}}\) such that \(\Pr(\epsilon_k \le \epsilon_k^{\mathrm{UCB}}) \ge 1-\alpha_{k,\epsilon}\)
- \(\delta_k^{\mathrm{UCB}}\) such that \(\Pr(\delta_k \le \delta_k^{\mathrm{UCB}}) \ge 1-\alpha_{k,\delta}\)

Define the **PAC penalty upper bound**
\[
\mathrm{pen}_k^{\mathrm{UCB}} := \lambda_\epsilon \epsilon_k^{\mathrm{UCB}} + \lambda_\delta \delta_k^{\mathrm{UCB}}.
\]

Define the **PAC certificate**
\[
p_k^{\mathrm{PAC}} := \Delta L_k^{\mathrm{LCB}} - \mathrm{pen}_k^{\mathrm{UCB}}.
\]

**Acceptance rule:**
\[
\text{ACCEPT update }k \iff p_k^{\mathrm{PAC}} \ge 0
\quad \text{(and optionally } \delta_k^{\mathrm{UCB}} \le \delta_{\mathrm{tgt}}\text{)}.
\]

---

## 4) Theorem 005 (PAC-Certified Policy Improvement)

**Theorem 005.**  
Assume the confidence bounds above are valid with budgets \(\alpha_{k,*}\) and \(\sum_k \alpha_k \le \alpha\).  
Then with probability at least \(1-\alpha\), **for every accepted update \(k\)** we have
\[
p_k \ge 0,
\quad\text{i.e.}\quad
\Delta L_k \ge \lambda_\epsilon \epsilon_k + \lambda_\delta \delta_k.
\]
Equivalently, every accepted update is a genuine improvement after penalties.

### Proof
Fix \(k\). On the event
\[
\mathcal{E}_k :=
\{\Delta L_k \ge \Delta L_k^{\mathrm{LCB}}\}
\cap
\{\epsilon_k \le \epsilon_k^{\mathrm{UCB}}\}
\cap
\{\delta_k \le \delta_k^{\mathrm{UCB}}\},
\]
we have
\[
p_k
= \Delta L_k - (\lambda_\epsilon \epsilon_k + \lambda_\delta \delta_k)
\ge
\Delta L_k^{\mathrm{LCB}} - (\lambda_\epsilon \epsilon_k^{\mathrm{UCB}} + \lambda_\delta \delta_k^{\mathrm{UCB}})
= p_k^{\mathrm{PAC}}.
\]
So if the gate accepts (\(p_k^{\mathrm{PAC}} \ge 0\)), then \(p_k \ge 0\) on \(\mathcal{E}_k\).

By the construction of bounds and a union bound,
\[
\Pr(\mathcal{E}_k) \ge 1-(\alpha_{k,L}+\alpha_{k,\epsilon}+\alpha_{k,\delta}) \ge 1-\alpha_k.
\]
Finally, by \(\sum_{k=1}^\infty \alpha_k \le \alpha\),
\[
\Pr\Big(\bigcap_{k=1}^\infty \mathcal{E}_k\Big)
\ge 1-\sum_{k=1}^\infty \alpha_k
\ge 1-\alpha.
\]
On this intersection event, every accepted update satisfies \(p_k \ge 0\). ∎

---

## 5) Derivation Integrity (Replay Correctness)

**Definition (Derivation Integrity).**  
A proofpack system has derivation integrity if an independent verifier can:
1. Hash-check raw artifacts and checkpoints (content-addressed),
2. Recompute \(\Delta L_k^{\mathrm{LCB}}, \epsilon_k^{\mathrm{UCB}}, \delta_k^{\mathrm{UCB}}\) from raw artifacts using the logged derivation rule,
3. Obtain the exact same logged \(p_k^{\mathrm{PAC}}\) (within a fixed tolerance).

**Consequence.**  
A training process cannot fabricate \(p_k^{\mathrm{PAC}}\) without either:
- changing raw artifacts (detected by SHA256 mismatch), or
- changing derivation rule (detected by code hash mismatch), or
- breaking the update chain (detected by row hash linkage).

This converts Theorem 005 from “paper guarantee” into an audit-grade guarantee.

---

## 6) Operational Notes (What This Enables)

- Long-horizon training without \(\alpha/10{,}000\) collapse (anytime-valid spending).
- External third-party verification without trusting the trainer.
- A clean bridge between classic descent certificates (Theorem 001/002) and RL update gates.

---

## 7) Monument Linkage

- **001** supplies the descent kernel logic (summable progress when a certified inequality holds).
- **003** supplies anytime-valid confidence sequences.
- **004** supplies replay-correct derivation integrity.
- **005** binds them into **certified policy improvement** with proof-carrying artifacts.
