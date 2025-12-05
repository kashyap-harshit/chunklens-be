import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PINECONE_API_KEY: str = os.getenv("PINECONE_API_KEY", "")
    PINECONE_ENVIRONMENT: str = os.getenv("PINECONE_ENVIRONMENT", "")
    PINECONE_INDEX_NAME: str = os.getenv("PINECONE_INDEX_NAME", "website-search-index")
    MAX_TOKENS_PER_CHUNK: int = int(os.getenv("MAX_TOKENS_PER_CHUNK", "500"))
    TOP_K_RESULTS: int = int(os.getenv("TOP_K_RESULTS", "10"))
    EMBEDDING_MODEL: str = "BAAI/bge-large-en-v1.5" 
    DIMENSION: int = 1024  

settings = Settings()