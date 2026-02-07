# VIREON Kernel v1 (Alpha)

This is the minimal, reusable “engine block” that everything else in the Monument binds to.

## 1) Domain Binding

A **domain binding** is a 5-tuple:

\[
(\mathcal X,\ \mathcal C,\ E,\ T,\ P)
\]

- **State space**: \(\mathcal X\)
- **Constraint / feasible set**: \(\mathcal C \subseteq \mathcal X\)
- **Energy / objective**: \(E:\mathcal C \to \mathbb R\)
- **Fold (update map)**: \(T:\mathcal C \to \mathcal C\)
- **Progress certificate**: \(P:\mathcal C \to [0,\infty)\)

### Axiom K (Kernel Descent)
There exists a constant \(\alpha>0\) such that for all \(x\in\mathcal C\),

\[
E(Tx)\ \le\ E(x)\ -\ \alpha\,P(x).
\tag{K}
\]

Interpretation: every fold decreases energy by at least \(\alpha P(x)\).  
When \(P(x)=0\), the fold is “stationary” at \(x\).

---

## 2) Theorem A — Feasibility / Admissibility Invariance

**Theorem A.** If \(T:\mathcal C\to\mathcal C\), then for any \(x_0\in\mathcal C\), the iterates
\[
x_{n+1}=T(x_n)
\]
satisfy \(x_n\in\mathcal C\) for all \(n\ge 0\).

**Proof.** By induction. Base: \(x_0\in\mathcal C\). Step: if \(x_n\in\mathcal C\), then \(x_{n+1}=T(x_n)\in\mathcal C\) since \(T\) maps \(\mathcal C\) to itself. ∎

---

## 3) Theorem B — Summability of Progress and Asymptotic Stationarity

Assume:
1. Axiom K holds.
2. \(E\) is bounded below on \(\mathcal C\): there exists \(E_\star\in\mathbb R\) with
   \[
   E(x)\ge E_\star\quad\forall x\in\mathcal C.
   \]

**Theorem B.** For any trajectory \(x_{n+1}=T(x_n)\) starting in \(\mathcal C\),
\[
\sum_{n=0}^{\infty} P(x_n)\ <\ \infty
\quad\text{and}\quad
P(x_n)\ \to\ 0.
\]

**Proof.** Sum (K) from \(n=0\) to \(N-1\):
\[
E(x_N)\ \le\ E(x_0)\ -\ \alpha\sum_{n=0}^{N-1}P(x_n).
\]
Rearrange and use \(E(x_N)\ge E_\star\):
\[
\alpha\sum_{n=0}^{N-1}P(x_n)\ \le\ E(x_0)-E_\star.
\]
Let \(N\to\infty\). The partial sums are bounded above, hence \(\sum_{n\ge0}P(x_n)<\infty\).  
A nonnegative summable sequence must converge to 0, so \(P(x_n)\to 0\). ∎

---

## 4) Theorem C — Gap-to-Progress Rates (Discrete Error Bound)

Define the **energy gap**:
\[
\Delta E(x) := E(x)-E_\star.
\]

Assume there exist constants \(c>0\) and \(p\ge 1\) such that for all \(x\in\mathcal C\),
\[
P(x)\ \ge\ c\,(\Delta E(x))^p.
\tag{EB}
\]

**Theorem C.** Under Axiom K + (EB), the gaps satisfy:
- If \(p=1\), then
  \[
  \Delta E(x_n)\ \le\ (1-\alpha c)^n\,\Delta E(x_0)
  \quad\text{whenever } 0<\alpha c<1.
  \]
- If \(p>1\), then
  \[
  \Delta E(x_n)\ \le\ \left(\Delta E(x_0)^{1-p} + (p-1)\alpha c\,n\right)^{-1/(p-1)}.
  \]

**Proof.** From (K) and (EB),
\[
\Delta E(x_{n+1}) \le \Delta E(x_n) - \alpha c\,(\Delta E(x_n))^p.
\]
For \(p=1\), this is \(\Delta E_{n+1}\le (1-\alpha c)\Delta E_n\), yielding the geometric bound.  
For \(p>1\), use the standard discrete comparison: consider \(f(u)=u^{1-p}\), which is decreasing for \(u>0\). One obtains
\[
\Delta E_{n+1}^{1-p} - \Delta E_n^{1-p} \ge (p-1)\alpha c,
\]
and summing gives the stated closed form. ∎

---

## 5) How to Use the Kernel (Rule of Construction)

To certify a system:

1. **Choose state** \(\mathcal X\), feasible set \(\mathcal C\).
2. **Define energy** \(E\) that you want to decrease.
3. **Define fold** \(T\) (the update rule).
4. **Exhibit certificate** \(P\ge 0\) and constant \(\alpha>0\) such that (K) holds.
5. Optional: prove an error bound (EB) to get rates via Theorem C.

This is the “steel foundation”: a reusable proof skeleton that activates across optimization, inference, control, and RL certification.
