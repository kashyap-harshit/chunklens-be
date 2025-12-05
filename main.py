from fastapi import FastAPI
from models.request_models import ParseRequest
from utils.fetch_html import fetch_html
from utils.parse_clean import parse_and_clean
from utils.tokenizer import tokenize_text
from utils.chunker import chunk_tokens


app = FastAPI()


@app.post("/parse")
async def parse_website(data: ParseRequest):
    html = fetch_html(data.url)
    cleaned_text = parse_and_clean(html)
    tokens = tokenize_text(cleaned_text)
    chunks = chunk_tokens(tokens, max_tokens=500)

    chunk_texts = ["".join(chunk) for chunk in chunks]

    return {"url": data.url, "total_chucnks": len(chunk_texts), "chunks": chunk_texts}
