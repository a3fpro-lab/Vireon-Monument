# Vireon Monument — Theorems Index

This index is the canonical entry point for the Monument theorem stack.

**Convention**
- Each theorem lives in `THEOREMS/NNN-<slug>/README.md`.
- The ID `NNN` is permanent once assigned.
- “Fold” = the function/action, “folding” = the process, “folded” = the final state.

---

## Core Kernel Layer (Guaranteed Descent)

- **001 — The Folding Descent Kernel (VIREON Base Certificate)**  
  Folder: `THEOREMS/001-folding-descent-kernel/`  
  What it is: The minimal descent certificate: (K)+(LB) ⇒ monotone energy drop, summable progress, progress→0, and a finite-budget best-iterate bound.

---

## Stochastic / Expected Descent Layer (Noisy Folds)

- **002 — Expected Descent Under Stochastic Folding (SGD / AdamW Certificate)**  
  Folder: `THEOREMS/002-expected-stochastic-descent/`  
  What it is: Expected version of the kernel for stochastic folds \(x_{k+1}=x_k-\eta g_k\), yielding convergence to a noise floor under bounded variance + smoothness.

---

## Correspondence / Inversion Layer (Generative Reconstruction)

- **003 — Anytime-Valid PAC Gate (Horizon-Free Certified Updates)** → `003-anytime-valid-pac-gate/README.md`

---

## Retrieval / Memory Layer (Hopfield / Attention)

- **004 — Hopfield Retrieval as Monotone Energy Descent (Attention Binding)**  
  Folder: `THEOREMS/004-hopfield-retrieval-descent/`  
  Status: queued (next)

---

## Equilibria / Interaction Layer (Saddles, Games, RL)

- **005 — PAC-Certified Policy Improvement with Derivation Integrity (PPO/TRPO Proofpacks)**  
  Folder: `THEOREMS/005-pac-certified-policy-improvement/`  
  Status: queued (next)
