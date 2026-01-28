"""Pydantic models"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class PDFUploadResponse(BaseModel):
    success: bool
    message: str
    document_id: str
    filename: str
    chunks_processed: int

class ChatRequest(BaseModel):
    query: str = Field(..., min_length=1)
    document_id: Optional[str] = None

class SourceChunk(BaseModel):
    content: str
    similarity_score: float

class ChatResponse(BaseModel):
    success: bool
    query: str
    answer: str
    sources: List[SourceChunk] = []
    processing_time: float