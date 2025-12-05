from fastapi import APIRouter, HTTPException
from app.models import SearchRequest, SearchResponse, SearchResult
from app.services.html_fetcher import HTMLFetcher
from app.services.text_processor import TextProcessor
from app.services.embeddings import EmbeddingService
from app.services.vector_db import VectorDBService
from app.config import settings

router = APIRouter()

html_fetcher = HTMLFetcher()
text_processor = TextProcessor()
embedding_service = EmbeddingService()
vector_db = VectorDBService()

@router.post("/search", response_model=SearchResponse)
async def search_website(request: SearchRequest):

    try:
        soup, path = html_fetcher.fetch_and_parse(request.url)
        
        text_blocks = html_fetcher.extract_text_with_structure(soup)
        
        if not text_blocks:
            raise HTTPException(status_code=400, detail="No content found on the webpage")
        
        chunks = text_processor.chunk_text(text_blocks)
        
        if not chunks:
            raise HTTPException(status_code=400, detail="Failed to create chunks from content")
        
        indexed_chunks = text_processor.prepare_chunks_for_indexing(chunks, request.url, path)
        
        chunk_texts = [chunk['text'] for chunk in indexed_chunks]
        embeddings = embedding_service.generate_embeddings_batch(chunk_texts)
        
        vector_db.upsert_chunks(indexed_chunks, embeddings)
        
        query_embedding = embedding_service.generate_embedding(request.query)
        
        search_results = vector_db.search(
            query_embedding=query_embedding,
            top_k=settings.TOP_K_RESULTS,
            filter_dict={'url': request.url}  
        )
        
        formatted_results = []
        for result in search_results:
            metadata = result['metadata']
            formatted_results.append(
                SearchResult(
                    content=metadata['text'],
                    score=result['score'],
                    path=metadata['path'],
                    token_count=metadata['token_count'],
                    html_preview=metadata.get('html_preview', '')
                )
            )
        
        return SearchResponse(
            results=formatted_results,
            total_chunks=len(indexed_chunks),
            query=request.query,
            url=request.url
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@router.get("/health")
async def health_check():

    try:
        if not vector_db._initialized:
            return {
                "status": "not_initialized",
                "message": "Vector DB not yet initialized. Make a search request first."
            }
        
        stats = vector_db.get_stats()
        
        total_count = 0
        namespace_info = {}
        
        if hasattr(stats, 'total_vector_count'):
            total_count = stats.total_vector_count
        elif isinstance(stats, dict):
            total_count = stats.get('total_vector_count', 0)
            
        if hasattr(stats, 'namespaces'):
            namespaces = stats.namespaces
            if isinstance(namespaces, dict):
                namespace_info = {k: v.get('vector_count', 0) if isinstance(v, dict) else str(v) 
                                 for k, v in namespaces.items()}
        elif isinstance(stats, dict) and 'namespaces' in stats:
            namespaces = stats['namespaces']
            if isinstance(namespaces, dict):
                namespace_info = {k: v.get('vector_count', 0) if isinstance(v, dict) else str(v) 
                                 for k, v in namespaces.items()}
        
        return {
            "status": "healthy",
            "vector_db_connected": True,
            "index_name": vector_db.index_name,
            "total_vectors": total_count,
            "namespaces": namespace_info
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }