"""B2a: build the 500-product tiny catalog (SQLite + thumbnails).

Pipeline: candidates from the listings index -> image paths from images.csv.gz
-> seeded balanced sample -> descriptions (listings pass) -> extract only the
chosen images (one sequential pass over the image tar) -> fill SQLite per
docs/CONTRACT_DB.md. Prices and stock are SIMULATED (seeded).

Run from the repo root:  python scripts/b2a_build_tiny.py
Rebuilds from scratch every time (deletes the old tiny DB).
"""
import csv
import gzip
import html
import json
import os
import random
import re
import sqlite3
import tarfile
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image

SEED = 42
DOMAIN = "amazon.com"        # one marketplace -> item_id is unique (source_id)
N_PRODUCTS = 500
MAX_EXTRA_IMAGES = 2         # extra views kept per product (besides the main one)

DATA = Path(os.environ.get("DATA_DIR", "data"))
RAW, INTERIM = DATA / "raw", DATA / "interim"
IMAGES_DIR = Path(os.environ.get("IMAGES_DIR", DATA / "images"))
DB_PATH = Path(os.environ.get("DB_PATH", DATA / "catalog_tiny.db"))
INDEX = INTERIM / "listings_index.jsonl.gz"
IMG_TAR, LIST_TAR = RAW / "abo-images-small.tar", RAW / "abo-listings.tar"
IMG_CSV = RAW / "images.csv.gz"

# slug: (name_en, name_fr, [ABO product_type values], (min_price, max_price) simulated)
CATEGORIES = {
    "shoes":       ("Shoes", "Chaussures", ["SHOES", "SANDAL", "BOOT"], (25, 150)),
    "jewelry":     ("Jewelry", "Bijoux", ["FINERING", "FINEEARRING", "FINENECKLACEBRACELETANKLET"], (30, 400)),
    "chair":       ("Chairs", "Chaises", ["CHAIR", "STOOL_SEATING"], (40, 350)),
    "sofa":        ("Sofas", "Canapés", ["SOFA"], (250, 1500)),
    "table":       ("Tables", "Tables", ["TABLE", "DESK"], (60, 600)),
    "rug":         ("Rugs", "Tapis", ["RUG"], (30, 500)),
    "lamp":        ("Lamps & lighting", "Luminaires", ["LAMP", "LIGHT_FIXTURE"], (20, 250)),
    "wall_art":    ("Wall art", "Décoration murale", ["WALL_ART"], (15, 200)),
    "pillow":      ("Pillows", "Coussins", ["PILLOW"], (10, 60)),
    "bed":         ("Beds", "Lits", ["BED", "HEADBOARD"], (150, 1200)),
    "beauty":      ("Beauty & skin care", "Beauté et soins",
                    ["BEAUTY", "SKIN_CLEANING_AGENT", "SKIN_MOISTURIZER"], (5, 80)),
    "electronics": ("Phone & electronics accessories", "Accessoires électroniques",
                    ["CELLULAR_PHONE_CASE", "WIRELESS_ACCESSORY", "OFFICE_ELECTRONICS"], (8, 120)),
}
TOY_WORDS = ("TOY", "GAME", "PUZZLE", "DOLL")

DDL = """
CREATE TABLE categories (
  id INTEGER PRIMARY KEY, slug TEXT NOT NULL UNIQUE,
  name_en TEXT NOT NULL, name_fr TEXT NOT NULL);
CREATE TABLE products (
  id INTEGER PRIMARY KEY AUTOINCREMENT, source_id TEXT UNIQUE,
  name TEXT NOT NULL, category_id INTEGER NOT NULL REFERENCES categories(id),
  brand TEXT, description TEXT,
  price NUMERIC(10,2) NOT NULL CHECK (price >= 0),
  currency CHAR(3) NOT NULL DEFAULT 'EUR',
  stock_quantity INTEGER NOT NULL DEFAULT 0 CHECK (stock_quantity >= 0),
  image_path TEXT NOT NULL, created_at TEXT NOT NULL, updated_at TEXT NOT NULL);
CREATE INDEX ix_products_category ON products(category_id);
CREATE INDEX ix_products_price ON products(price);
CREATE INDEX ix_products_brand ON products(brand);
CREATE TABLE product_images (
  id INTEGER PRIMARY KEY,
  product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
  image_path TEXT NOT NULL, UNIQUE (product_id, image_path));
"""


def english_value(field):
    """Return the English value of an ABO language-tagged list, else None."""
    if isinstance(field, list):
        for e in field:
            if str(e.get("language_tag", "")).lower().startswith("en"):
                return e.get("value")
    return None


def clean_html(text, limit=1000):
    """Strip tags/entities from an ABO description and cap its length."""
    if not text:
        return None
    text = html.unescape(re.sub(r"<[^>]+>", " ", text))
    text = re.sub(r"\s+", " ", text).strip()
    return text[:limit] or None


def load_candidates():
    """Eligible products per category slug (amazon.com, >=1 extra image, English name)."""
    ptype_to_slug = {p: s for s, (_, _, pts, _) in CATEGORIES.items() for p in pts}
    cands, seen = defaultdict(list), set()
    toy_types = Counter()
    with gzip.open(INDEX, "rt", encoding="utf-8") as fh:
        for line in fh:
            r = json.loads(line)
            if r["domain"] != DOMAIN:
                continue
            if r["ptype"] and any(w in r["ptype"] for w in TOY_WORDS):
                toy_types[r["ptype"]] += 1
            slug = ptype_to_slug.get(r["ptype"])
            if not slug or not r["name_en"] or not r["main"] or not r["others"]:
                continue
            if r["item_id"] in seen:
                continue
            seen.add(r["item_id"])
            cands[slug].append(r)
    print("Toy-like product_type on", DOMAIN, ":", dict(toy_types))
    return cands


def load_image_paths(image_ids):
    """image_id -> relative path (e.g. '00/00834536.jpg'), only for the ids we need."""
    paths = {}
    with gzip.open(IMG_CSV, "rt", encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            if row["image_id"] in image_ids:
                paths[row["image_id"]] = row["path"]
    return paths


def pick_images(rec, paths):
    """Main + up to MAX_EXTRA_IMAGES other views that exist in images.csv; None if unusable."""
    main = paths.get(rec["main"])
    extras = []
    for i in rec["others"]:
        p = paths.get(i)
        if p and p != main and p not in extras:
            extras.append(p)
    if not main or not extras:
        return None
    return main, extras[:MAX_EXTRA_IMAGES]


def sample(cands, paths):
    """Seeded balanced sample: fixed quota per category (remainder to the first ones)."""
    rng = random.Random(SEED)
    base, extra = divmod(N_PRODUCTS, len(CATEGORIES))
    chosen = {}
    for k, slug in enumerate(CATEGORIES):
        quota = base + (1 if k < extra else 0)
        pool = sorted((r for r in cands[slug] if pick_images(r, paths)), key=lambda r: r["item_id"])
        rng.shuffle(pool)
        if len(pool) < quota:
            print(f"WARNING: {slug} has only {len(pool)} usable products (quota {quota})")
        for r in pool[:quota]:
            r["slug"] = slug
            r["main_path"], r["extra_paths"] = pick_images(r, paths)
            chosen[r["item_id"]] = r
    return chosen


def fetch_descriptions(chosen):
    """One streaming pass over the listings to get the English description."""
    n = 0
    with tarfile.open(LIST_TAR, "r|") as tf:
        for m in tf:
            if not (m.isfile() and os.path.basename(m.name).startswith("listings_")):
                continue
            with gzip.open(tf.extractfile(m), "rt", encoding="utf-8") as fh:
                for line in fh:
                    d = json.loads(line)
                    if d.get("domain_name") == DOMAIN and d.get("item_id") in chosen:
                        chosen[d["item_id"]]["description"] = clean_html(
                            english_value(d.get("product_description")))
                        n += 1
    print(f"Descriptions pass done ({n} listings matched)")


def extract_images(chosen):
    """One sequential pass over the image tar; extract only the wanted files."""
    wanted = set()
    for r in chosen.values():
        wanted.add(r["main_path"])
        wanted.update(r["extra_paths"])
    remaining = {"images/small/" + p: p for p in wanted}
    sizes = []
    with tarfile.open(IMG_TAR, "r|") as tf:
        for m in tf:
            rel = remaining.pop(m.name, None)
            if rel is None:
                continue
            out = IMAGES_DIR / rel
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(tf.extractfile(m).read())
            with Image.open(out) as im:
                sizes.append(im.size)
            if not remaining:
                break
    if remaining:
        raise SystemExit(f"{len(remaining)} wanted images not found in the tar, e.g. {next(iter(remaining))}")
    print(f"Extracted {len(sizes)} images to {IMAGES_DIR}")
    print(f"Image size (w,h): max side min={min(max(s) for s in sizes)}, max={max(max(s) for s in sizes)}")


def fill_db(chosen):
    """Create the SQLite DB per CONTRACT_DB.md and insert the sample."""
    rng = random.Random(SEED + 1)  # separate stream for simulated prices/stock
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    if DB_PATH.exists():
        DB_PATH.unlink()
    con = sqlite3.connect(DB_PATH)
    con.execute("PRAGMA foreign_keys = ON")
    con.executescript(DDL)
    cat_id = {}
    for i, (slug, (en, fr, _, _)) in enumerate(CATEGORIES.items(), start=1):
        con.execute("INSERT INTO categories VALUES (?,?,?,?)", (i, slug, en, fr))
        cat_id[slug] = i
    for r in sorted(chosen.values(), key=lambda r: (list(CATEGORIES).index(r["slug"]), r["item_id"])):
        lo, hi = CATEGORIES[r["slug"]][3]
        price = round(rng.uniform(lo, hi)) - 0.01           # simulated, ends in .99
        stock = 0 if rng.random() < 0.15 else rng.randint(1, 200)  # ~15% out of stock
        cur = con.execute(
            "INSERT INTO products (source_id,name,category_id,brand,description,price,currency,"
            "stock_quantity,image_path,created_at,updated_at) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            (r["item_id"], r["name_en"], cat_id[r["slug"]], r["brand_en"], r.get("description"),
             price, "EUR", stock, r["main_path"], now, now))
        for p in r["extra_paths"]:
            con.execute("INSERT INTO product_images (product_id,image_path) VALUES (?,?)",
                        (cur.lastrowid, p))
    con.commit()
    for slug, n in con.execute("SELECT c.slug, COUNT(*) FROM products p JOIN categories c "
                               "ON c.id=p.category_id GROUP BY c.slug ORDER BY c.id"):
        print(f"  {slug}: {n}")
    print("Total products:", con.execute("SELECT COUNT(*) FROM products").fetchone()[0])
    con.close()


if __name__ == "__main__":
    cands = load_candidates()
    ids = {i for lst in cands.values() for r in lst for i in [r["main"], *r["others"]]}
    paths = load_image_paths(ids)
    print(f"Candidates: {sum(map(len, cands.values()))}, image paths resolved: {len(paths)}")
    chosen = sample(cands, paths)
    fetch_descriptions(chosen)
    extract_images(chosen)
    fill_db(chosen)
    print("DB:", DB_PATH)