import fitz
from .model import make_prompt
from src.utils.files import open_pdf, get_text

def summarize(pdf_path: str) -> str:
    """Produz e retorna o resumo feito pela LLM."""
    doc = open_pdf(pdf_path)
    text = get_text(doc)

    chain = make_prompt()
    summa = chain.invoke({"text": text})
    summa = summa.strip()

    print(summa)

    return summa