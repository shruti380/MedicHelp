"""Embeddings Service (Google GenAI v1 – FINAL FIX)"""
from typing import List
from google import genai
from app.config.settings import settings

class EmbeddingsService:
    def __init__(self):
        self.client = genai.Client(api_key=settings.GOOGLE_API_KEY)
        self.model = "text-embedding-004"

    def generate_embedding(self, text: str) -> List[float]:
        try:
            response = self.client.models.embed_content(
                model=self.model,
                contents=text   # ✅ NOTE: contents (plural)
            )
            return response["embedding"]
        except Exception as e:
            raise Exception(f"Embedding error: {str(e)}")

    def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        return [self.generate_embedding(text) for text in texts]

    def generate_query_embedding(self, query: str) -> List[float]:
        try:
            response = self.client.models.embed_content(
                model=self.model,
                contents=query  # ✅ same here
            )
            return response["embedding"]
        except Exception as e:
            raise Exception(f"Query embedding error: {str(e)}")
