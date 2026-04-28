from pathlib import Path

from .services.ollama_service import ensure_ready, ensure_required_models, generate
from .services.retrieval_service import retrieve_context


def answer_question(docs_dir: Path, query: str, top_k: int) -> str:
    ensure_ready()
    ensure_required_models()

    context = retrieve_context(docs_dir, query, top_k)
    if not context:
        return "I could not find relevant context in the knowledge base."

    prompt = (
        "You are a RAG assistant. Answer using ONLY the retrieved context.\n"
        "If the answer is not in the context, say you do not know.\n\n"
        f"Question:\n{query}\n\nRetrieved context:\n{context}\n\nAnswer:"
    )
    return generate(prompt)


def run_chat(docs_dir: Path, top_k: int) -> None:
    print("RAG chat ready.")
    print("Type /exit to quit.")

    while True:
        query = input("> ").strip()
        if query.lower() in {"/exit", "exit", "quit"}:
            print("Goodbye.")
            break

        if not query:
            continue

        try:
            print(answer_question(docs_dir, query, top_k))
            print()
        except (ValueError, RuntimeError) as exc:
            print(exc)
            print()
