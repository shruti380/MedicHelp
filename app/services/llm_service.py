"""LLM Service"""
from groq import Groq
from typing import List, Dict
from app.config.settings import settings

class LLMService:
    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = settings.MODEL_NAME
    
    def generate_response(self, query: str, context_chunks: List[Dict]) -> str:
        try:
            context = "\n\n".join([
                f"Source {idx + 1}:\n{chunk['metadata']['content']}"
                for idx, chunk in enumerate(context_chunks)
            ])
            
            prompt = f"""You are a medical AI assistant. Answer based ONLY on the context provided.

Context:
{context}

Question: {query}

Provide a clear, accurate answer. If the context doesn't contain the information, say so.

Answer:"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful medical assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=settings.TEMPERATURE,
                max_tokens=settings.MAX_TOKENS
            )
            
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"LLM error: {str(e)}")