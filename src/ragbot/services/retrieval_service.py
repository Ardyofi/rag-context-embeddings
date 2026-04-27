from pathlib import Path

from .ollama_service import embed

VECTOR_DB: list[tuple[str, str, list[float]]] = []


def _load_chunks(docs_dir: Path) -> list[tuple[str, str]]:
    chunks: list[tuple[str, str]] = []
    for file_path in sorted(docs_dir.glob("*.txt")):
        text = file_path.read_text(encoding="utf-8").strip()
        if not text:
            continue
        for part in text.split("\n\n"):
            part = part.strip()
            if part:
                chunks.append((file_path.name, part))
    return chunks


def _cosine_similarity(a: list[float], b: list[float]) -> float:
    dot_product = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(x * x for x in b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)


def _rebuild_vector_db(docs_dir: Path) -> None:
    chunks = _load_chunks(docs_dir)
    if not chunks:
        raise ValueError("No text found. Add knowledge with /add in chat.")
    VECTOR_DB.clear()
    for source, chunk in chunks:
        VECTOR_DB.append((source, chunk, embed(chunk)))


def retrieve_context(docs_dir: Path, query: str, top_k: int) -> str:
    _rebuild_vector_db(docs_dir)
    query_embedding = embed(query)
    similarities: list[tuple[str, str, float]] = []
    for source, chunk, chunk_embedding in VECTOR_DB:
        similarity = _cosine_similarity(query_embedding, chunk_embedding)
        similarities.append((source, chunk, similarity))
    similarities.sort(key=lambda item: item[2], reverse=True)

    lines = []
    for source, chunk, similarity in similarities[:top_k]:
        if similarity > 0:
            lines.append(f"[{source} | score={similarity:.3f}] {chunk}")
    return "\n".join(lines)
