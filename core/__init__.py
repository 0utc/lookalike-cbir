"""Package core: moteur de recherche visuelle (indépendant de FastAPI)."""
from core.engine import MODELS, Hit, SearchEngine, SearchOutput
from core.stub_engine import StubEngine

__all__ = ["MODELS", "Hit", "SearchEngine", "SearchOutput", "StubEngine"]