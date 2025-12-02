import os
from src.utils.text import count_words, get_urls
from src.utils.files import output, open_pdf

def extract_pdf(pdf_path: str):
    """Extrai o PDF."""
    pdf_extraido = open_pdf(pdf_path)
    metadata = extract_metadata(pdf_extraido, pdf_path)

    output(metadata)

def extract_metadata(pdf_extraido, pdf):
    """Extrai dados do PDF."""
    page_count = pdf_extraido.page_count
    size_kb = os.path.getsize(pdf) / 1024
    all_titles = []
    all_links = []
    full_text = ""

    for page in pdf_extraido:
        full_text += page.get_text() + "\n"
        title = detect_struct(page)
        if title:
            all_titles.append(title)
        links = get_urls(page.get_links())
        if links:
            all_links.append(links)

    num_words, num_voc, top_10 = count_words(full_text)

    return {
        "titles": all_titles,
        "page_count": page_count,
        "num_words": num_words,
        "num_voc": num_voc,
        "top_10": top_10,
        "size_kb": size_kb,
        "links": all_links
    }

def detect_struct(page):
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
