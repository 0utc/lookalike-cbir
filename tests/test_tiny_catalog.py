"""Integrity checks for the tiny catalog (skipped if it has not been built)."""
import os
import sqlite3
from pathlib import Path

import pytest

DATA = Path(os.environ.get("DATA_DIR", "data"))
DB_PATH = Path(os.environ.get("DB_PATH", DATA / "catalog_tiny.db"))
IMAGES_DIR = Path(os.environ.get("IMAGES_DIR", DATA / "images"))

pytestmark = pytest.mark.skipif(not DB_PATH.exists(), reason="tiny catalog not built")


@pytest.fixture(scope="module")
def con():
    c = sqlite3.connect(DB_PATH)
    yield c
    c.close()


def test_size_and_unique_source_ids(con):
    n, n_src = con.execute("SELECT COUNT(*), COUNT(DISTINCT source_id) FROM products").fetchone()
    assert n == 500 and n_src == 500


def test_every_product_has_an_extra_view(con):
    n = con.execute("SELECT COUNT(*) FROM products p WHERE NOT EXISTS "
                    "(SELECT 1 FROM product_images i WHERE i.product_id = p.id)").fetchone()[0]
    assert n == 0


def test_image_files_exist_and_paths_are_relative(con):
    paths = [r[0] for r in con.execute(
        "SELECT image_path FROM products UNION SELECT image_path FROM product_images")]
    for p in paths:
        assert not os.path.isabs(p) and "\\" not in p
        assert (IMAGES_DIR / p).is_file(), p


def test_prices_stock_and_categories(con):
    assert con.execute("SELECT COUNT(*) FROM products WHERE price < 0 OR stock_quantity < 0").fetchone()[0] == 0
    counts = [c for (c,) in con.execute("SELECT COUNT(*) FROM products GROUP BY category_id")]
    assert len(counts) == 12 and max(counts) - min(counts) <= 1