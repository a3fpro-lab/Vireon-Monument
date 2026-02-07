# T01 — Descent Kernel: Summable Progress and Asymptotic Stationarity

**Status:** Proven  
**Version:** Alpha  
**Scope:** Deterministic descent with nonnegative progress certificate  
**Used by:** optimization folds, certified update logs, kernel bindings

---

## 1. Definitions

Let \(\mathcal{X}\) be a set (state space). Let \(E:\mathcal{X}\to\mathbb{R}\) be an **energy**.  
Let \(T:\mathcal{X}\to\mathcal{X}\) be an **update map** (a “fold”).  
Let \(P:\mathcal{X}\to[0,\infty)\) be a **progress certificate**.

We say the triple \((E,T,P)\) satisfies a **descent certificate** with constant \(\alpha>0\) if:

\[
E(Tx)\ \le\ E(x)\ -\ \alpha\,P(x)\quad\text{for all }x\in\mathcal{X}.
\tag{DC}
\]

We also assume a **lower bound**:

\[
E(x)\ \ge\ E_{\inf}\quad\text{for all }x\in\mathcal{X},
\tag{LB}
\]

for some finite constant \(E_{\inf}\in\mathbb{R}\).

Define the iterates \(x_{n+1}=T(x_n)\) starting from some \(x_0\in\mathcal{X}\).

---

## 2. Theorem (Summable Progress + Stationarity)

### Theorem T01
Assume (DC) and (LB). Then along the orbit \(\{x_n\}\):

1) **Energy is monotone nonincreasing**
\[
E(x_{n+1})\le E(x_n)\quad\text{for all }n\ge 0.
\]

2) **Progress is summable**
\[
\sum_{n=0}^{\infty} P(x_n)\ \le\ \frac{E(x_0)-E_{\inf}}{\alpha}\ <\ \infty.
\]

3) **Asymptotic stationarity (progress vanishes)**
\[
P(x_n)\ \to\ 0\quad\text{as }n\to\infty.
\]

---

## 3. Proof

From (DC) applied to \(x=x_n\):

\[
E(x_{n+1})\ \le\ E(x_n)\ -\ \alpha P(x_n).
\]

This immediately implies monotonicity \(E(x_{n+1})\le E(x_n)\).

Now sum the inequality from \(n=0\) to \(N-1\):

\[
E(x_N)\ \le\ E(x_0)\ -\ \alpha\sum_{n=0}^{N-1}P(x_n).
\]

Rearrange:

\[
\alpha\sum_{n=0}^{N-1}P(x_n)\ \le\ E(x_0)-E(x_N).
\]

Using the lower bound (LB), \(E(x_N)\ge E_{\inf}\), hence:

\[
\alpha\sum_{n=0}^{N-1}P(x_n)\ \le\ E(x_0)-E_{\inf}.
\]

Divide by \(\alpha>0\):

\[
\sum_{n=0}^{N-1}P(x_n)\ \le\ \frac{E(x_0)-E_{\inf}}{\alpha}.
\]

Let \(N\to\infty\). The partial sums are bounded and nondecreasing (since \(P\ge 0\)), therefore the series converges and:

\[
\sum_{n=0}^{\infty}P(x_n)\ \le\ \frac{E(x_0)-E_{\inf}}{\alpha}<\infty.
\]

Finally, if \(P(x_n)\not\to 0\), then there exists an \(\varepsilon>0\) and infinitely many indices \(n_k\) with \(P(x_{n_k})\ge\varepsilon\). This would force the sum \(\sum_n P(x_n)\) to diverge, contradicting finiteness. Hence \(P(x_n)\to 0\).

∎

---

## 4. Why This Matters (Monument-Level)

This theorem is the **base steel beam** of the Monument:

- If you can express an algorithm step as a fold \(T\),
- and prove a descent certificate (DC),
- then you automatically get **finite total progress** and **vanishing residuals**.

This is the exact skeleton used later for:
- gradient descent / proximal updates,
- Hopfield/attention energy descent,
- certified RL updates (PPO/TRPO) when a verifiable progress proxy is logged,
- proofpacks (ledger rows that prove each accepted step had nonnegative certified progress).

---

## 5. Notes (Scope + Limits)

- T01 does **not** guarantee convergence of \(x_n\) itself; it guarantees the **progress residual goes to zero**.
- To get convergence to an optimizer or equilibrium set, you add **error bounds**, **sharpness**, **Fejér monotonicity**, or compactness assumptions in later theorems.

---

## 6. Minimal Dependencies

None. Pure inequality + telescoping.

---

## 7. References

This is a standard telescoping argument appearing throughout optimization and dynamical systems, included here as a foundational lemma for the Vireon kernel.
