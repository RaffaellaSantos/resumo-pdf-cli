from typing import Dict
import fitz, os, logging
from rich.table import Table
from rich import box
from rich.console import Console
from src.utils.validator import abs_path

console = Console()
logger = logging.getLogger(__name__)

def open_pdf(pdf_path: str) -> fitz.Document:
    """Abre o PDF utilizando o pymupdf."""
    logger.debug(f"Abrindo o PDF: {pdf_path}")
    return fitz.open(pdf_path)

def get_text(doc: fitz.Document) -> str :
    """Extrai o texto que será resumido."""
    logger.debug("Extraindo texto do documento.")
    full_text = ""
    try:
        for page in doc:
            full_text += page.get_text() + "\n"
        return full_text
    except Exception as e:
        logger.error(f"Ocorreu um erro extraindo o texto do documento - {e}")   

def format_output(metadata: Dict) -> str:
    """Constroi a saída dos dados extraidos do pdf."""
    logger.debug("Formatando a saída dos metadados extraidos.")

    top_10, sections = console_print(metadata)

    markdown_output = (
        "## Dados Extraídos\n\n"
        "| Atributo | Valor |\n"
        "| :--- | :--- |\n"
        f"| **Número de Páginas** | {metadata['page_count']} |\n"
        f"| **Número de Palavras** | {metadata['num_words']} |\n"
        f"| **Vocabulário Único** | {metadata['num_voc']} |\n"
        f"| **Tamanho (KB)** | {metadata['size_kb']:.2f} |\n\n"
        
        "### Top 10 Palavras\n"
        f"{top_10}\n\n"
        
        "### Estrutura de Seções\n"
        f"{sections.replace('•', '-')}"
    )

    return markdown_output

def console_print(metadata: Dict):
    """Imprime no console os metadados extraidos do PDF."""

    logger.debug("Formatando a saída dos metadados extraidos.")
    
    table = Table(title="Metadados Extraídos do PDF", box=box.ROUNDED, show_header=True, header_style="bold magenta")

    table.add_column("Atributo", style="cyan", no_wrap=True)
    table.add_column("Valor", style="white")

    table.add_row("Número de Páginas", str(metadata['page_count']))
    table.add_row("Número de Palavras", str(metadata['num_words']))
    table.add_row("Número de Vocabulário", str(metadata['num_voc']))
    table.add_row("Tamanho (KB)", f"{metadata['size_kb']:.2f}")
    
    top_10 = ", ".join([f"{word} ({count})" for word, count in metadata['top_10']])
    table.add_row("Top 10 Palavras", top_10)

    sections = "\n".join([f"• {t}" for t in metadata['titles']])
    table.add_row("Seções", sections)

    console.print(table)

    return top_10, sections

def pixmap(pdf: str, xref: str, name_image: str, image_index: int, page_index: int, dir: str) -> str:
    """Cria o Pixmap, converte para RGB, salva a imagem no diretorio."""
    logger.debug(f"Salvando imagem xref {xref} da página {page_index}.")
    output_dir = f"output/imagens/{dir}"
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        pix = fitz.Pixmap(pdf, xref) 

        if pix.n - pix.alpha > 3: 
            pix = fitz.Pixmap(fitz.csRGB, pix)

        file_path = os.path.join(output_dir, f"{name_image}_pg{page_index}_img{image_index}.png")
        pix.save(file_path)
        logger.debug(f"Imagem salva: {file_path}")
        pix = None
    except Exception as e:
        logger.error(f"Falha ao salvar imagem xref {xref}: {e}")

    return abs_path(output_dir)

def make_markdown(summarize: str = None, metadata: str = None, filename: str = None):
    """Cria o arquivo markdown com os dados extraidos e/ou resumo."""
    logger.debug(f"Criando arquivo markdown: {filename}.md")
    path = f"output/markdown/{filename}.md"
    os.makedirs("output/markdown", exist_ok=True)
    markdown = open(path, "w", encoding="utf-8-sig")

    path = abs_path(path)
    logger.info(f"Arquivo markdown criado em: {path}")

    if summarize != None:
        markdown.write(summarize + "\n\n")
    if metadata != None:
        markdown.write(metadata + "\n\n")
    
    markdown.close()