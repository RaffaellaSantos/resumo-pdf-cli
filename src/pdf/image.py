from src.utils.files import open_pdf, pixmap

def extract_image(pdf: str, name_image: str):
    """Extrair e guarda imagens do pdf."""
    pdf_extraido = open_pdf(pdf)

    for page_index in range(len(pdf_extraido)):
        page = pdf_extraido[page_index]
        image_list = page.get_images()

        # if image_list:
        #     print(f"Imagem encontrada {len(image_list)} nas páginas {page_index}")
        # else:
        #     print(f"Sem imagem na página: {page_index}")

        for image_index, img in enumerate(image_list, start=1):
            xref = img[0] 
            pixmap(pdf_extraido, xref, name_image, image_index, page_index)