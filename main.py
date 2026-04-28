from src.ragbot.chatbot import run_chat
from src.ragbot.config import DOCS_DIR, TOP_K
from src.ragbot.services.knowledge_service import ensure_storage


def main() -> None:
    ensure_storage(DOCS_DIR)
    run_chat(docs_dir=DOCS_DIR, top_k=TOP_K)


if __name__ == "__main__":
    main()
