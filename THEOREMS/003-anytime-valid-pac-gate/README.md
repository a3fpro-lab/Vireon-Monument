# Theorem 003 — Anytime-Valid PAC Gate (Horizon-Free Certified Updates)

Status: Alpha  
License: Apache-2.0  
Authors: The Architects

---

## 1) Setup (Certified Update Gate)

We model a single update attempt as a **fold** on a state space:

- A state (policy, parameters, iterate) is \(x \in X\).
- A proposal fold is \(x' = T(x)\).

We want a **certified acceptance rule** that can be audited from logged artifacts.

Assume there exist three *true* quantities associated with each attempted update \(k\):

- \(\Delta L_k\) = true improvement proxy (e.g., expected surrogate gain)
- \(\epsilon_k\) = true advantage magnitude proxy (or another bounded risk term)
- \(\delta_k\) = true divergence proxy (e.g., KL)

and nonnegative weights \(\lambda_\epsilon,\lambda_\delta\).

Define the (true) update value:
\[
p_k := \Delta L_k - \lambda_\epsilon \epsilon_k - \lambda_\delta \delta_k.
\]
A safe update is \(p_k \ge 0\).

**Problem:** \(\Delta L_k,\epsilon_k,\delta_k\) are unknown; we only observe samples.

---

## 2) Logged Artifacts (Replayable, Not Trust-Based)

For each step \(k\), the system logs three bounded sample artifacts:

- \(Y_{k,1},\dots,Y_{k,n_k}\) estimating \(\Delta L_k\), each clipped to \([a_L,b_L]\)
- \(U_{k,1},\dots,U_{k,n_k}\) estimating \(\epsilon_k\), each clipped to \([a_\epsilon,b_\epsilon]\)
- \(V_{k,1},\dots,V_{k,n_k}\) estimating \(\delta_k\), each clipped to \([a_\delta,b_\delta]\)

Let their empirical means be:
\[
\widehat{\Delta L}_k := \frac{1}{n_k}\sum_{i=1}^{n_k} Y_{k,i},\quad
\widehat{\epsilon}_k := \frac{1}{n_k}\sum_{i=1}^{n_k} U_{k,i},\quad
\widehat{\delta}_k := \frac{1}{n_k}\sum_{i=1}^{n_k} V_{k,i}.
\]

Because the artifacts are clipped, Hoeffding bounds apply **without** distributional assumptions beyond boundedness.

---

## 3) Anytime-Valid \(\alpha\)-Spending Schedule

Fix a total failure budget \(\alpha \in (0,1)\). Define a horizon-free spending schedule:
\[
\alpha_k := \alpha \cdot \frac{6}{\pi^2}\cdot\frac{1}{k^2},\qquad k\ge 1.
\]
Then:
\[
\sum_{k=1}^\infty \alpha_k = \alpha.
\]

Split each step budget across the three quantities:
\[
\alpha_{k,L}=\tfrac{1}{3}\alpha_k,\quad
\alpha_{k,\epsilon}=\tfrac{1}{3}\alpha_k,\quad
\alpha_{k,\delta}=\tfrac{1}{3}\alpha_k.
\]

---

## 4) Confidence Bounds (Hoeffding, Bounded Samples)

For bounded samples in \([a,b]\), Hoeffding gives:
\[
\Pr\Big(\ \big|\widehat{\mu}-\mu\big|\le (b-a)\sqrt{\tfrac{\log(2/\eta)}{2n}}\ \Big)\ \ge\ 1-\eta.
\]

Define per-step radii:
\[
r_{k,L} := (b_L-a_L)\sqrt{\frac{\log(2/\alpha_{k,L})}{2n_k}},
\quad
r_{k,\epsilon} := (b_\epsilon-a_\epsilon)\sqrt{\frac{\log(2/\alpha_{k,\epsilon})}{2n_k}},
\quad
r_{k,\delta} := (b_\delta-a_\delta)\sqrt{\frac{\log(2/\alpha_{k,\delta})}{2n_k}}.
\]

Define the conservative bounds:
\[
\Delta L_k^{\mathrm{LCB}} := \widehat{\Delta L}_k - r_{k,L},
\quad
\epsilon_k^{\mathrm{UCB}} := \widehat{\epsilon}_k + r_{k,\epsilon},
\quad
\delta_k^{\mathrm{UCB}} := \widehat{\delta}_k + r_{k,\delta}.
\]

Define the **PAC certificate value**:
\[
p_k^{\mathrm{PAC}} := \Delta L_k^{\mathrm{LCB}} - \lambda_\epsilon \epsilon_k^{\mathrm{UCB}} - \lambda_\delta \delta_k^{\mathrm{UCB}}.
\]

**Acceptance Gate (Anytime-valid):**
\[
\text{ACCEPT at step }k\quad \Longleftrightarrow \quad p_k^{\mathrm{PAC}} \ge 0.
\]

---

## 5) Theorem (Horizon-Free Certified Safety)

### Theorem 003 (Anytime-Valid PAC Gate)

Assume for each step \(k\) the logged artifacts are bounded as in §2 and sampled such that:
\[
\mathbb{E}[Y_{k,i}]=\Delta L_k,\quad
\mathbb{E}[U_{k,i}]=\epsilon_k,\quad
\mathbb{E}[V_{k,i}]=\delta_k,
\]
with all samples almost surely within their clipping intervals.

Then, with probability at least \(1-\alpha\), **simultaneously for all steps \(k\ge 1\)**:
\[
\Delta L_k \ge \Delta L_k^{\mathrm{LCB}},\qquad
\epsilon_k \le \epsilon_k^{\mathrm{UCB}},\qquad
\delta_k \le \delta_k^{\mathrm{UCB}}.
\]
In particular, on this event, whenever the system accepts (\(p_k^{\mathrm{PAC}}\ge 0\)), the true update value is nonnegative:
\[
p_k \ge 0.
\]

---

## 6) Proof

Fix a step \(k\).

By Hoeffding with parameter \(\alpha_{k,L}\):
\[
\Pr\big(\Delta L_k < \widehat{\Delta L}_k - r_{k,L}\big)\le \alpha_{k,L}.
\]
Equivalently:
\[
\Pr(\Delta L_k \ge \Delta L_k^{\mathrm{LCB}})\ge 1-\alpha_{k,L}.
\]

Similarly:
\[
\Pr(\epsilon_k \le \epsilon_k^{\mathrm{UCB}})\ge 1-\alpha_{k,\epsilon},
\qquad
\Pr(\delta_k \le \delta_k^{\mathrm{UCB}})\ge 1-\alpha_{k,\delta}.
\]

By union bound at fixed \(k\), the three inequalities hold jointly with probability at least:
\[
1-(\alpha_{k,L}+\alpha_{k,\epsilon}+\alpha_{k,\delta}) = 1-\alpha_k.
\]

Now apply a second union bound over all \(k\ge 1\):
\[
\Pr(\text{all steps satisfy all bounds}) \ge 1-\sum_{k=1}^\infty \alpha_k = 1-\alpha.
\]

On this event, for every \(k\):
\[
p_k = \Delta L_k - \lambda_\epsilon\epsilon_k - \lambda_\delta\delta_k
\ge
\Delta L_k^{\mathrm{LCB}} - \lambda_\epsilon\epsilon_k^{\mathrm{UCB}} - \lambda_\delta\delta_k^{\mathrm{UCB}}
= p_k^{\mathrm{PAC}}.
\]
Therefore if \(p_k^{\mathrm{PAC}}\ge 0\), then \(p_k\ge 0\). ∎

---

## 7) What This Gives You Operationally

This is the “steel foundation” point:

- **No horizon precommitment:** the guarantee holds for all \(k\) using \(\sum \alpha_k=\alpha\).
- **Auditability:** an external verifier recomputes \(p_k^{\mathrm{PAC}}\) from the raw artifacts.
- **Hard acceptance semantics:** passing the gate implies \(p_k\ge 0\) with confidence \(1-\alpha\) under bounded-sample assumptions.
- **Fold-ready:** this is a certified fold rule—accept only when the certificate says “safe.”

This theorem is the mathematical spine behind:
- PPO/TRPO-style safe policy updates with logged evidence,
- long-running training pipelines with non-collapsing statistical guarantees,
- proofpacks that are replayable by independent verifiers.

---

## 8) Monument Linkage

This binds directly to:

- Theorem 001 (Descent Kernel): \(P(x_k)\) becomes the certificate margin \(p_k^{\mathrm{PAC}}\) in a logged gate.
- Proofpack Integrity (ledger + hashing): ensures the artifacts used in the proof cannot be silently swapped or reordered.
- Certification systems: “accepted” has meaning beyond trust; it is a probabilistic statement tied to logged data.
