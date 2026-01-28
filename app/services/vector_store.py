"""Vector Store Service"""
from pinecone import Pinecone, ServerlessSpec
from typing import List, Dict
from app.config.settings import settings

class VectorStoreService:
    def __init__(self):
        self.pc = Pinecone(api_key=settings.PINECONE_API_KEY)
        self.index_name = settings.PINECONE_INDEX_NAME
        self._initialize_index()
    
    def _initialize_index(self):
        try:
            if self.index_name not in self.pc.list_indexes().names():
                self.pc.create_index(
                    name=self.index_name,
                    dimension=768,
                    metric='cosine',
                    spec=ServerlessSpec(cloud='aws', region='us-east-1')
                )
            self.index = self.pc.Index(self.index_name)
        except Exception as e:
            raise Exception(f"Pinecone init error: {str(e)}")
    
    def store_embeddings(self, embeddings: List[List[float]], chunks: List[Dict], document_id: str):
        try:
            vectors = []
            for idx, (embedding, chunk) in enumerate(zip(embeddings, chunks)):
                vector_id = f"{document_id}_{idx}"
                vectors.append({
                    "id": vector_id,
                    "values": embedding,
                    "metadata": {
                        "content": chunk["content"],
                        "chunk_id": chunk["chunk_id"],
                        "document_id": document_id
                    }
                })
            
            batch_size = 100
            for i in range(0, len(vectors), batch_size):
                batch = vectors[i:i + batch_size]
                self.index.upsert(vectors=batch)
            
            return len(vectors)
        except Exception as e:
            raise Exception(f"Storage error: {str(e)}")
    
    def search(self, query_embedding: List[float], top_k: int = None, document_id: str = None):
        try:
            if top_k is None:
                top_k = settings.TOP_K_RESULTS
            
            filter_dict = None
            if document_id:
                filter_dict = {"document_id": {"$eq": document_id}}
            
            results = self.index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True,
                filter=filter_dict
            )
            return results.matches
        except Exception as e:
            raise Exception(f"Search error: {str(e)}")