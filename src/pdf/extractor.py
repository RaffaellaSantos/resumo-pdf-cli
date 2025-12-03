import os
from src.utils.text import count_words, get_urls, is_latex_pdf, sanitize_latex_text, normalize_text
from src.utils.files import output, open_pdf

def extract_pdf(pdf_path: str):
    """Extrai o PDF."""
    doc = open_pdf(pdf_path)
    try:
        metadata = extract_metadata(doc, pdf_path)
        output(metadata)
    finally:
        doc.close()

def extract_metadata(doc: str, pdf_path: str):
    """Extrai dados do PDF."""
    page_count = doc.page_count
    size_kb = os.path.getsize(pdf_path) / 1024
    all_titles = []
    all_links = []
    full_text = ""

    is_latex = is_latex_pdf(doc)

    for page in doc:
        full_text += page.get_text() + "\n"
        title = detect_struct(page)
        if title:
            if is_latex:
                title = sanitize_latex_text(title)
            title = normalize_text(title)
            all_titles.append(title)
        links = get_urls(page.get_links())
        if links:
            all_links.append(links)

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

def detect_struct(page: str) -> str:
    """Detecta os Títulos das seções."""
    blocks = page.get_text("dict")["blocks"]

    titles = []
    font_sizes = []

    for b in blocks:
        if "lines" in b:
            for line in b["lines"]:
                for span in line["spans"]:
                    font_sizes.append(span["size"])

    medium_font = sum(font_sizes) / len(font_sizes) if font_sizes else 12

    for b in blocks:
        if "lines" in b:
            for line in b["lines"]:
                for span in line["spans"]:
                    text = span["text"].strip()
                    if not text:
                        continue
                    if span["size"] >= medium_font * 1.2:
                        titles.append(text)
    return "; ".join(titles) if titles else None
