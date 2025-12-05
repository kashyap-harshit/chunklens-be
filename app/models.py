from pydantic import BaseModel, HttpUrl
from typing import List, Optional

class SearchRequest(BaseModel):
    url: str
    query: str

class SearchResult(BaseModel):
    content: str
    score: float
    path: str
    token_count: int
    html_preview: Optional[str] = None

class SearchResponse(BaseModel):
    results: List[SearchResult]
    total_chunks: int
    query: str
    url: str