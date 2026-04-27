import subprocess
import time
import ollama

from ..config import EMBED_MODEL, OLLAMA_KEEP_ALIVE, OLLAMA_MODEL


def _can_connect() -> bool:
    try:
        ollama.list()
        return True
    except Exception:
        return False


def _start_server() -> None:
    creationflags = 0
    if hasattr(subprocess, "DETACHED_PROCESS"):
        creationflags |= subprocess.DETACHED_PROCESS
    if hasattr(subprocess, "CREATE_NEW_PROCESS_GROUP"):
        creationflags |= subprocess.CREATE_NEW_PROCESS_GROUP

    subprocess.Popen(  # noqa: S603
        ["ollama", "serve"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL,
        creationflags=creationflags,
    )


def ensure_ready() -> None:
    if _can_connect():
        return

    _start_server()
    for _ in range(20):
        if _can_connect():
            return
        time.sleep(0.5)
    raise RuntimeError("Ollama is not reachable. Please ensure Ollama is installed and in PATH.")


def ensure_model(model: str) -> None:
    models = ollama.list().get("models", [])
    names = {m.get("model", "") for m in models}
    names |= {m.get("name", "") for m in models}
    names |= {name.split(":")[0] for name in names if name}
    if model in names:
        return
    print(f"Pulling Ollama model: {model} (first time only)")
    subprocess.run(["ollama", "pull", model], check=True)  # noqa: S603


def ensure_required_models() -> None:
    ensure_model(OLLAMA_MODEL)
    ensure_model(EMBED_MODEL)


def generate(prompt: str) -> str:
    response = ollama.chat(
        model=OLLAMA_MODEL,
        messages=[{"role": "user", "content": prompt}],
        keep_alive=OLLAMA_KEEP_ALIVE,
    )
    answer = response["message"]["content"].strip()
    if not answer:
        raise RuntimeError("Ollama returned an empty response.")
    return answer


def embed(text: str) -> list[float]:
    data = ollama.embed(model=EMBED_MODEL, input=text, keep_alive=OLLAMA_KEEP_ALIVE)
    embeddings = data.get("embeddings", [])
    if not embeddings:
        raise RuntimeError("Ollama embedding response is empty.")
    return embeddings[0]
