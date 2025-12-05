from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np
from app.config import settings


class EmbeddingService:
    def __init__(self):
        self.model = SentenceTransformer(settings.EMBEDDING_MODEL)

    def generate_embedding(self, text: str) -> List[float]:

        embedding = self.model.encode(text, convert_to_tensor=False)
        return embedding.tolist()

    def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        embeddings = self.model.encode(
            texts, convert_to_tensor=False, show_progress_bar=True
        )
        return [embedding.tolist() for embedding in embeddings]

    def get_dimension(self) -> int:

        return self.model.get_sentence_embedding_dimension()
