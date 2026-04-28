from pathlib import Path

OLLAMA_MODEL = "phi3:mini"
EMBED_MODEL = "nomic-embed-text"
OLLAMA_KEEP_ALIVE = "24h"

DOCS_DIR = Path("docs")
USER_NOTES_FILE = DOCS_DIR / "user_notes.txt"
TOP_K = 3