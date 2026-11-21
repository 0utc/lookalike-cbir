# PROGRESS — Lookalike (CBIR e-commerce)

> Shared status board. **Each person edits ONLY their own section** (to avoid merge conflicts).
> The milestones table is updated by whoever reaches the milestone, after telling the other person.
> Task IDs come from `TASKS.md`. What happened goes in your own devlog:
> `devlog/DEVLOG_oussama.md` and `devlog/DEVLOG_bilal.md`.
> Deadline: **TBD** — "a few days after the professor's final exam". Add real dates as soon as it is announced.

Legend: ⬜ todo · 🟨 in progress · ✅ done · ⛔ blocked

## Milestones (shared)
| ID | Milestone | Target date | Status |
|----|-----------|-------------|--------|
| M0 | Kickoff: repo skeleton, 3 contracts frozen and reviewed by both | | ⬜ |
| M1 | End-to-end with stub; tiny catalog (500 products) searchable | | ⬜ |
| M2 | All [core] tasks working (swap one task) | | ⬜ |
| M3 | Chosen optional (§10) extensions working | | ⬜ |
| M4 | All tests run, demo recorded | | ⬜ |
| M5 | Report merged, `v1.0` tagged, submitted | | ⬜ |

## Shared tasks
| Task | Status | Notes |
|------|--------|-------|
| Kickoff session (repo skeleton, read contracts together) | ⬜ | |
| REFERENCES.md kept up to date | ⬜ | |
| Final integration day (fresh clone, full test plan, report merge, tag) | ⬜ | |

---

## PACKAGE B — Aissati Oussama — Data, API & Evaluation
*Only Oussama (and his Claude) edits this section.*
Last updated: YYYY-MM-DD

| Task | Description | Tag | Status | Branch / PR | Notes |
|------|-------------|-----|--------|-------------|-------|
| B0 | Environment + GitHub repo setup | core | ⬜ | | |
| B1 | DB schema + OpenAPI contracts | core | ⬜ | | |
| B2a | Tiny catalog (500 products) | core | ⬜ | | due within 3 days of kickoff |
| B2b | Full catalog + DB + data docs | core | ⬜ | | |
| B3a | API core endpoints on stub | core | ⬜ | | |
| B3b | API on real engine | core | ⬜ | | |
| B3c | Filters + admin CRUD | opt | ⬜ | | |
| B4 | Evaluation (Precision@K, 2-model comparison, threshold, failures) | core+opt | ⬜ | | |
| B5 | Wireframes | core | ⬜ | | due weeks 1–2 |
| B6 | Test plan + execution | core | ⬜ | | |
| B7 | Test-query set (~15 images) + judgements | core | ⬜ | | |
| B8 | Report sections (B) | core | ⬜ | | |

**Next 3 actions (B):**
1.
2.
3.

**Blocked / waiting on A:** none

---

## PACKAGE A — Afallah Bilal — Retrieval & Interface
*Only Bilal (and his Claude) edits this section.*
Last updated: YYYY-MM-DD

| Task | Description | Tag | Status | Branch / PR | Notes |
|------|-------------|-----|--------|-------------|-------|
| A1 | Retrieval contract + stub engine | core | ⬜ | | |
| A2 | Feature extraction (MobileNetV2; DINOv2-S optional) | core+opt | ⬜ | | |
| A3 | Retrieval core (+ similarity score, vector update) | core+opt | ⬜ | | |
| A4 | CPU serving check | core | ⬜ | | |
| A5 | Front-end (+ filters, similarity indicator, admin UI) | core+opt | ⬜ | | |
| A6 | Install & usage guide | core | ⬜ | | |
| A7 | Test-query set (~15 images) | core | ⬜ | | |
| A8 | Short demo | core | ⬜ | | |
| A9 | Report sections (A) | core | ⬜ | | |

**Next 3 actions (A):**
1.
2.
3.

**Blocked / waiting on B:** none

---

## Decisions log (short; details in DEVLOG.md)
- 2026-11-19 — Scope v1.0 frozen; tasks agreed (A = Bilal, B = Oussama).
