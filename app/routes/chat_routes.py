"""Chat Routes"""
from fastapi import APIRouter, HTTPException
from app.models.schemas import ChatRequest, ChatResponse, SourceChunk
from app.services.embeddings_service import EmbeddingsService
from app.services.vector_store import VectorStoreService
from app.services.llm_service import LLMService
import time

router = APIRouter()

@router.post("/query", response_model=ChatResponse)
async def chat_query(request: ChatRequest):
    try:
        start_time = time.time()
        
        embeddings_service = EmbeddingsService()
        query_embedding = embeddings_service.generate_query_embedding(request.query)
        
        vector_store = VectorStoreService()
        search_results = vector_store.search(
            query_embedding=query_embedding,
            document_id=request.document_id
        )
        
        if not search_results:
            raise HTTPException(status_code=404, detail="No information found")
        
        llm_service = LLMService()
        answer = llm_service.generate_response(request.query, search_results)
        
        sources = [
            SourceChunk(
                content=result.metadata['content'][:200] + "...",
                similarity_score=result.score
            )
            for result in search_results[:3]
        ]
        
        processing_time = time.time() - start_time
        
        return ChatResponse(
            success=True,
            query=request.query,
            answer=answer,
            sources=sources,
            processing_time=processing_time
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))