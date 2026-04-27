# Simple RAG (Python)

This is a minimal Retrieval-Augmented Generation (RAG) chatbot using your requested Ollama pattern:
- `ollama.embed(...)` to build embeddings
- in-memory vector database (list of `(source, chunk, embedding)`)
- cosine similarity retrieval
- `ollama.chat(...)` for strict context-grounded answers

1. Load text documents from `docs/`
2. Split into chunks (by paragraph)
3. Build in-memory vector DB from embeddings
4. Retrieve semantically similar chunks with cosine similarity
5. Generate grounded answer with Ollama

## Setup

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
ollama pull llama3.2
ollama pull nomic-embed-text
```

Models are hardcoded in `rag.py`:
- generation: `llama3.2`
- embeddings: `nomic-embed-text`

You do not need to run `ollama serve` manually; `rag.py` auto-starts Ollama when needed.

## Project structure

```text
RAG/
  main.py
  rag.py
  src/ragbot/
    config.py
    chatbot.py
    services/
      knowledge_service.py
      ollama_service.py
      retrieval_service.py
```

- `main.py`: entrypoint that wires everything
- `src/ragbot/services`: separated logic (Ollama, retrieval, knowledge)
- `src/ragbot/chatbot.py`: chat flow
- `rag.py`: compatibility runner (calls `main.py`)

## Run chatbot

```bash
python main.py
```

This starts chatbot mode directly. No command-line arguments needed.
Inside chat:
- Type your question normally.
- Type `/add` to add knowledge text (finish with `END` on a new line).
- Type `/exit` to quit.

## Optional file-based data

- Put `.txt` files inside `docs/`
- Keep paragraphs separated by blank lines for better chunking
