# DEVLOG — Oussama (Package B)

> Append-only, newest entry at the TOP. One entry per work session or notable event. Never delete old entries.
> Only Oussama (and their Claude) writes here. Raw material for the report: what you tried, what failed, numbers, why you chose things.

## Entry template (copy this)
```
### YYYY-MM-DD — @Oussama — Task ID — short title
**Goal:** what I set out to do
**Done:** what actually got done (commits/PRs: #12, abc1234)
**Findings / numbers:** metrics, timings, memory, surprises
**Problems & fixes:** what broke, how it was solved (or not)
**Decisions:** what was decided and why (alternatives rejected)
**Next:** what comes next / what the other person needs to know
```

---
### 2026-11-21 — @Oussama — B0 — Environment and GitHub repo
**Goal:** Working dev environment on a 4 GB laptop and the shared GitHub repo with protected main.
**Done:** Python 3.11.9 installed on O: (per-user, not on PATH). Repo `0utc/lookalike-cbir` cloned into project\lookalike-cbir. Skeleton, .gitignore, .env.example, scripts/env.ps1 (redirects pip/HF/torch/temp caches into cache\), venv and base requirements.txt (fastapi, uvicorn, sqlalchemy, pillow, numpy, pandas, scikit-learn, matplotlib, httpx, pytest, ruff) installed. Initial commit c6f595b. Ruleset protect-main active: PR required, 1 approval, no force push, no deletion. Direct push to main tested and rejected (GH013).
**Findings / numbers:** C: free space went 11.8 GB to 8.7 GB during setup; cause is the Windows page file (5.1 GB allocated, ~3 GB used) under 4 GB RAM pressure, not our installs. Old pip cache on C: is ~158 MB.
**Problems & fixes:** conda base shadowed python (3.13), so we used a separate Python 3.11.9 and a venv. GitHub Free does not enforce protection on private repos and the Student Pack is not available yet (no school ID), so the repo was made public.
**Decisions:** Repo public. Assignment PDF never committed (git-ignored). Commit email is the GitHub noreply address, set per repo. Requirements are unpinned for now; pin with pip freeze later.
**Next:** Bilal accepts the invitation and reviews this PR. Then kickoff session, B1 contracts, B2 tiny catalog within 3 days.

### 2026-11-19 — @Oussama — Kickoff — Scope and tasks agreed
**Goal:** Fix what we build and who does what.
**Done:** `SCOPE.md` frozen (approved 2026-11-16 by Oussama, 2026-11-19 by Bilal). `TASKS.md` agreed: Bilal = Package A, Oussama = Package B. Separate devlog files per person.
**Findings / numbers:** —
**Problems & fixes:** —
**Decisions:** Project = "Lookalike". Catalog = Amazon Berkeley Objects subset. Models = MobileNetV2 (core) + DINOv2-Small (optional comparison). Back-end FastAPI (final) + SQLite, front-end React + Vite. Only the assignment's required and optional items are planned. Deadline unknown ("a few days after the final exam").
**Next:** Oussama sets up the environment and the GitHub repo (B0), then kickoff session and contracts (B1 / A1).
