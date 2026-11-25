# DATA — Lookalike catalog

Status: B2a (tiny catalog) done. B2b (full catalog) will extend this file.

## Source and licence
- Dataset: Amazon Berkeley Objects (ABO), listings metadata + small catalog images (<= 256 px).
- Licence: CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). Attribution to Amazon.com / ABO is required
  (see `ATTRIBUTION.txt` inside the release zip). Our use is academic/portfolio only.
- Changes we made: category mapping, subset selection, simulated prices and stock, HTML stripped from descriptions.
- Raw files are never committed. Download them into `data/raw/` from the official ABO page:
  `abo-listings.tar`, `abo-images-small.tar`, `images.csv.gz` (separate download: image_id -> path).

## Tiny catalog (B2a)
- Marketplace: `amazon.com` only. `item_id` is unique inside one marketplace, so `products.source_id = item_id`.
  Pooling several marketplaces (B2b) would need `domain_name` in the key (contract change).
- 500 products, 12 fine-grained categories, 41-42 products each, fixed quota, selection seed 42.
- Categories (slug: ABO product_type values): shoes (SHOES, SANDAL, BOOT); jewelry (FINERING, FINEEARRING,
  FINENECKLACEBRACELETANKLET); chair (CHAIR, STOOL_SEATING); sofa (SOFA); table (TABLE, DESK); rug (RUG);
  lamp (LAMP, LIGHT_FIXTURE); wall_art (WALL_ART); pillow (PILLOW); bed (BED, HEADBOARD);
  beauty (BEAUTY, SKIN_CLEANING_AGENT, SKIN_MOISTURIZER);
  electronics (CELLULAR_PHONE_CASE, WIRELESS_ACCESSORY, OFFICE_ELECTRONICS).
- Selection rules: English name, a main image and at least one extra view. Each product keeps its main image
  plus up to 2 extra views (`product_images`, used for same-product evaluation). GROCERY excluded (packaging photos).
- 1419 images, all 256 px on the long side.
- Names and descriptions are the English ABO values (descriptions stripped of HTML, capped at 1000 characters).

## Simulated fields
ABO has no prices or stock. Both are SIMULATED and seeded (seed 43 = selection seed + 1, so changing a price range
never changes which products are selected): price uniform in a per-category range, ending in .99;
about 15% of products out of stock, otherwise 1-200 units. Currency EUR is a placeholder.
This is stated in the app footer, README and report.

## Known gaps (to document in the report)
- **Toys:** about 15 toy-like listings on amazon.com (7 are VIDEO_GAME_ACCESSORIES): no toys category.
- **Electronics:** only accessories (phone cases, wireless accessories, office electronics).
- amazon.in was rejected: 85% of its listings are CELLULAR_PHONE_CASE.
- Decision pending for B2b: drop toys, check other marketplaces, or supplement from another open dataset.

## Rebuild and sharing
```powershell
python scripts\b2a_explore.py              # stats + data\interim\listings_index.jsonl.gz
python scripts\b2a_build_tiny.py           # DB + images (data\catalog_tiny.db, data\images)
python scripts\pack_tiny.py                # data\lookalike-tiny-catalog.zip
```
Paths come from `.env` (`DATA_DIR`, `IMAGES_DIR`, `DB_PATH`), never hard-coded.
Shared artefact: GitHub Release `data-tiny-v1` (`lookalike-tiny-catalog.zip`: DB + images + ATTRIBUTION.txt).
Unzip it anywhere and point `IMAGES_DIR` and `DB_PATH` to it.