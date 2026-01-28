# MedicHelper - AI-Powered Medical Knowledge Assistant

AI-powered RAG-based chatbot for medical knowledge queries with PDF upload capabilities.

 **Live Demo**: [https://medichelp-70z9.onrender.com](https://medichelp-70z9.onrender.com)

## Features

-  PDF upload and processing
-  Semantic search using vector embeddings
-  Context-aware chat responses
-  Source citation and retrieval
-  Fast API with async support

## Tech Stack

- **Backend**: FastAPI
- **LLM**: Groq (LLaMA3-70B)
- **Embeddings**: Google Generative AI
- **Vector DB**: Pinecone
- **PDF Processing**: PyPDF2
- **Framework**: LangChain

## Setup Instructions

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/medichelper.git
cd medichelper
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**

Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_groq_api_key
GOOGLE_API_KEY=your_google_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENVIRONMENT=your_pinecone_environment
```

4. **Run the application**
```bash
uvicorn main:app --reload
```

5. **Access the application**
- Open your browser and navigate to `http://localhost:8000`

## API Endpoints

### Upload PDF
```bash
POST /upload-pdf
Content-Type: multipart/form-data

Upload a medical PDF document (max 20MB)
```

**Response:**
```json
{
  "message": "PDF processed successfully",
  "filename": "medical_report.pdf",
  "status": "success"
}
```

## How It Works

1. **Upload**: User uploads a PDF medical document
2. **Extract**: Text is extracted from the PDF
3. **Chunk**: Document is split into manageable chunks
4. **Embed**: Chunks are converted to vector embeddings
5. **Store**: Embeddings are stored in Pinecone vector database
6. **Query**: User asks a question
7. **Retrieve**: Relevant chunks are retrieved using semantic search
8. **Generate**: LLM generates an answer using the retrieved context

## Deployment

The application is deployed on Render and accessible at:
**https://medichelp-70z9.onrender.com**

## Project Structure

```
medichelper/
├── app/
│   ├── routes/
│   ├── services/
│   └── config/
├── static/
├── uploads/
├── main.py
├── requirements.txt
└── README.md
```


## Developed By - SHRUTI GUPTA 
## Contact

For questions or support, please open an issue on GitHub.
