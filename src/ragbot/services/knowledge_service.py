from pathlib import Path


def ensure_storage(docs_dir: Path) -> None:
    docs_dir.mkdir(parents=True, exist_ok=True)
