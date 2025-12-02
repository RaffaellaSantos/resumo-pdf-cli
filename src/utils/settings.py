import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent

def clear() -> None:
    os.system("cls" if os.name == "nt" else "clear")
    return