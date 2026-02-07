# Vireon Monument — Theorems Index

This index is the canonical entry point for the Monument theorem stack.

**Convention**
- Each theorem lives in `THEOREMS/NNN_<SLUG>/README.md` or `THEOREMS/NNN-<slug>/README.md` depending on the folder already committed.
- The ID `NNN` is permanent once assigned.
- “Fold” = the function/action, “folding” = the process, “folded” = the final state.

---

## Core Kernel Layer (Guaranteed Descent)

- **001 — The Folding Descent Kernel (VIREON Base Certificate)**  
  Folder: `THEOREMS/001_FOLDING_DESCENT_KERNEL/`  
  What it is: The minimal descent certificate: (K)+(LB) ⇒ monotone energy drop, summable progress, progress→0, and a finite-budget best-iterate bound.

---

## Stochastic / Expected Descent Layer (Noisy Folds)

- **002 — Expected Descent Under Stochastic Folding (SGD / AdamW Certificate)**  
  Folder: `THEOREMS/002-expected-stochastic-descent/`  
  What it is: Expected version of the kernel for stochastic folds (e.g., SGD-style updates), yielding convergence to a noise floor under bounded variance + smoothness-type assumptions.

---

## Proofpack Integrity Layer (Audit-Grade Computation)

- **003 — Anytime-Valid PAC Gate (Horizon-Free Certified Updates)**  
  Folder: `THEOREMS/003-anytime-valid-pac-gate/`  
  What it is: A horizon-free certification gate using anytime-valid confidence sequences (via α-spending) so long runs don’t suffer the α/10,000 “death spiral.”

- **004 — Derivation Integrity (Replay-Correct Certificates)**  
  Folder: `THEOREMS/004-derivation-integrity-replay/`  
  What it is: Prevents certificate fabrication by binding (i) raw artifacts, (ii) derivation code hash, and (iii) verifier replay with exact-match checks.

---

## Equilibria / Interaction Layer (RL, Games, Variational Inequalities)

- **005 — PAC-Certified Policy Improvement with Derivation Integrity (PPO/TRPO Proofpacks)**  
  Folder: `THEOREMS/005-pac-certified-policy-improvement/`  
  Status: queued (next)  
  What it is: The policy-update theorem tying certified improvement to proofpack artifacts (ΔL/ε/KL), with PAC bounds + replay correctness as enforcement.
