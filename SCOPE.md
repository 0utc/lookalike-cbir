# SCOPE — Lookalike: visual-first product search

> Status: **FROZEN — 2026-11-19** (approved by both team members, see §13).
> From now on, scope changes only through a dated entry in the "Change log" at the bottom, agreed by both.
> Task division is in `TASKS.md`.

- Course: Python pour les sciences de données — mini-project "CBIR e-commerce" (2026/2027)
- Team: Aissati Oussama, Afallah Bilal
- Scope version: 1.2 — 2026-11-25

---

## 1. Vision

A web e-commerce application where a user finds products by **uploading or photographing an item**
(optionally combined with text) and gets visually similar products from a catalog, ranked by similarity.

Two goals, in this order:

1. **v1.0 — Assignment-complete.** Satisfies every functional and non-functional requirement of the
   course document and its test scenarios.
2. **v2.0 — Portfolio-grade.** The retrieval layer is treated as a small research project
   (multi-model comparison, hybrid fusion, rigorous evaluation), and the repo is reproducible,
   tested, containerised and documented well enough to present on a CV.

## 2. Differentiation (why this is not the "default" solution)

The default solution is ResNet50/MobileNetV2 + a fashion dataset + cosine similarity in Flask.
Ours differs in:

- A **less common dataset** (Amazon Berkeley Objects) with multi-view products, which gives
  built-in ground truth for evaluation.
- **Modern embedding models** (DINOv2, CLIP) compared against the classic baseline (MobileNetV2).
- **Hybrid fusion** of embeddings and proper joint text+image search via CLIP.
- **Quantitative evaluation** (Precision@K, Recall@K, ablations) and a **real-world photo test set**.
- **CPU-only, low-memory serving** with ONNX Runtime (int8) — the app runs on a 4 GB laptop.

## 3. In scope

### 3.1 Must-have (v1.0 — maps to the assignment)

| # | Feature | Assignment ref. |
|---|---------|-----------------|
| M1 | Catalog of products across several categories, stored in a database (id, name, category, price, image path; plus brand/description when available) | §5 |
| M2 | Home page: text search box (optional), image picker (file / phone camera where supported), preview with replace/cancel, search button enabled only when input is valid, loading indicator, clear error messages | §3.1 |
| M3 | Suggested-products grid, randomised per visit/refresh, multi-category, responsive, links to a product page | §3.1 |
| M4 | Server-side image validation (type, size, real image decoding) — never trust the browser only | §3.2, §6 |
| M5 | Preprocessing + feature extraction with a pretrained model (final classification layer removed) | §3.2 |
| M6 | Pre-computed catalog vectors, stored; only the query vector is computed at search time | §5, §6 |
| M7 | Similarity ranking (cosine) with FAISS-backed nearest-neighbour search; results sorted most→least similar | §3.2 |
| M8 | Results page: image, name, price, category/brand, similarity indicator; explicit "no relevant result" message | §3.2 |
| M9 | Text search working independently, **and** text+image combination (design choice explained in the report) | §3.3 |
| M10 | Robustness: invalid file, oversized file, network error, empty catalog | §6 |
| M11 | Modular code (front-end / API / retrieval core / database), documented main functions | §6 |
| M12 | Test scenarios from §7 of the assignment, plus automated tests. Includes: home-page display and product diversity; valid image import from computer and phone; rejection of unsupported/oversized files; relevance across several categories; coherent ranking; behaviour on different screen sizes (desktop, tablet, phone — tested explicitly) and error handling | §7 |
| M13 | Deliverables: code, loadable catalog data + instructions, test-image set (provenance documented), install/usage guide, short demo, and a **report** containing: the need, the architecture, the technical choices (justified), the CBIR algorithm, the tests, the limits, and a discussion of cases where objects of different categories look alike | §8, §7 |
| M14 | **Explainability (oral):** both members can explain (a) image classification vs. similar-image retrieval, (b) the role of the feature vector, (c) the chosen similarity measure, (d) the ranking method. Covered by a dedicated report section ("CBIR explained") | §12 |
| M15 | **References:** every external resource reused (code, model, dataset, image) is listed in the report and in a `REFERENCES.md` kept up to date during development | §12 |
| M16 | **Mockups:** wireframes of the main screens (home, results, product page; desktop + mobile) produced before front-end implementation and included in the report | §11 (Phase 1) |

### 3.2 Should-have (v2.0 — portfolio differentiators)

| # | Feature | Assignment ref. |
|---|---------|-----------------|
| S1 | Three feature extractors benchmarked: MobileNetV2 (baseline), DINOv2-Small, CLIP ViT-B/32 | §10 (two-model comparison) |
| S2 | Hybrid fusion of embeddings (weighted / concatenated), with ablation table | — |
| S3 | Evaluation protocol: Precision@K by category; Recall@K for same-product retrieval (alternate photo of the same product as query); ~100 self-shot real-world phone photos; failure analysis | §7 |
| S4 | Filters by category / price / brand | §10 |
| S5 | Similarity score with an explanation of how to interpret it | §10 |
| S6 | Admin area: add/edit/delete products; embedding recomputed automatically when an image changes | §10 |
| S7 | ONNX export + int8 quantisation; latency and memory measurements | — |
| S8 | Docker, GitHub Actions CI (lint + tests), `make` targets for one-command setup | — |
| S9 | Public demo (free hosting) + write-up for portfolio | — |

### 3.3 Could-have (only if everything above is done)

- Object cropping/segmentation of the query before embedding (to reduce background influence).
- Colour-aware re-ranking.
- Query-by-multiple-images.
- French/English UI toggle.

## 4. Out of scope

- User accounts, cart, checkout, payments, order management.
- Training or fine-tuning a model from scratch (only pretrained extractors; light fine-tuning is
  at most a could-have experiment).
- Large-scale deployment (>100k products), GPUs in production, mobile native apps.
- Commercial use of the ABO catalog (ABO is CC BY 4.0: attribution required; our use is academic/portfolio only).

## 5. Data

- **Source:** Amazon Berkeley Objects (ABO) — product listings metadata + catalog images.
- **Subset:** ~15–20k products, chosen to cover ≥ 10–12 categories with a balanced count per category
  and to keep products that have **≥ 2 images** (needed for same-product evaluation).
- **Prices:** not provided by ABO → **simulated** with a seeded, per-category distribution.
  This must be stated plainly in the app footer/README and in the report.
- **Images:** ≤ 256 px thumbnails. **Never committed to Git.** Published as a downloadable artefact
  (Hugging Face Hub dataset repo or GitHub Release) and fetched by a `make data` script.
- **Licence:** ABO is distributed under CC BY 4.0 (attribution required; verified on the official ABO page). Attribution is included in the shared catalog artefact and must be repeated in the README and the report. Our project is academic/portfolio only.
- **To verify in the first data task:** that categories matching the assignment's examples
  (fashion, home, electronics, beauty, toys) are sufficiently represented. If a category is too thin,
  document it and supplement it from another open dataset (recorded in the report's references).

## 6. Models and retrieval design

| Role | Model | Dim. | Notes |
|------|-------|------|-------|
| Baseline | MobileNetV2 (ImageNet, no top layer) | 1280 | The assignment's suggested model |
| Visual instance matching | DINOv2 ViT-S/14 | 384 | Strong for "same/similar object" |
| Semantic + text | CLIP ViT-B/32 | 512 | Image and text encoders share one space |

- **Similarity:** cosine similarity on L2-normalised vectors (inner product in FAISS).
- **Index:** FAISS flat index (exact) — adequate at this scale; HNSW only if benchmarked as useful.
- **Fusion:** score-level weighted fusion of per-model similarities; weights tuned on a validation split.
- **Text + image:** v1.0 baseline = text filters by keyword/category, then image similarity ranks.
  v2.0 = CLIP text embedding blended with the image embedding. Final choice justified by the experiments.
- **"No relevant result":** threshold on the top-1 similarity, calibrated on validation data (not guessed).
- **Embedding compute:** offline on Kaggle/Colab (GPU). **Serving:** ONNX Runtime on CPU; the
  backend never imports PyTorch.

## 7. Architecture (target)

```
┌────────────┐   HTTPS/JSON    ┌───────────────────────────────┐
│ React app  │ ──────────────► │ FastAPI (thin layer)          │
│ (Vite)     │ ◄────────────── │  - validation, routing, auth  │
└────────────┘                 └──────────────┬────────────────┘
                                              │ calls
                               ┌──────────────▼────────────────┐
                               │ core/ (framework-independent) │
                               │  - preprocessing              │
                               │  - ONNX embedders             │
                               │  - FAISS index + fusion       │
                               └───────┬───────────────┬───────┘
                                       │               │
                              ┌────────▼──────┐  ┌─────▼────────────┐
                              │ SQLite        │  │ embeddings/*.npy │
                              │ (catalog)     │  │ + FAISS files    │
                              └───────────────┘  └──────────────────┘
```

Contracts that both team members code against (to be written in `docs/` before implementation):
OpenAPI spec of the REST API; database schema; embedding file format
(`ids.npy` + `<model>.npy` + FAISS index, rows aligned by product id).

## 8. Tech stack

| Layer | Choice |
|-------|--------|
| Front-end | React + Vite + Tailwind (responsive) |
| Back-end | FastAPI (Python 3.11), SQLAlchemy |
| Database | SQLite (schema kept PostgreSQL-compatible) |
| Vision | ONNX Runtime (serving); PyTorch/transformers only in offline notebooks |
| Vectors | NumPy, FAISS (cpu) |
| Eval | scikit-learn, pandas, matplotlib |
| Quality | pytest, ruff, GitHub Actions |
| Packaging | Docker / docker-compose, Makefile |

> Note on the framework: the assignment names Flask or Django. FastAPI is our decision (final); the
> framework-independent `core/` package keeps a switch cheap if the instructor ever requires it.

## 9. Evaluation plan (summary)

1. **Category precision:** query = held-out catalog image; relevant = same category → Precision@K (K = 1, 5, 10).
2. **Same-product retrieval:** query = alternate photo of a product; relevant = that product → Recall@K, MRR.
3. **Real-world photos:** ~100 phone photos of everyday objects matching catalog categories; manual relevance
   judgement of the top-K → Precision@K; analysis of the domain gap.
4. **Ablations:** each model alone vs. fusion; text-only vs. image-only vs. combined; threshold effect.
5. **Systems metrics:** query latency (p50/p95) and RAM on a 4 GB CPU-only machine, FP32 vs int8.
6. **Failure analysis:** examples of cross-category look-alikes and why they happen (required by §7).

## 10. Constraints and risks

| Risk | Mitigation |
|------|------------|
| Low-spec dev machines (design target: 4 GB RAM, CPU only; teammate's specs may differ) | Offline GPU compute on Kaggle/Colab; ONNX int8 serving; Vite; no PyTorch in the backend |
| 64 GB eMMC storage | Raw data on external SSD; ≤ 256 px thumbnails; no images in Git |
| ABO category coverage mismatch with assignment examples | Verify in the first data task; supplement if needed |
| Real-world photos perform worse than catalog queries | Treat as a finding (domain-gap analysis); optional cropping |
| Two people working independently → integration drift | Contract-first (OpenAPI/schema/format), stub engine + mock API, PR review by the other person |
| Time | v1.0 is defined narrowly; v2.0 items are strictly optional and ordered by value |

## 11. Definition of done

**v1.0 is done when:** all Must-have items work end-to-end; the assignment's test scenarios pass;
the report (with all required contents, the "CBIR explained" section and references), wireframes, install guide,
test-image set and demo exist; the responsive-layout and error-handling tests have been run; a fresh clone can be
run by following the README.

**v2.0 is done when:** S1–S3 and S7–S8 are complete with real measured results in the repo; the README
has the benchmark table and screenshots; a tagged release exists.

## 12. Open questions — answered

1. Submission deadline: **not announced yet** — "a few days after the professor's final exam". Plan with relative weeks;
   aim to have all [core] tasks done at least one week before the final exam date, and put real dates in `PROGRESS.md`
   as soon as the exam date/deadline is known.
2. FastAPI vs Flask/Django: **FastAPI** (final). The assignment does not forbid it.
3. Language of the report / UI: to be decided with the professor's expectations (the course document is in French) —
   default: report in French, UI in French (English strings kept in a single translation file).
4. Instructor requirements on categories / catalog size: none beyond the assignment document.
5. Teammates' hardware: not recorded in the repo (each person tells their own Claude privately). Design target stays:
   CPU-only, 4 GB RAM.

## 13. Approval

| Member | Approved | Date |
|--------|----------|------|
| Aissati Oussama | ☑ | 2026-11-16 |
| Afallah Bilal | ☑ | 2026-11-19 |

## 14. Change log

| Date | Change | Agreed by |
|------|--------|-----------|
| 2026-11-16 | v0.1 initial draft | — |
| 2026-11-16 | v0.2: added full report contents (M13), oral explainability (M14), references (M15), wireframes (M16), explicit screen-size tests (M12) after a line-by-line check against the assignment | — |
| 2026-11-19 | v1.0: scope frozen after approval by both members | Aissati Oussama, Afallah Bilal |
| 2026-11-19 | v1.1: open questions answered (deadline TBD, FastAPI final, hardware not recorded); no change of scope | Aissati Oussama (Afallah Bilal to acknowledge) |
| 2026-11-25 | v1.2: licence corrected to CC BY 4.0 (ABO); marketplace fixed to amazon.com, so source_id = item_id. Wording and data-source fix, not a scope change. | Aissati Oussama (Bilal's approval of this PR = acknowledgement, also for v1.1 and TASKS v0.4) |
