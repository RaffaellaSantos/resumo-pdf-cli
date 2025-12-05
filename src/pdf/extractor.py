import os, logging
import re
from src.utils.text import count_words, get_urls, is_latex_pdf, sanitize_latex_text, normalize_text, search_section_keywords
from src.utils.files import open_pdf, get_text, format_output
from statistics import mode

logger = logging.getLogger(__name__)

def extract_pdf(pdf_path: str):
    """Extrai o PDF."""
    logger.debug(f"Iniciando extração do PDF: {pdf_path}")
    doc = open_pdf(pdf_path)
    try:
        metadata = extract_metadata(doc, pdf_path)
        out = format_output(metadata)
        print(out)

        return out
    finally:
        doc.close()

def extract_metadata(doc: str, pdf_path: str):
    """Extrai dados do PDF."""
    logger.debug("Iniciando extração de metadados do PDF.")
    try:
        page_count = doc.page_count
        size_kb = os.path.getsize(pdf_path) / 1024
        all_titles = []
        all_links = []

        is_latex = is_latex_pdf(doc)

        for page in doc:
            title = detect_struct(page)
            if title:
                if is_latex:
                    title = sanitize_latex_text(title)
                title = normalize_text(title)
                all_titles.append(title)
            links = get_urls(page.get_links())
            if links:
                all_links.append(links)
        
        full_text = get_text(doc)
        num_words, num_voc, top_10 = count_words(full_text, is_latex)

        return {
            "titles": all_titles,
            "page_count": page_count,
            "num_words": num_words,
            "num_voc": num_voc,
            "top_10": top_10,
            "size_kb": size_kb,
            "links": all_links
        }
    except Exception as e:
        logger.error(f"Problema ao extrair dados - {e}")

def detect_struct(page):
    """Detecta títulos reais usando heurísticas robustas."""
    logger.debug("Detectando títulos na página do PDF.")
    blocks = page.get_text("dict")["blocks"]

    spans = []
    for b in blocks:
        if "lines" in b:
            for line in b["lines"]:
                for span in line["spans"]:
                    spans.append(span)

    if not spans:
        return None
    font_sizes = [round(s["size"], 1) for s in spans]
    
    try:
        dominant_font = mode(font_sizes)
    except:
        from statistics import median
        dominant_font = median(font_sizes)

    titles = []

    for span in spans:
        text = span["text"].strip()
        if not text:
            continue

        font = round(span["size"], 1)

        if len(text) > 120:
            continue

        if text.count(" ") > 15:
            continue 

        if text.isupper():
            continue
    
        if re.search(r"\.{5,}", text):
            continue

        section = search_section_keywords(text)        
        if section:
            titles.append(section)
            logger.debug(f"Título detectado por palavra-chave de seção: {section}")
            continue        

        if any(p in text for p in [".", ";", ",", ":"]):
            continue 

        if font <= dominant_font * 1.25:
            continue

        if dominant_font < 10 and font < 14:
            continue
        
        titles.append(text)
        logger.debug(f"Título detectado por tamanho de fonte: {text}")

    seen = set()
    clean_titles = []
    for t in titles:
        if t not in seen:
            seen.add(t)
            clean_titles.append(t)

    return "; ".join(clean_titles) if clean_titles else None
