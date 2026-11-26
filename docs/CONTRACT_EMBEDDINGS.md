# CONTRACT — Embeddings & SearchEngine (A1)

Status: DRAFT — à valider avec Oussama au kickoff (M0).

## 1. Format des fichiers (dossier `EMBEDDINGS_DIR`, par défaut `data/embeddings/`)

| Fichier | Contenu | Type |
|---------|---------|------|
| `ids.npy` | ids des produits (`products.id`), forme `(N,)` | int64 |
| `<model>.npy` | vecteurs, forme `(N, D)` | float32 |

- `<model>` ∈ `mobilenet_v2` (D=1280), `dinov2_small` (D=384).
- **Ligne i de `<model>.npy` = produit `ids[i]`** (alignement obligatoire, testé).
- Les vecteurs sont **normalisés L2** (norme = 1) → le produit scalaire = similarité cosinus.
- Même prétraitement pour le catalogue et pour les requêtes.
- Un fichier d'index FAISS (`<model>.faiss`) peut être reconstruit à partir des `.npy`.

## 2. Interface `SearchEngine` (`core/engine.py`)

| Méthode | Rôle |
|---------|------|
| `search(image_bytes, top_k=20, model="mobilenet_v2", candidate_ids=None)` | Renvoie un `SearchOutput` |
| `add_or_update(product_id, image_bytes)` | Calcule/met à jour le vecteur d'un produit |
| `remove(product_id)` | Supprime le vecteur |
| `size()` | Nombre de produits indexés |

`SearchOutput` : `hits` (liste de `Hit(id, score)` triée du plus au moins similaire),
`no_relevant_result` (bool), `threshold` (float), `model` (str).

## 3. Règles

1. Le moteur renvoie **seulement `(id, score)`** ; l'API joint avec la base SQLite.
2. `score` = similarité cosinus entre 0 et 1.
3. Si le meilleur score < seuil : `no_relevant_result = True` et `hits = []`.
4. Le **filtre texte/catégorie/prix** est fait par l'API (SQL) ; elle passe les ids restants dans `candidate_ids`.
5. `size() == 0` => l'API répond 503 `catalog_empty`.
6. Image invalide : l'API valide **avant** d'appeler le moteur ; le moteur peut lever `ValueError`.
7. Modèle inconnu => `ValueError`.
8. Le vrai moteur (A3) et le Stub (`core/stub_engine.py`) ont **exactement la même interface**.