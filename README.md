# Vireon-Monument
The VIREON Monument: kernel, theorem library, and replayable proofpacks—verifiable foundations for descent, equilibria, and certified RL.


## Repos

- **Kernel (definitions + theorem map):** `vireon-kernel` *(create next)*
- **Theorem library (proofs + bindings):** `vireon-theorems` *(create next)*
- **Executable proofpacks (evidence + verifier):** `Vireon-Proofpacks` *(existing)*

## What “proof” means here

We separate **mathematical statements** from **evidence artifacts**:

- A **theorem** is a written proof (LaTeX/Markdown), versioned and cross-linked.
- A **proofpack** is an executable evidence bundle:
  - append-only chained ledger (anti-reorder)
  - hashed artifacts + hashed checkpoints (anti-fabrication)
  - deterministic certificate derivation (replayable)
  - independent verifier (auditor-grade)

If a claim can be executed, it ships with a proofpack. If not, it ships as a theorem with clearly stated assumptions.

## Roadmap (public)

1. `vireon-kernel`: core definitions, descent kernel, equilibrium extensions
2. `vireon-theorems`: organized theorem catalog + modern bindings (transformers, diffusion, Hopfield/attention, VI/equilibria, PPO/TRPO certification)
3. `Vireon-Proofpacks`: reference implementation + demo environments (starting with CartPole)
4. Releases: tagged versions with reproducible verification reports

## License

MIT (unless a specific sub-repo states otherwise).
