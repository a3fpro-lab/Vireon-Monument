# Theorem 001 — The Folding Descent Kernel (VIREON Base Certificate)

**Status:** Alpha  
**License:** Apache-2.0  
**Authors:** The Architects

## 1) Setup

Let \(X\) be a set and let \(T: X \to X\) be an update map (“fold”).  
Let \(E: X \to \mathbb{R}\) be an energy (Lyapunov candidate).  
Let \(P: X \to [0,\infty)\) be a progress functional.

We study the orbit:
\[
x_{k+1} = T(x_k), \qquad k=0,1,2,\dots
\]

## 2) Descent Certificate (Kernel Condition)

Assume there exists a constant \(\alpha>0\) such that for all \(x\in X\),
\[
E(Tx) \le E(x) - \alpha\, P(x). \tag{K}
\]

Also assume **lower boundedness**:
\[
\inf_{x\in X} E(x) > -\infty. \tag{LB}
\]

This is the entire kernel. Everything below is a forced consequence.

---

## 3) Theorem (Summable Progress + Asymptotic Stationarity)

### Theorem 001 (Kernel Consequences)
Under (K) and (LB), for any initial \(x_0\in X\), the sequence \(\{x_k\}\) satisfies:

1) **Monotone energy drop**
\[
E(x_{k+1}) \le E(x_k) \quad \text{for all } k.
\]

2) **Summable progress**
\[
\sum_{k=0}^{\infty} P(x_k) \;<\; \infty.
\]

3) **Progress vanishes**
\[
P(x_k) \to 0 \quad \text{as } k\to\infty.
\]

---

## 4) Proof

**Step 1 (Telescoping).**  
Apply (K) at \(x=x_k\):
\[
E(x_{k+1}) \le E(x_k) - \alpha P(x_k).
\]
Rearrange:
\[
\alpha P(x_k) \le E(x_k) - E(x_{k+1}).
\]
Sum from \(k=0\) to \(N-1\):
\[
\alpha \sum_{k=0}^{N-1} P(x_k)
\;\le\;
\sum_{k=0}^{N-1}\bigl(E(x_k)-E(x_{k+1})\bigr)
=
E(x_0) - E(x_N).
\]

**Step 2 (Use lower boundedness).**  
By (LB), \(E(x_N)\ge \inf_X E\). Hence
\[
\alpha \sum_{k=0}^{N-1} P(x_k)
\le
E(x_0) - \inf_X E.
\]
Let \(N\to\infty\). The RHS is finite, so
\[
\sum_{k=0}^{\infty} P(x_k) < \infty,
\]
which proves (2).

**Step 3 (Progress must vanish).**  
If \(P(x_k)\) did not go to zero, there would exist \(\epsilon>0\) and infinitely many \(k\) with \(P(x_k)\ge \epsilon\), forcing the sum \(\sum_k P(x_k)\) to diverge. Contradiction. Therefore \(P(x_k)\to 0\), proving (3).

**Step 4 (Monotone energy drop).**  
Since \(P(x_k)\ge 0\), (K) immediately gives \(E(x_{k+1})\le E(x_k)\), proving (1). ∎

---

## 5) What This Gives You Operationally (No Handwaving)

If you can *log and verify* the inequality (K) at each step, you get a hard guarantee:

- the run cannot claim infinite “progress” without paying energy;
- progress values must eventually collapse toward 0;
- the entire system is auditable by re-checking (K) per step.

This is the minimal spine behind:
- certified gradient descent (choose \(P(x)=\|\nabla E(x)\|^2\) in expectation),
- certified proximal descent,
- certified operator splitting / fixed-point iteration (take \(P(x)=\|x-Tx\|^2\)),
- certified policy updates (PPO/TRPO-style gates using a conservative \(P\) built from artifacts).

---

## 6) Corollary (Finite-Budget “Best Iterate” Bound)

Let \(B := (E(x_0)-\inf_X E)/\alpha\). Then for any \(N\ge 1\),
\[
\min_{0\le k\le N-1} P(x_k) \le \frac{B}{N}.
\]

**Proof.**  
If all \(P(x_k) > B/N\) for \(k=0,\dots,N-1\), then \(\sum_{k=0}^{N-1}P(x_k) > B\), contradicting the telescoping bound. ∎

This is the practical “with N steps, you must have had at least one good step” guarantee.

---

## 7) Monument Linkage

This theorem is intentionally minimal. It is the **kernel** that later entries bind to:
- stochastic descent (expected version),
- diffusion training objectives,
- Hopfield/attention energy descent,
- PPO/TRPO PAC certificates + proofpacks,
- chained ledgers + derivation integrity.

It is the base invariant: **energy can’t lie** if the certificate is checked.
