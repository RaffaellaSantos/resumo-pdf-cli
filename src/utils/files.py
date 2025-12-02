from typing import Dict
import fitz, os

def open_pdf(pdf_path: str):
    return fitz.open(pdf_path)

def format_output(metadata: Dict):
    """Constroi a saída dos dados extraidos do pdf."""
    return {
        "titles": metadata['titles'],
        "page_count": metadata['page_count'],
        "num_words": metadata['num_words'],
        "num_voc": metadata['num_voc'],
        "top_10": metadata['top_10'],
        "size_kb": metadata['size_kb'],
        "links": metadata['links']
    }

def output(metadata: Dict):
    """Mostra os dados extraidos."""
    out = format_output(metadata)
    print("=====Dados extraidos=====")
    print(f"Título das seções: {out['titles']}\n")
    print(f"Número de páginas: {out['page_count']}\n")
    print(f"Número de palavras: {out['num_words']}\n")
    print(f"Número de palavras únicas: {out['num_voc']}\n")
    print(f"10 palavras mais citadas: {out['top_10']}\n")
    print(f"Tamanho do arquivo (KB): {out['size_kb']:.2f}\n")
    print(f"Links: {out['links']}\n")

def pixmap(pdf, xref, name_image, image_index, page_index):
    """Cria o Pixmap, converte para RGB, salva a imagem no diretorio."""
    output_dir = f"images/{name_image}"
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        pix = fitz.Pixmap(pdf, xref) 

        if pix.n - pix.alpha > 3: 
            pix = fitz.Pixmap(fitz.csRGB, pix)

        file_path = os.path.join(output_dir, f"{name_image}_pg{page_index}_img{image_index}.png")
        pix.save(file_path)
        print(f"[Salvo] {file_path}")
        pix = None
    except Exception as e:
        print(f"[Erro] Falha ao salvar imagem xref {xref}: {e}")