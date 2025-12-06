import logging
from rich.console import Console
from src.utils.validator import define_name
from src.utils.files import make_markdown
from src.pdf.extractor import extract_pdf
from src.pdf.image import extract_image
from src.llm.summarize import summarize

console = Console()
logger = logging.getLogger(__name__)

def handle_extract(args):
    """Comunicação entre argumentos e funções."""

    logger.debug(f"Argumentos recebidos: {vars(args)}")

    if not args.path:
        logger.error("Caminho do arquivo não foi especificado.")
        return
        
    path_pdf = args.path
    filename = define_name(path_pdf)

    name_image = args.image_name or f"{filename}_imagem"
    logger.debug(f"Nome base para imagens: {name_image}")

    extract_text = args.text_only or args.everything or (args.text_only and args.summarize)
    extract_img = args.image or args.everything or (args.text_only and args.image) or (args.summarize and args.image)
    extract_sum = args.summarize or args.everything

    metadata = None
    summa = None

    try:
        if not (extract_text or extract_img or extract_sum):
            logger.error("Nenhuma ação especificada. Consulte a ajuda com -h/--help para mais informações.")
            return

        if extract_text:
            logger.debug("Iniciando extração de texto.")
            with console.status("[bold green]Lendo o PDF e extraindo metadados...", spinner="dots"):
                metadata = extract_pdf(path_pdf)

        if extract_img:
            logger.debug("Iniciando extração de imagens.")
            with console.status("[bold green]Lendo o PDF e extraindo imagens...", spinner="dots"):
                extract_image(path_pdf, name_image, filename)

        if extract_sum:
            logger.debug("Iniciando resumo do PDF.")
            with console.status("[bold green]Lendo o PDF e gerando resumo com LLM...", spinner="dots"):
                summa = summarize(path_pdf)

        if metadata or summa:
            logger.debug("Criando arquivo markdown com os resultados.")
            make_markdown(summarize=summa, metadata=metadata, filename=filename)
    except Exception as e:
        logger.error(f"Ocorreu um erro durante o processamento: {e}")
