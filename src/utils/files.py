from typing import Dict
import fitz, os, logging

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
    titles = "\n".join(f"- {t}" for t in metadata['titles'])
    out = (
    "## **Dados extraidos**\n\n"
    f"**Título das seções**: \n{titles}\n\n"
    f"**Número de páginas**: {metadata['page_count']}\n\n"
    f"**Número de palavras**: {metadata['num_words']}\n\n"
    f"**Número de palavras únicas**: {metadata['num_voc']}\n\n"
    f"**10 palavras mais citadas**: {metadata['top_10']}\n\n"
    f"**Tamanho do arquivo (KB)**: {metadata['size_kb']:.2f}\n\n"
    f"**Links**: {metadata['links']}\n\n"
    )

    return out 

def pixmap(pdf: str, xref: str, name_image: str, image_index: int, page_index: int, dir: str):
    """Cria o Pixmap, converte para RGB, salva a imagem no diretorio."""
    logger.debug(f"Salvando imagem xref {xref} da página {page_index}.")
    output_dir = f"images/{dir}/{name_image}"
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        pix = fitz.Pixmap(pdf, xref) 

        if pix.n - pix.alpha > 3: 
            pix = fitz.Pixmap(fitz.csRGB, pix)

        file_path = os.path.join(output_dir, f"{name_image}_pg{page_index}_img{image_index}.png")
        pix.save(file_path)
        logger.info(f"Imagem salva: {file_path}")
        pix = None
    except Exception as e:
        logger.error(f"Falha ao salvar imagem xref {xref}: {e}")

def make_markdown(summarize: str = None, metadata: str = None, filename: str = None):
    """Cria o arquivo markdown com os dados extraidos e/ou resumo."""
    logger.debug(f"Criando arquivo markdown: {filename}.md")
    path = f"markdown/{filename}.md"
    os.makedirs("markdown", exist_ok=True)
    markdown = open(path, "w", encoding="utf-8-sig")

    if summarize != None:
        markdown.write(summarize + "\n\n")
    if metadata != None:
        markdown.write(metadata + "\n\n")
    
    markdown.close()