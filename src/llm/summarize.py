import logging
from .model import make_prompt
from src.utils.files import open_pdf, get_text
from rich.panel import Panel
from rich.markdown import Markdown
from rich.console import Console

console = Console()
logger = logging.getLogger(__name__)

def summarize(pdf_path: str) -> str:
    """Produz e retorna o resumo feito pela LLM."""
    logger.debug(f"Resumindo o PDF: {pdf_path}")
    doc = open_pdf(pdf_path)
    text = get_text(doc)

    chain = make_prompt()
    summa = chain.invoke({"text": text})
    summa = summa.strip()

    print(summa)
    print_summary(summa)
    
    return summa

def print_summary(summary: str):
    """Imprime o resumo no console."""
    logger.debug("Imprimindo o resumo gerado pela LLM.")
    
    md = Markdown(summary)
    console.print(Panel(
        md,
        title="[bold yellow]Resumo do PDF[/]",
        border_style="green",
        padding=(1, 2)
    ))