import argparse
from pathlib import Path

def validate_str(value: str="") -> str:
    """Valida se a string existe."""
    clean_str = value.strip()

    if not clean_str:
        raise argparse.ArgumentTypeError("[Erro]: Argumento vazio.")
    
    return clean_str

def validate_path(value: str) -> Path:
    """Valiida se o caminho existe, se é um arquivo e se é um pdf."""
    path = Path(value)

    if not path.exists():
        raise argparse.ArgumentTypeError(f"[Erro]: o arquivo '{path}' não foi encontrado.")
    
    if not path.is_file():
        raise argparse.ArgumentTypeError(f"[Erro]: '{path}' é um diretório, esperava-se um arquivo.")
    
    if path.suffix.lower() != '.pdf':
        raise argparse.ArgumentTypeError(f"[Erro]: O arquivo precisa ser um PDF. Você forneceu '{path.suffix}'. ")
    
    return path