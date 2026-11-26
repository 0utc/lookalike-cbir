# DEVLOG — Bilal (Package A)

> Append-only, newest entry at the TOP. One entry per work session or notable event. Never delete old entries.
> Only Bilal (and their Claude) writes here. Raw material for the report: what you tried, what failed, numbers, why you chose things.

## Entry template (copy this)
```
### YYYY-MM-DD — @Bilal — Task ID — short title
**Goal:** what I set out to do
**Done:** what actually got done (commits/PRs: #12, abc1234)
**Findings / numbers:** metrics, timings, memory, surprises
**Problems & fixes:** what broke, how it was solved (or not)
**Decisions:** what was decided and why (alternatives rejected)
**Next:** what comes next / what the other person needs to know
```

---
### 2026-11-26 — @Bilal — A1 — Contrat embeddings + stub
**Goal:** Écrire le contrat des embeddings et un faux moteur pour débloquer l'API de B.
**Done:** docs/CONTRACT_EMBEDDINGS.md, core/engine.py, core/stub_engine.py, tests/test_stub_engine.py (6 tests OK).
**Problems & fixes:** fichier de test créé dans core/ au lieu de tests/, déplacé.
**Decisions:** le moteur renvoie (id, score) seulement; l'API filtre en SQL puis passe candidate_ids.
**Next:** A2 (extraction des vecteurs avec MobileNetV2, notebook Kaggle).