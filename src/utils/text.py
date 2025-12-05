import re, fitz, unicodedata, logging
from typing import Dict
from collections import Counter

logger = logging.getLogger(__name__)

# Stopwords básicas em português
STOPWORDS = {
    "a","as","o","os","de","do","da","dos","das","e","um","uma","uns","umas","que",
    "em","no","na","nos","nas","por","para","com","se","ao","aos","à","às",
    "não","mais","como","é","ser","são","seu","sua","seus","suas", "foi", "ser", 
    "estar", "é", "são", "ele", "ela", "nós", "apenas", "este", "será", "pelo",
    "and", "cão", "ca", "ou", "cada", "pode"
}

def is_latex_pdf(doc: fitz.Document) -> bool:
    """Detecta arquivos feitos com latex"""
    logger.debug("Detectando se o PDF foi criado com LaTeX.")
    metadata = doc.metadata
    if not metadata:
        return False
    
    producer = metadata.get('producer', '').lower()
    creator = metadata.get('creator', '').lower()

    latex_keywords = [
        'latex', 'pdftex', 'luatex', 'xetex', 'tex live', 'dvips', 'overleaf'
    ]

    is_latex = any(key in producer or key in creator for key in latex_keywords)

    return is_latex

def normalize_text(text: str) -> str:
    """Normaliza o texto."""
    logger.debug("Normalizando o texto.")
    text = unicodedata.normalize("NFKC", text)
    
    return text

# TODO Usar ocr (Tesseract 3) para ler os PDF.
def sanitize_latex_text(text: str) -> str:
    """
    Corrige artefatos comuns de PDFs gerados por LaTeX (acentos separados,
    hifenização de quebra de linha, ligaduras quebradas).
    """
    logger.debug("Sanitizando texto LaTeX.")
    text = text.replace(" ̧c", "ç").replace("¸c", "ç").replace(" ¸", "¸")

    text = re.sub(r'([cCaAoO])\s+([¸~^´`])', r'\1\2', text)

    replacements = {
        "c¸": "ç",   "C¸": "Ç",
        "a˜": "ã",   "A˜": "Ã",
        "o˜": "õ",   "O˜": "Õ",
        "˜a": "ã",   "˜o": "õ",
        
        "´a": "á",   "´A": "Á",
        "´e": "é",   "´E": "É",
        "´i": "í",   "´I": "Í",
        "´o": "ó",   "´O": "Ó",
        "´u": "ú",   "´U": "Ú",
        
        "a´": "á",   "e´": "é",   "i´": "í",   "o´": "ó",   "u´": "ú",

        "^a": "â",   "^e": "ê",   "´ı": "í",   "^o": "ô",   "ç˜": "çã",
        
        "`a": "à",   "`A": "À",   "´i": "í",   "ˆe": "ê",

        "’": "'",    "”": '"',    "“": '"',
    }

    for bad, good in replacements.items():
        text = text.replace(bad, good)

    text = re.sub(r'(?<=[a-zA-Z])\s+ç', r'ç', text)
    text = re.sub(r'ç\s+(?=[a-zA-Z])', r'ç', text)

    text = re.sub(r'([a-zA-ZÀ-ÿ])-(\n\s*)([a-zA-ZÀ-ÿ])', r'\1\3', text)

    return text

def count_words(text: str, is_latex: bool):
    """Retira Stopwords e retorna o número de palavras geral, únicas e mais citadas no texto."""
    logger.debug("Contando palavras no texto.")
    if is_latex:
        text = sanitize_latex_text(text)
        logger.debug("Texto sanitizado para LaTeX.")
    
    text = normalize_text(text)    

    text = re.findall(r"[^\W\d_]+", text.lower(), re.UNICODE)

    filter_words = [w for w in text if w not in STOPWORDS]

    num_words = len(filter_words)
    vocabulary = set(filter_words)
    num_voc = len(vocabulary)
    top_10 = Counter(filter_words).most_common(10)

    return num_words, num_voc, top_10

def get_urls(links: Dict) -> Dict:
    """Extrai apenas as urls do texto."""
    logger.debug("Extraindo URLs do texto.")
    urls  = [link["uri"] for link in links if "uri" in link]

    return urls