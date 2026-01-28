"""PDF Processing Service"""
from typing import List, Dict
import PyPDF2
from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.config.settings import settings

class PDFProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
    
    def extract_text_from_pdf(self, file_path: str) -> str:
        try:
            text = ""
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n"
            return text
        except Exception as e:
            raise Exception(f"Error extracting PDF: {str(e)}")
    
    def chunk_text(self, text: str) -> List[str]:
        return self.text_splitter.split_text(text)
    
    def process_pdf(self, file_path: str) -> List[Dict[str, str]]:
        text = self.extract_text_from_pdf(file_path)
        chunks = self.chunk_text(text)
        
        processed_chunks = []
        for idx, chunk in enumerate(chunks):
            processed_chunks.append({
                "content": chunk,
                "chunk_id": idx,
                "source": file_path
            })
        return processed_chunks