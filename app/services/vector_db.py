from pinecone import Pinecone, ServerlessSpec
from typing import List, Dict
from app.config import settings
import time


class VectorDBService:
    def __init__(self):
        self.pc = None
        self.index_name = settings.PINECONE_INDEX_NAME
        self.index = None
        self._initialized = False

    def _initialize_index(self):

        if self._initialized:
            return

        try:
            print("Connecting to Pinecone...")
            self.pc = Pinecone(api_key=settings.PINECONE_API_KEY)

            self.index = self.pc.Index(self.index_name)
            self._initialized = True
            print(f"Connected to Pinecone index: {self.index_name}")

        except Exception as e:
            print(f"Error connecting to Pinecone: {str(e)}")
            raise Exception(f"Error initializing Pinecone index: {str(e)}")

    def upsert_chunks(self, chunks: List[Dict], embeddings: List[List[float]]):
        if not self._initialized:
            self._initialize_index()

        vectors = []
        for chunk, embedding in zip(chunks, embeddings):
            vector = {
                "id": chunk["id"],
                "values": embedding,
                "metadata": {
                    "text": chunk["text"][:1000],
                    "html_preview": chunk["html_preview"],
                    "token_count": chunk["token_count"],
                    "url": chunk["url"],
                    "path": chunk["path"],
                    "chunk_index": chunk["chunk_index"],
                },
            }
            vectors.append(vector)

        batch_size = 100
        for i in range(0, len(vectors), batch_size):
            batch = vectors[i : i + batch_size]
            self.index.upsert(vectors=batch)
            print(f"Upserted batch {i//batch_size + 1} ({len(batch)} vectors)")

    def search(
        self, query_embedding: List[float], top_k: int = 10, filter_dict: Dict = None
    ) -> List[Dict]:

        if not self._initialized:
            self._initialize_index()

        results = self.index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True,
            filter=filter_dict,
        )

        search_results = []
        for match in results["matches"]:
            search_results.append(
                {
                    "id": match["id"],
                    "score": match["score"],
                    "metadata": match["metadata"],
                }
            )

        return search_results

    def delete_by_url(self, url: str):

        if not self._initialized:
            self._initialize_index()

        try:
            self.index.delete(filter={"url": url})
        except Exception as e:
            print(f"Could not delete by URL: {str(e)}")

    def get_stats(self):

        if not self._initialized:
            self._initialize_index()

        return self.index.describe_index_stats()
