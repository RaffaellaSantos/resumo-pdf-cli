from src.utils.files import open_pdf, pixmap
import logging

logger = logging.getLogger(__name__)

def extract_image(pdf: str, name_image: str, dir_name: str):
    """Extrair e guarda imagens do pdf."""
    logger.debug(f"Extraindo imagens do PDF: {pdf}")
    pdf_extraido = open_pdf(pdf)

    for page_index in range(len(pdf_extraido)):
        page = pdf_extraido[page_index]
        image_list = page.get_images()

        if image_list:
            logger.debug(f"Quantidades de imagens encontradas {len(image_list)} na página {page_index}")
        else:
            logger.debug(f"Sem imagem na página: {page_index}")

        for image_index, img in enumerate(image_list, start=1):
            xref = img[0] 
            path = pixmap(pdf_extraido, xref, name_image, image_index, page_index, dir_name)

    logger.info(f"Imagens salvas em: {path}")