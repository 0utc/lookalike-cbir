import hashlib
import random
from typing import Optional

from core.engine import MODELS, Hit, SearchOutput


class StubEngine:
    def __init__(self, ids=None, threshold: float = 0.6):
        self.ids = set(ids if ids is not None else range(1, 501))
        self.threshold = threshold

    def search(self, image_bytes: bytes, top_k: int = 20, model: str = "mobilenet_v2",
               candidate_ids: Optional[list] = None) -> SearchOutput:
        if model not in MODELS:
            raise ValueError(f"Modèle inconnu: {model}")
        pool = self.ids if candidate_ids is None else self.ids & set(candidate_ids)
        rng = random.Random(int(hashlib.md5(image_bytes).hexdigest(), 16))
        hits = [Hit(i, round(rng.uniform(0.4, 0.95), 4)) for i in sorted(pool)]
        hits.sort(key=lambda h: h.score, reverse=True)
        hits = hits[:top_k]
        no_relevant = not hits or hits[0].score < self.threshold
        return SearchOutput([] if no_relevant else hits, no_relevant, self.threshold, model)

    def add_or_update(self, product_id: int, image_bytes: bytes) -> None:
        self.ids.add(product_id)

    def remove(self, product_id: int) -> None:
        self.ids.discard(product_id)

    def size(self) -> int:
        return len(self.ids)