# CONTRACT — Database schema (B1)

Status: DRAFT — to be frozen at M0 after review by both members.
Engine: SQLite (dev). Schema kept PostgreSQL-compatible (no SQLite-only types;
SQLAlchemy models are the source of truth for the DDL; this file is the human contract).

## Tables

```sql
CREATE TABLE categories (
  id      INTEGER PRIMARY KEY,
  slug    TEXT NOT NULL UNIQUE,          -- e.g. 'chair', 'shoes'
  name_en TEXT NOT NULL,
  name_fr TEXT NOT NULL                  -- UI is French by default
);

CREATE TABLE products (
  id             INTEGER PRIMARY KEY AUTOINCREMENT,  -- never reused (see rules)
  source_id      TEXT UNIQUE,            -- ABO item_id; NULL for admin-created products
  name           TEXT NOT NULL,
  category_id    INTEGER NOT NULL REFERENCES categories(id),
  brand          TEXT,                   -- nullable: not always available
  description    TEXT,                   -- nullable
  price          NUMERIC(10,2) NOT NULL CHECK (price >= 0),   -- SIMULATED
  currency       CHAR(3) NOT NULL DEFAULT 'EUR',
  stock_quantity INTEGER NOT NULL DEFAULT 0 CHECK (stock_quantity >= 0),  -- SIMULATED
  image_path     TEXT NOT NULL,          -- main image, relative to IMAGES_DIR, '/' separators
  created_at     TEXT NOT NULL,          -- ISO 8601 UTC
  updated_at     TEXT NOT NULL
);
CREATE INDEX ix_products_category ON products(category_id);
CREATE INDEX ix_products_price    ON products(price);
CREATE INDEX ix_products_brand    ON products(brand);

-- Extra views of a product (used by the same-product evaluation, B4). Not served by the UI.
CREATE TABLE product_images (
  id         INTEGER PRIMARY KEY,
  product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
  image_path TEXT NOT NULL,
  UNIQUE (product_id, image_path)
);
```

## Rules

1. **Embedding alignment:** `products.id` is the key stored in `ids.npy` (int64). Ids are never
   reused (AUTOINCREMENT), otherwise a deleted product's stale vector could point to a new product.
2. **Availability** is derived: `in_stock = stock_quantity > 0`. No separate column.
3. **Prices and stock are simulated** (seeded, per-category distribution). Stated in the app footer,
   README, `docs/DATA.md` and the report. Currency `EUR` is a placeholder decision.
4. **Paths:** `image_path` is relative to `IMAGES_DIR` (from `.env`); never absolute, never hard-coded.
5. **Names/descriptions:** English (ABO's `en_*` values). The UI is French, so the catalog stays English.
   Category names exist in both languages.
6. **Text search (v1):** case-insensitive `LIKE` on `name`, `brand`, `description`, combined with category filter.
7. **Admin writes** that change `image_path` must call the engine's update-vector function (A3);
   deletes must call remove-vector.
8. `created_at`/`updated_at`: set by the application, not by DB defaults (portability).