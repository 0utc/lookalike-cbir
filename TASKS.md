# TASKS — Lookalike

> Status: **DRAFT v0.2 — package choice pending.** Based on `SCOPE.md` v1.0 (frozen).
> These tasks cover **everything the assignment asks for, including all its optional extensions (§10)** — nothing more.
> Portfolio-only ideas from the scope (CLIP/fusion, ONNX quantisation, Docker/CI, public demo, large real-photo
> benchmark) are **not planned** here; they stay in `SCOPE.md` as a ceiling and can be taken up after submission.
> Once chosen, write the names in the "Owner" lines and set the status to `AGREED`.

## 1. How this works

- Two packages of about the same size (**~100 h each**), each mixing ML/data work with engineering work.
- Each person picks one package (ranked preferences, or a coin flip if both want the same).
- Tags: **[core]** = required by the assignment · **[opt]** = optional extension listed in assignment §10 or §3.3.
  Do all [core] first; [opt] tasks are spread evenly between the two packages.
- Estimates are rough (±30%). At each milestone we rebalance if one of us is clearly more loaded.
  **At M2 we swap at least one task** so both touch both sides.
- Both must be able to explain the **whole** system at the oral (SCOPE M14).

## 2. Ground rules

1. **Contract-first:** DB schema, OpenAPI REST contract, and embedding-file format + `SearchEngine` interface are written
   in week 0 and frozen. Changes = a dated entry in your own devlog + telling the other person.
2. **Stubs and mocks:** the API runs on a fake `SearchEngine` until the real one exists; the front-end runs on a mock API
   generated from the OpenAPI file.
3. **Git:** protected `main`, one branch per task, small PRs, **each PR reviewed by the other person**.
4. **No images or large files in Git** (artefacts shared as described in `docs/DATA.md`).
5. Each person edits only their own section of `PROGRESS.md` and writes only in their own devlog file
   (`devlog/DEVLOG_oussama.md`, `devlog/DEVLOG_bilal.md`).
6. Every external resource (code, model, dataset, image) goes into `REFERENCES.md` the day it is used.

## 3. The two packages

### PACKAGE A — "Retrieval & Interface"
Owner: `__________`  ·  Total ≈ 97 h

| ID | Task | Tag | h | Done when |
|----|------|-----|---|-----------|
| A1 | **Retrieval contract:** embedding file format (ids + vectors aligned by product id) and `SearchEngine` interface; a **stub engine** returning plausible fake results | core | 3 | `docs/CONTRACT_EMBEDDINGS.md` + stub; B's API can call the stub with nothing else |
| A2 | **Feature extraction (Kaggle/Colab notebooks):** pretrained CNN without its classification layer, same preprocessing for catalog and queries. Do the tiny catalog first, then the full one. **MobileNetV2 = core; DINOv2-Small = optional second model for the comparison** | core + opt | 9 | Notebooks in `notebooks/`; vectors saved; preprocessing documented; row alignment checked by a test |
| A3 | **Retrieval core (`core/`):** query preprocessing + embedding, cosine similarity over precomputed vectors (FAISS), sorted top-K, **"no relevant result" threshold**; text filter (keyword/category) then image ranking; selectable model (for the comparison); **similarity score + how to interpret it** [opt]; **add/update/remove one product's vector** when its image changes [opt] | core + opt | 21 | Unit tests; tiny catalog returns sensible neighbours; same interface as the stub |
| A4 | **CPU serving check:** load the model(s) inside the backend and measure RAM/latency on a 4 GB machine; only if too heavy, convert to ONNX as a fallback | core | 4 | A short note in `docs/` with the numbers and the choice made |
| A5 | **Front-end (React + Vite + Tailwind):** home page (text box, image picker incl. phone camera, preview/replace/cancel, button enabled only when valid, loader, clear errors), random multi-category product grid, results page, product page, responsive; **filters (category/price/brand/availability)** [opt]; **similarity indicator** [opt]; **admin screens** (add/edit/delete product) [opt]. Built against the mock API first | core + opt | 35 | Matches the wireframes; usable on phone/tablet/desktop; all error cases of SCOPE M10 visible and readable |
| A6 | **Install & usage guide:** `requirements.txt`, how to load the catalog, how to start back-end and front-end | core | 4 | A fresh clone runs by following the README only |
| A7 | **Test-query set (half, ~15 images):** photos covering several categories (some taken with a phone), provenance documented | core | 2 | Files + `docs/TEST_QUERIES.md` (split with B7: different objects) |
| A8 | **Short demo** (narrated screen recording of the main scenarios) | core | 4 | Video file/link in the README |
| A9 | **Report sections (A):** architecture, technical choices, CBIR algorithm, **"CBIR explained"** (classification vs retrieval, feature vector, similarity measure, ranking), model comparison, text+image combination choice, front-end | core | 15 | Drafted in `report/`, reviewed by B |

### PACKAGE B — "Data, API & Evaluation"
Owner: `__________`  ·  Total ≈ 99 h

| ID | Task | Tag | h | Done when |
|----|------|-----|---|-----------|
| B1 | **Data + API contracts:** DB schema (SQLite, PostgreSQL-compatible) and OpenAPI spec (home suggestions, image search, text search, combined search, product detail, filters, admin CRUD) | core | 5 | `docs/CONTRACT_DB.md`, `docs/openapi.yaml`; A can generate a mock API from it |
| B2 | **Data & catalog:** download ABO, pick ~15–20k products over ≥10–12 categories, **check coverage of the assignment's example categories** (fashion, electronics, beauty, toys, home), clean, small thumbnails, fill the DB (id, name, category, price, image path, brand, description, **stock/availability**), seeded simulated prices/stock stated openly, loading script + instructions. **Deliver a 500-product tiny catalog in the first 3 days** | core | 18 | `docs/DATA.md` (provenance, licence, simulation); catalog rebuildable from scratch with one command |
| B3 | **Back-end API (FastAPI):** endpoints from the contract; **server-side** image validation (format, size, real decode); handling of invalid file, oversized file, network error, empty catalog; runs on A's stub first, then the real engine; **filters** [opt]; **admin CRUD that calls A3's update-vector function** [opt]; pytest suite | core + opt | 27 | All endpoints match OpenAPI; one test per error case; no search logic outside `core/` |
| B4 | **Evaluation:** small query set judged for relevance, **Precision@K** [opt], **comparison of the two models** [opt], threshold calibration, **failure analysis of look-alike objects from different categories** | core + opt | 18 | `eval/` scripts + `docs/RESULTS.md` with tables/figures; each number reproducible with one command |
| B5 | **Wireframes:** home, results, product page (desktop + mobile) — **done early (weeks 1–2)** so A can build the UI | core | 6 | Images/PDF in `docs/wireframes/` |
| B6 | **Test plan & execution:** the assignment's §7 scenarios (home display and diversity, valid import from computer/phone, rejection of bad/oversized files, relevance across categories, ranking coherence, **different screen sizes**, errors); run them and record results | core | 8 | `docs/TEST_PLAN.md`: scenario, steps, expected, actual, pass/fail |
| B7 | **Test-query set (half, ~15 images)** + relevance judgements of the top results | core | 2 | Files + judgements file |
| B8 | **Report sections (B):** need analysis, data and catalog, database/API design, evaluation and results, tests, **limits of the model** | core | 15 | Drafted in `report/`, reviewed by A |

### Shared (both)
- `REFERENCES.md` kept up to date as resources are used.
- Kickoff session (~1 h): repo skeleton, read the three contracts together, agree on branch/PR rules.
- Final integration day: fresh-clone run, full test plan pass, report merge, tag `v1.0`.

## 4. Order of work (relative weeks — add dates once the deadline is known)

| Phase | Weeks | A | B | Exit criterion |
|-------|-------|---|---|----------------|
| 0 Kickoff | 0 | A1 | B1, repo skeleton | Three contracts frozen and reviewed by both |
| 1 Unblock | 1 | A2 (tiny), A3 start, A5 start on mock API | **B2 tiny catalog (≤3 days)**, B5, B3 on the stub | **M1:** end-to-end with the stub; tiny catalog searchable |
| 2 Core | 2–4 | A2 (full), A3, A4, A5 core, A6 | B2 (full), B3 core, B4 basics, B6 start | **M2: all [core] working** (swap one task here) |
| 3 Optional | 5–6 | A2 (2nd model), A3 [opt], A5 [opt] | B3 [opt], B4 comparison + Precision@K | **M3:** every §10 extension we chose is working |
| 4 Finish | 7–8 | A7, A8 | B6 complete, B7 | **M4:** tests all run, demo recorded |
| 5 Report | 9 | A9 | B8 | **M5:** report merged, `v1.0` tagged, submitted |

## 5. Dependencies (who waits on whom)

- **B2-tiny → A2/A3:** A needs a few hundred real images. Until then, A uses ~20 random images to test the code paths.
- **B5 → A5:** layout. A starts with the plain functional flow and restyles once the wireframes exist.
- **A1 → B3:** the API needs an engine → A1 is done in week 0 as a stub.
- **A2 + A3 → B4:** evaluation needs vectors and the engine → B builds the harness on the stub, then plugs in the real ones.
- **B3 → A5:** the front-end needs the API → mock API from the OpenAPI file.

## 6. Change log

| Date | Change | Agreed by |
|------|--------|-----------|
| 2026-11-19 | v0.1 initial draft | — |
| 2026-11-19 | v0.2: removed portfolio-only work; all assignment optional extensions (§10, §3.3) kept and spread across both packages | — |
| 2026-11-19 | v0.3: separate devlog files per person | Aissati Oussama, Afallah Bilal |
| 2026-11-21 | v0.4: repo is public (branch protection needs it on the Free plan); the assignment PDF is NOT committed to the repo (kept outside, git-ignored) | Aissati Oussama (Afallah Bilal to acknowledge) |
