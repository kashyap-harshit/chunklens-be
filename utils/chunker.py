def chunk_tokens(tokens, max_tokens=500):
    chunks = []
    for i in range(0, len(tokens), max_tokens):
        chunks.append(tokens[i:i + max_tokens])
    return chunks