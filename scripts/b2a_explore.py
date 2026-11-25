"""B2a step 1: explore ABO without extracting anything.

- Lists the first entries of the image tar (layout check).
- Streams the listings tar (no extraction to disk), writes a compact index
  of every listing to data/interim/listings_index.jsonl.gz.
- Prints counts: marketplaces, product_type, image counts, and a
  keyword-based coverage check for the assignment's example categories.

Run from the repo root:  python scripts/b2a_explore.py [domain_name]
"""
import gzip
import json
import os
import sys
import tarfile
from collections import Counter
from pathlib import Path

DATA = Path(os.environ.get("DATA_DIR", "data"))
RAW = DATA / "raw"
INTERIM = DATA / "interim"
IMG_TAR = RAW / "abo-images-small.tar"
LIST_TAR = RAW / "abo-listings.tar"
EXPECTED_IMG_TAR_BYTES = 3253381120

# Heuristic buckets (substring of product_type). Checked in this order.
# This is only a coverage CHECK; the real mapping is decided after seeing the numbers.
BUCKETS = {
    "electronics": ["PHONE", "HEADPHONE", "ELECTRONIC", "COMPUTER", "CABLE",
                    "CHARGER", "SPEAKER", "CAMERA", "LAPTOP", "TABLET"],
    "toys": ["TOY", "GAME", "PUZZLE", "DOLL"],
    "beauty": ["BEAUTY", "SKIN", "HAIR", "COSMETIC", "PERFUME", "MAKEUP"],
    "fashion": ["SHOE", "SHIRT", "DRESS", "SANDAL", "BOOT", "PANTS", "SWEATER",
                "JACKET", "HANDBAG", "SOCK", "HAT", "COAT", "SKIRT"],
    "home": ["CHAIR", "SOFA", "TABLE", "LAMP", "RUG", "BED", "HOME", "FURNITURE",
             "PILLOW", "DECOR", "CURTAIN", "SHELF"],
}


def first_value(field):
    """ABO text fields are lists of {language_tag, value}; type fields may too."""
    if isinstance(field, list) and field:
        return field[0].get("value")
    return field if isinstance(field, str) else None


def english_value(field):
    """Return the English value of a language-tagged list, else None."""
    if isinstance(field, list):
        for e in field:
            if str(e.get("language_tag", "")).lower().startswith("en"):
                return e.get("value")
    return None


def bucket_of(ptype):
    p = (ptype or "").upper()
    for name, words in BUCKETS.items():
        if any(w in p for w in words):
            return name
    return "other"


def check_image_tar():
    size = IMG_TAR.stat().st_size
    ok = "OK" if size == EXPECTED_IMG_TAR_BYTES else "MISMATCH"
    print(f"Image tar size: {size} bytes (expected {EXPECTED_IMG_TAR_BYTES}) -> {ok}")
    print("First entries of the image tar:")
    with tarfile.open(IMG_TAR, "r|") as tf:  # stream mode: no member index in RAM
        for i, m in enumerate(tf):
            print(f"  {m.name}  ({m.size} bytes)")
            if i >= 14:
                break


def build_index():
    INTERIM.mkdir(parents=True, exist_ok=True)
    out_path = INTERIM / "listings_index.jsonl.gz"
    n = 0
    with tarfile.open(LIST_TAR, "r|") as tf, gzip.open(out_path, "wt", encoding="utf-8") as out:
        for m in tf:
            base = os.path.basename(m.name)
            if not (m.isfile() and base.startswith("listings_") and base.endswith(".json.gz")):
                continue
            with gzip.open(tf.extractfile(m), "rt", encoding="utf-8") as fh:
                for line in fh:
                    d = json.loads(line)
                    others = d.get("other_image_id") or []
                    main = d.get("main_image_id")
                    rec = {
                        "item_id": d.get("item_id"),
                        "domain": d.get("domain_name"),
                        "ptype": first_value(d.get("product_type")),
                        "name_en": english_value(d.get("item_name")),
                        "brand_en": english_value(d.get("brand")),
                        "main": main,
                        "others": others,
                        "n_images": (1 if main else 0) + len(others),
                    }
                    out.write(json.dumps(rec) + "\n")
                    n += 1
            print(f"  read {base} (total {n} listings)")
    return out_path, n


def report(index_path, domain_arg):
    domains, per_type, per_type_ge2, hist = Counter(), Counter(), Counter(), Counter()
    rows = []
    with gzip.open(index_path, "rt", encoding="utf-8") as fh:
        for line in fh:
            r = json.loads(line)
            domains[r["domain"]] += 1
            rows.append((r["domain"], r["ptype"], r["n_images"], bool(r["name_en"])))
    domain = domain_arg or domains.most_common(1)[0][0]
    lines = ["Marketplaces (domain_name): " + ", ".join(f"{d}={c}" for d, c in domains.most_common(10))]
    lines.append(f"Chosen marketplace: {domain}")
    bucket_all, bucket_ok = Counter(), Counter()
    for dom, ptype, n_img, has_en in rows:
        if dom != domain:
            continue
        hist[min(n_img, 6)] += 1
        per_type[ptype] += 1
        ok = n_img >= 2 and has_en
        if ok:
            per_type_ge2[ptype] += 1
        b = bucket_of(ptype)
        bucket_all[b] += 1
        bucket_ok[b] += ok
    lines.append("Images per product (6 = 6 or more): " + str(dict(sorted(hist.items()))))
    lines.append("Distinct product_type: %d" % len(per_type))
    lines.append("\nTop 60 product_type: total / usable (>=2 images and English name)")
    for p, c in per_type.most_common(60):
        lines.append(f"  {p}: {c} / {per_type_ge2[p]}")
    lines.append("\nHeuristic coverage (bucket: total / usable)")
    for b in list(BUCKETS) + ["other"]:
        lines.append(f"  {b}: {bucket_all[b]} / {bucket_ok[b]}")
    text = "\n".join(lines)
    (INTERIM / "abo_stats.txt").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    index = INTERIM / "listings_index.jsonl.gz"
    if index.exists():
        print(f"Reusing existing index: {index}")
        total = None
    else:
        check_image_tar()
        print("\nStreaming listings...")
        index, total = build_index()
    report(index, sys.argv[1] if len(sys.argv) > 1 else None)