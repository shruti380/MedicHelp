"""MedicHelper - AI-Powered Medical Knowledge Assistant"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
import uvicorn
import os

from app.routes import pdf_routes, chat_routes
from app.config.settings import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting MedicHelper...")
    print(f"📊 Environment: {settings.ENVIRONMENT}")
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    os.makedirs("static", exist_ok=True)
    yield
    print("👋 Shutting down...")

app = FastAPI(
    title="MedicHelper API",
    description="AI Medical Assistant",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(pdf_routes.router, prefix="/api/v1/pdf", tags=["PDF"])
app.include_router(chat_routes.router, prefix="/api/v1/chat", tags=["Chat"])

@app.get("/")
async def root():
    return FileResponse("static/index.html")

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "message": "MedicHelper is running"
    }

@app.get("/config-check")
async def config_check():
    """Debug endpoint to check configuration"""
    google_set = bool(settings.GOOGLE_API_KEY and len(settings.GOOGLE_API_KEY) > 10)
    pinecone_set = bool(settings.PINECONE_API_KEY and len(settings.PINECONE_API_KEY) > 10)
    groq_set = bool(settings.GROQ_API_KEY and len(settings.GROQ_API_KEY) > 10)
    
    return {
        "status": "Configuration Check",
        "google_api_key": "✅ Configured" if google_set else "❌ NOT SET",
        "pinecone_api_key": "✅ Configured" if pinecone_set else "❌ NOT SET",
        "groq_api_key": "✅ Configured" if groq_set else "❌ NOT SET",
        "pinecone_index": settings.PINECONE_INDEX_NAME,
        "upload_dir": settings.UPLOAD_DIR,
        "help": {
            "google": "Get key from https://makersuite.google.com/app/apikey",
            "pinecone": "Get key from https://app.pinecone.io",
            "groq": "Get key from https://console.groq.com"
        }
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.PORT,
        reload=True
    )