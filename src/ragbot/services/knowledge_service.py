from pathlib import Path


def ensure_storage(docs_dir: Path, notes_file: Path) -> None:
    docs_dir.mkdir(parents=True, exist_ok=True)
    notes_file.touch(exist_ok=True)


def read_multiline() -> str:
    print("Paste/type your knowledge. Type END on a new line.")
    lines: list[str] = []
    while True:
        line = input()
        if line.strip() == "END":
            return "\n".join(lines).strip()
        lines.append(line)


def append_manual_knowledge(notes_file: Path, text: str, source: str = "manual") -> None:
    clean = text.strip()
    if not clean:
        raise ValueError("Knowledge text is empty.")
    with notes_file.open("a", encoding="utf-8") as f:
        f.write(f"Source: {source}\n{clean}\n\n")
