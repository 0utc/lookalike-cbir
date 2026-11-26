from dataclasses import dataclass
from typing import Optional, Protocol

MODELS = ("mobilenet_v2", "dinov2_small")


@dataclass
class Hit:
    id: int
    score: float


@dataclass
class SearchOutput:
    hits: list
    no_relevant_result: bool
    threshold: float
    model: str


class SearchEngine(Protocol):
    def search(self, image_bytes: bytes, top_k: int = 20, model: str = "mobilenet_v2",
               candidate_ids: Optional[list] = None) -> SearchOutput:
        """Classe les produits par similarité avec l'image requête."""

    def add_or_update(self, product_id: int, image_bytes: bytes) -> None:
        """Calcule et enregistre le vecteur d'un produit."""

    def remove(self, product_id: int) -> None:
        """Supprime le vecteur d'un produit."""

    def size(self) -> int:
        """Nombre de produits indexés (0 = catalogue vide)."""