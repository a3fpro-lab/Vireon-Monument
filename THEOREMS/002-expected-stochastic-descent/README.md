# Theorem 002 — Expected Descent Under Stochastic Folding (SGD / AdamW Certificate)

**Status:** Alpha  
**License:** Apache-2.0  
**Authors:** The Architects  

---

## 1) Setup (Stochastic Fold)

Let \(E:\mathbb{R}^d\to\mathbb{R}\) be differentiable and \(L\)-smooth:
\[
\|\nabla E(u)-\nabla E(v)\|\le L\|u-v\|\quad\forall u,v.
\]

Let the stochastic fold be
\[
x_{k+1} = T_k(x_k) := x_k - \eta\, g_k,
\]
where \(g_k\) is a stochastic estimator of \(\nabla E(x_k)\) satisfying:
\[
\mathbb{E}[g_k\mid x_k] = \nabla E(x_k) \tag{U}
\]
and a bounded second moment condition:
\[
\mathbb{E}\bigl[\|g_k\|^2 \mid x_k\bigr] \le G^2. \tag{M2}
\]

(For AdamW / preconditioning, see §5: the same argument applies in a bounded metric.)

---

## 2) Expected Descent Certificate

Assume step size \(0<\eta\le 1/L\). Then one-step smoothness gives, for any realized \(g_k\),
\[
E(x_{k+1}) \le E(x_k) - \eta \langle \nabla E(x_k), g_k\rangle + \frac{L\eta^2}{2}\|g_k\|^2.
\]
Taking conditional expectation given \(x_k\) and using (U),
\[
\mathbb{E}[E(x_{k+1})\mid x_k]
\le E(x_k) - \eta\|\nabla E(x_k)\|^2 + \frac{L\eta^2}{2}\,\mathbb{E}[\|g_k\|^2\mid x_k].
\]
Using (M2),
\[
\mathbb{E}[E(x_{k+1})\mid x_k]
\le E(x_k) - \eta\|\nabla E(x_k)\|^2 + \frac{L\eta^2}{2}G^2. \tag{EK}
\]

Interpretation: this is the kernel certificate “up to a noise floor”.

---

## 3) Theorem (Summable Gradient-Norm up to Noise Floor)

Assume lower boundedness:
\[
\inf_{x\in\mathbb{R}^d} E(x) > -\infty. \tag{LB}
\]

### Theorem 002 (Expected Kernel Consequences)
Under \(L\)-smoothness, (U), (M2), (LB), and \(0<\eta\le 1/L\), for any \(K\ge 1\),
\[
\eta\sum_{k=0}^{K-1}\mathbb{E}\bigl[\|\nabla E(x_k)\|^2\bigr]
\le
\mathbb{E}[E(x_0)] - \mathbb{E}[E(x_K)]
+ \frac{L\eta^2}{2}G^2\,K.
\]
Equivalently,
\[
\frac{1}{K}\sum_{k=0}^{K-1}\mathbb{E}\bigl[\|\nabla E(x_k)\|^2\bigr]
\le
\frac{\mathbb{E}[E(x_0)]-\inf E}{\eta K}
+\frac{L\eta}{2}G^2. \tag{AVG}
\]
In particular,
\[
\min_{0\le k\le K-1}\mathbb{E}\bigl[\|\nabla E(x_k)\|^2\bigr]
\le
\frac{\mathbb{E}[E(x_0)]-\inf E}{\eta K}
+\frac{L\eta}{2}G^2. \tag{BEST}
\]
Thus as \(K\to\infty\), the expected stationarity measure converges to a neighborhood of size \(\sim (L\eta/2)G^2\).

---

## 4) Proof

Start from the one-step expected descent inequality (EK):
\[
\mathbb{E}[E(x_{k+1})\mid x_k]
\le E(x_k) - \eta\|\nabla E(x_k)\|^2 + \frac{L\eta^2}{2}G^2.
\]
Take full expectation and rearrange:
\[
\eta\,\mathbb{E}[\|\nabla E(x_k)\|^2]
\le
\mathbb{E}[E(x_k)]-\mathbb{E}[E(x_{k+1})]
+\frac{L\eta^2}{2}G^2.
\]
Sum from \(k=0\) to \(K-1\) (telescoping):
\[
\eta\sum_{k=0}^{K-1}\mathbb{E}[\|\nabla E(x_k)\|^2]
\le
\mathbb{E}[E(x_0)]-\mathbb{E}[E(x_K)]
+\frac{L\eta^2}{2}G^2 K.
\]
Use \(E(x_K)\ge \inf E\) to obtain (AVG). The “best iterate” bound (BEST) follows from
\(\min_k a_k \le \frac{1}{K}\sum_k a_k\). \(\square\)

---

## 5) Notes for AdamW / Preconditioned Updates (Bounded Metric)

If the update is \(x_{k+1}=x_k-\eta\,H_k g_k\) with symmetric \(H_k\) satisfying
\[
m I \preceq H_k \preceq M I
\]
for constants \(0<m\le M<\infty\), then the same proof applies in the induced metric with modified constants.
This is the precise sense in which “adaptive preconditioners are leashed”: the fold remains a controlled descent step
up to a variance floor.

---

## 6) Monument Linkage

- This is the stochastic/expected analogue of Theorem 001’s kernel.
- Binding targets:
  - transformer training (SGD/AdamW on parameters),
  - diffusion training (noise-prediction MSE objective),
  - any minibatch-trained model with bounded second moment gradients.

Next queued: correspondence inversion (diffusion sampling) and Hopfield retrieval descent (attention).
