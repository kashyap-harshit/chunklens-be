import tiktoken
from typing import List, Dict
from app.config import settings


class TextProcessor:
    def __init__(self):
        self.encoding = tiktoken.get_encoding("cl100k_base")
        self.max_tokens = settings.MAX_TOKENS_PER_CHUNK

    def count_tokens(self, text: str) -> int:
        return len(self.encoding.encode(text))

    def chunk_text(self, text_blocks: List[Dict]) -> List[Dict]:

        chunks = []
        current_chunk = {"text": "", "html_preview": "", "token_count": 0}

        for block in text_blocks:
            text = block["text"]
            html_preview = block.get("html_preview", "")

            token_count = self.count_tokens(text)

            if token_count > self.max_tokens:
                sentences = text.split(". ")
                for sentence in sentences:
                    sentence = sentence.strip()
                    if not sentence:
                        continue

                    sentence_tokens = self.count_tokens(sentence)

                    if current_chunk["token_count"] + sentence_tokens > self.max_tokens:
                        if current_chunk["text"]:
                            chunks.append(current_chunk.copy())
                        current_chunk = {
                            "text": sentence + ". ",
                            "html_preview": html_preview[:200],
                            "token_count": sentence_tokens,
                        }
                    else:
                        current_chunk["text"] += sentence + ". "
                        current_chunk["token_count"] += sentence_tokens
                        if not current_chunk["html_preview"]:
                            current_chunk["html_preview"] = html_preview[:200]
            else:
                if current_chunk["token_count"] + token_count > self.max_tokens:
                    if current_chunk["text"]:
                        chunks.append(current_chunk.copy())
                    current_chunk = {
                        "text": text,
                        "html_preview": html_preview[:200],
                        "token_count": token_count,
                    }
                else:
                    current_chunk["text"] += " " + text
                    current_chunk["token_count"] += token_count
                    if not current_chunk["html_preview"]:
                        current_chunk["html_preview"] = html_preview[:200]

        if current_chunk["text"]:
            chunks.append(current_chunk)

        return chunks

    def prepare_chunks_for_indexing(
        self, chunks: List[Dict], url: str, path: str
    ) -> List[Dict]:

        indexed_chunks = []
        for idx, chunk in enumerate(chunks):
            indexed_chunks.append(
                {
                    "id": f"{url}_{idx}",
                    "text": chunk["text"],
                    "html_preview": chunk["html_preview"],
                    "token_count": chunk["token_count"],
                    "url": url,
                    "path": path,
                    "chunk_index": idx,
                }
            )
        return indexed_chunks
