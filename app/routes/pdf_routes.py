"""PDF Upload Routes - Enhanced Error Logging"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.models.schemas import PDFUploadResponse
from app.services.pdf_processor import PDFProcessor
from app.services.embeddings_service import EmbeddingsService
from app.services.vector_store import VectorStoreService
from app.config.settings import settings
import os
import uuid
import traceback
import sys

router = APIRouter()

@router.post("/upload", response_model=PDFUploadResponse)
async def upload_pdf(file: UploadFile = File(...)):
    try:
        print(f"\n{'='*60}", file=sys.stderr)
        print(f"📤 UPLOAD REQUEST STARTED", file=sys.stderr)
        print(f"{'='*60}", file=sys.stderr)
        print(f"Filename: {file.filename}", file=sys.stderr)
        print(f"Content Type: {file.content_type}", file=sys.stderr)
        
        # Step 1: Validate API keys
        print("\n🔑 Step 1: Checking API keys...", file=sys.stderr)
        if not settings.GOOGLE_API_KEY:
            raise HTTPException(status_code=400, detail="Google API key missing")
        if not settings.PINECONE_API_KEY:
            raise HTTPException(status_code=400, detail="Pinecone API key missing")
        if not settings.GROQ_API_KEY:
            raise HTTPException(status_code=400, detail="Groq API key missing")
        print("✅ All API keys present", file=sys.stderr)
        
        # Step 2: Validate file
        print("\n📄 Step 2: Validating file...", file=sys.stderr)
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files allowed")
        
        contents = await file.read()
        file_size = len(contents)
        print(f"File size: {file_size} bytes ({file_size / 1024 / 1024:.2f} MB)", file=sys.stderr)
        
        if file_size > settings.MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail=f"File too large (max 20MB)")
        if file_size == 0:
            raise HTTPException(status_code=400, detail="File is empty")
        print("✅ File validation passed", file=sys.stderr)
        
        # Step 3: Save file
        print("\n💾 Step 3: Saving file...", file=sys.stderr)
        document_id = str(uuid.uuid4())
        file_path = os.path.join(settings.UPLOAD_DIR, f"{document_id}.pdf")
        print(f"Save path: {file_path}", file=sys.stderr)
        
        with open(file_path, 'wb') as f:
            f.write(contents)
        print(f"✅ File saved successfully", file=sys.stderr)
        
        # Step 4: Extract text
        print("\n📖 Step 4: Extracting text from PDF...", file=sys.stderr)
        try:
            pdf_processor = PDFProcessor()
            chunks = pdf_processor.process_pdf(file_path)
            print(f"✅ Extracted {len(chunks)} chunks", file=sys.stderr)
        except Exception as e:
            print(f"❌ PDF extraction failed: {str(e)}", file=sys.stderr)
            raise
        
        if len(chunks) == 0:
            raise HTTPException(status_code=400, detail="No text found in PDF")
        
        # Step 5: Generate embeddings
        print("\n🧠 Step 5: Generating embeddings...", file=sys.stderr)
        try:
            embeddings_service = EmbeddingsService()
            chunk_texts = [chunk["content"] for chunk in chunks]
            print(f"Generating embeddings for {len(chunk_texts)} chunks...", file=sys.stderr)
            embeddings = embeddings_service.generate_embeddings_batch(chunk_texts)
            print(f"✅ Generated {len(embeddings)} embeddings", file=sys.stderr)
        except Exception as e:
            print(f"❌ Embedding generation failed: {str(e)}", file=sys.stderr)
            print(f"Full error: {traceback.format_exc()}", file=sys.stderr)
            raise
        
        # Step 6: Store in Pinecone
        print("\n🗄️  Step 6: Storing in Pinecone...", file=sys.stderr)
        try:
            vector_store = VectorStoreService()
            num_stored = vector_store.store_embeddings(embeddings, chunks, document_id)
            print(f"✅ Stored {num_stored} vectors", file=sys.stderr)
        except Exception as e:
            print(f"❌ Pinecone storage failed: {str(e)}", file=sys.stderr)
            print(f"Full error: {traceback.format_exc()}", file=sys.stderr)
            raise
        
        print(f"\n{'='*60}", file=sys.stderr)
        print(f"✅ UPLOAD COMPLETED SUCCESSFULLY", file=sys.stderr)
        print(f"{'='*60}\n", file=sys.stderr)
        
        return PDFUploadResponse(
            success=True,
            message="PDF processed successfully!",
            document_id=document_id,
            filename=file.filename,
            chunks_processed=num_stored
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"\n{'='*60}", file=sys.stderr)
        print(f"❌ FATAL ERROR", file=sys.stderr)
        print(f"{'='*60}", file=sys.stderr)
        print(f"Error: {str(e)}", file=sys.stderr)
        print(f"\nFull Traceback:", file=sys.stderr)
        print(traceback.format_exc(), file=sys.stderr)
        print(f"{'='*60}\n", file=sys.stderr)
        raise HTTPException(status_code=500, detail=str(e))