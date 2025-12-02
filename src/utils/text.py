import re
import unicodedata
from collections import Counter

# Stopwords básicas em português
STOPWORDS = {
    "a","as","o","os","de","do","da","dos","das","e","um","uma","uns","umas","que",
    "em","no","na","nos","nas","por","para","com","se","ao","aos","à","às",
    "não","mais","como","é","ser","são","seu","sua","seus","suas", "foi", "ser", 
    "estar", "é", "são", "ele", "ela", "nós"
}

def count_words(text: str):
    """Retira Stopwords e retorna o número de palavras geral, únicas e mais citadas no texto."""
    text = re.findall(r"[a-zA-ZÀ-ÿ]+", text.lower())
    filter_words = [w for w in text if w not in STOPWORDS]

    num_words = len(filter_words)

    vocabulary = set(filter_words)
    num_voc = len(vocabulary)

    top_10 = Counter(filter_words).most_common(10)

    return num_words, num_voc, top_10

def get_urls(links: dict):
    urls  = [link["uri"] for link in links if "uri" in link]

    return urls