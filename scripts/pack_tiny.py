"""Zip the tiny catalog (DB + images + licence/attribution) for sharing as a GitHub Release asset."""
import os
import zipfile
from pathlib import Path

DATA = Path(os.environ.get("DATA_DIR", "data"))
IMAGES_DIR = Path(os.environ.get("IMAGES_DIR", DATA / "images"))
DB_PATH = Path(os.environ.get("DB_PATH", DATA / "catalog_tiny.db"))
OUT = DATA / "lookalike-tiny-catalog.zip"

ATTRIBUTION = (
    "Product data and images: Amazon Berkeley Objects (ABO), Amazon.com, "
    "licensed CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/).\n"
    "This subset (500 products, amazon.com) was selected and re-packaged for an academic project. "
    "Prices and stock are SIMULATED (seed 42), not real.\n"
)

with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
    z.write(DB_PATH, "catalog_tiny.db")
    z.writestr("ATTRIBUTION.txt", ATTRIBUTION)
    for p in sorted(IMAGES_DIR.rglob("*.jpg")):
        z.write(p, "images/" + p.relative_to(IMAGES_DIR).as_posix())
print(OUT, round(OUT.stat().st_size / 1e6, 1), "MB")