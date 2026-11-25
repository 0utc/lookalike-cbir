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
### 2026-11-25 — @Oussama — B2a — Tiny catalog (500 products) built, merged and released
**Goal:** Build a balanced 500-product catalog from ABO with >=2 images per product, SQLite per CONTRACT_DB.md, and share it with Bilal.
**Done:** scripts/b2a_explore.py (stream listings, stats), scripts/b2a_build_tiny.py (seeded sample, image extraction, DB fill), scripts/pack_tiny.py, tests/test_tiny_catalog.py (4 passed). B1 contracts PR and tiny-catalog PR merged. Catalog zipped and published as GitHub Release data-tiny-v1. Added docs/DATA.md and SCOPE v1.2 (CC BY 4.0, amazon.com) in branch b2/data-doc.
**Findings / numbers:** 147,702 listings in total. amazon.in = 76,433 listings, of which 64,609 (85%) are CELLULAR_PHONE_CASE, so unusable as a balanced base. amazon.com = 19,616 listings, 384 product_types, 8,927 candidates in our 12 categories. Catalog: 12 categories, 41-42 products each, 1419 images, all 256 px max side. Toys: about 15 toy-like listings on amazon.com (7 are VIDEO_GAME_ACCESSORIES), so there is no toys category. Electronics is only accessories (phone cases, wireless accessories, office electronics).
**Problems & fixes:** Keyword buckets were misleading ("HAIR" matches CHAIR, "PHONE" matches phone cases), so the final mapping uses exact product_type values. images.csv.gz is a separate download (not in the image tar) and is needed for image_id -> path. docs/DATA.md had never been created, so it was added late.
**Decisions:** Marketplace = amazon.com (item_id unique, so source_id = item_id stays; pooling marketplaces would need domain in the key). 12 fine-grained categories with fixed quotas; seed 42 for selection, seed 43 (SEED+1) for prices/stock. Grocery excluded (packaging photos). Toys gap and thin electronics documented; B2b decision (drop toys / check other marketplaces / supplement) still open. Rule agreed: Bilal's PR approval counts as acknowledgement of the changes described in the PR.
**Next:** B5 wireframes (A5 depends on them), then B3a on the stub once A1 exists, then B2b. Kickoff session with Bilal and contract freeze (tag contracts-v1) still to do.

### 2026-11-24 — @Oussama — B2a prep — ABO licence and download route verified
**Goal:** Verify the ABO source, licence and download route before building the tiny catalog.
**Done:** Read the AWS Open Data registry page and the official ABO READMEs. Measured archive sizes with HTTP HEAD. Started downloading both archives to data\raw\.
**Findings / numbers:** Licence is CC BY 4.0 since 2023 (the paper, blog and AWS Marketplace still say CC BY-NC). Attribution: Amazon.com for the data; Guillaumin, Dideriksen, Deng, Arora, Collins, Malik for the dataset. We must say what we changed. abo-listings.tar = 87,480,320 B; abo-images-small.tar (256 px) = 3,253,381,120 B (about 3 GiB). Listings are 16 gzip JSON-lines files with multilingual fields (item_name, brand, item_id).
**Problems & fixes:** My earlier assumptions were wrong: SCOPE says non-commercial, and the GitHub Pages URL does not exist. The README recommends archives over per-image CDN URLs, so we use the archives.
**Decisions:** Use the archives, stored on O: under data\raw\ only (never C:). Extract only the selected images from the tar. DATA.md must credit the source and list our changes (resize, category mapping, simulated prices).
**Next:** Read the rest of the listings and images READMEs (category and image fields), write the B2a script (count products by category and image count), build the 500-product tiny catalog on branch b2/tiny-catalog.

### 2026-11-24 — @Oussama — B1 / M0 — Contract drafts and kickoff plan
**Goal:** Draft the DB and OpenAPI contracts and plan the kickoff session with Bilal.
**Done:** B0 closed (PR #1 merged, Bilal approved). Branch b1/contracts with docs/CONTRACT_DB.md (categories, products, product_images) and docs/openapi.yaml (catalog, text/image search, admin CRUD), validated with openapi-spec-validator. Kickoff agenda prepared.
**Findings / numbers:** Setup facts for the report/README: Python 3.11.9 at O:\TechTools\Tools\Python311 (not on PATH); each new shell needs .venv activation then scripts\env.ps1.
**Problems & fixes:** TASKS.md still says "package choice pending" and two change-log lines wait for Bilal's acknowledgement; to be fixed in one small shared PR after kickoff.
**Decisions:** products.id is AUTOINCREMENT and is the key in ids.npy. SearchEngine returns (id, score) only; the API joins with the DB. One image-search endpoint with optional q (text filters, image ranks). Admin protected by a shared X-Admin-Token. Currency EUR is a placeholder. Prices and stock simulated. All still drafts until Bilal reviews.
**Next:** Kickoff with Bilal, merge both contract PRs, tag contracts-v1 (M0). Then B2a: verify the ABO route and licence on the official page, count categories, build the 500-product tiny catalog within 3 days.

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
