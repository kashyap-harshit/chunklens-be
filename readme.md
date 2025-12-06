# ChunkLens Backend 🔍

A FastAPI-based semantic search engine that fetches, chunks, and searches website content using vector embeddings and Pinecone.

## 🚀 Features

- **Smart Web Scraping**: Fetches and cleans HTML content from any URL
- **Intelligent Chunking**: Splits content into 500-token chunks for optimal processing
- **Semantic Search**: Uses AI embeddings (BAAI/bge-large-en-v1.5) for meaning-based search
- **Vector Database**: Leverages Pinecone for lightning-fast similarity search
- **Top 10 Results**: Returns the most relevant content chunks ranked by similarity score

## 🛠️ Tech Stack

- **FastAPI**: Modern, fast web framework
- **Pinecone**: Cloud vector database
- **Sentence Transformers**: State-of-the-art text embeddings
- **BeautifulSoup**: HTML parsing and cleaning
- **Tiktoken**: Token counting and management

## 📦 Installation

### Prerequisites

- Python 3.11.3
- Pinecone account (free tier works)

### Setup

1. **Clone the repository**

```bash
git clone <your-repo-url>
cd chunklens-be
```

2. **Create virtual environment**

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure environment variables**

Create a `.env` file in the root directory:

```env
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENVIRONMENT=us-east-1
PINECONE_INDEX_NAME=chunklens-db
MAX_TOKENS_PER_CHUNK=500
TOP_K_RESULTS=10
```

5. **Run the server**

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## 🎯 API Endpoints

### Search Website

```http
POST /api/search
Content-Type: application/json

{
  "url": "https://example.com",
  "query": "artificial intelligence"
}
```

**Response:**

```json
{
  "results": [
    {
      "content": "Text content of matching chunk...",
      "score": 0.89,
      "path": "/about",
      "token_count": 450,
      "html_preview": "<div>..."
    }
  ],
  "total_chunks": 25,
  "query": "artificial intelligence",
  "url": "https://example.com"
}
```

### Health Check

```http
GET /api/health
```

## 📁 Project Structure

```
chunklens-be/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration settings
│   ├── models.py            # Pydantic models
│   ├── services/
│   │   ├── html_fetcher.py  # Web scraping
│   │   ├── text_processor.py # Chunking logic
│   │   ├── embeddings.py    # Vector embeddings
│   │   └── vector_db.py     # Pinecone integration
│   └── routes/
│       └── search.py        # API endpoints
├── requirements.txt
├── Procfile                 # Deployment config
├── .env                     # Environment variables
└── README.md
```

## 🧠 How It Works

1. **Fetch**: Downloads HTML from the provided URL
2. **Clean**: Removes scripts, styles, and non-content elements
3. **Chunk**: Splits text into 500-token segments
4. **Embed**: Converts chunks to 1024-dimensional vectors
5. **Store**: Saves vectors to Pinecone with metadata
6. **Search**: Finds semantically similar chunks to the query
7. **Rank**: Returns top 10 results by similarity score

## 🔍 Example Usage

```python
import requests

response = requests.post(
    "http://localhost:8000/api/search",
    json={
        "url": "https://smarter.codes",
        "query": "AI automation"
    }
)

results = response.json()
for result in results['results'][:3]:
    print(f"Score: {result['score']}")
    print(f"Content: {result['content'][:100]}...")
    print("---")
```

## 🐛 Troubleshooting

### Pinecone Connection Issues

- Verify API key and environment in `.env`
- Check index exists in Pinecone dashboard
- Ensure index dimension matches model (1024)

### Model Download

- First run downloads ~1.3GB model
- Requires stable internet connection
- Model cached locally after first download

### Port Already in Use

```bash
# Change port
uvicorn app.main:app --port 8001
```

## 📝 Environment Variables

| Variable               | Description           | Default        |
| ---------------------- | --------------------- | -------------- |
| `PINECONE_API_KEY`     | Your Pinecone API key | Required       |
| `PINECONE_ENVIRONMENT` | Pinecone region       | `us-east-1`    |
| `PINECONE_INDEX_NAME`  | Name of your index    | `chunklens-db` |
| `MAX_TOKENS_PER_CHUNK` | Max tokens per chunk  | `500`          |
| `TOP_K_RESULTS`        | Number of results     | `10`           |

## 🔗 Links

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pinecone Documentation](https://docs.pinecone.io/)
- [Sentence Transformers](https://www.sbert.net/)

---
