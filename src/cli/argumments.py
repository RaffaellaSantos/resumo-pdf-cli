import argparse, textwrap, rich_argparse, logging
from src.utils.validator import validate_str, validate_path, define_name
from src.utils.files import make_markdown
from src.pdf.extractor import extract_pdf
from src.pdf.image import extract_image
from src.llm.summarize import summarize

logger = logging.getLogger(__name__)

def build_parser() -> None:
    """Construi os argumentos a serem passados."""
    parser = argparse.ArgumentParser(prog="pdf_cli", description=textwrap.dedent("""
        Projeto: Resumo PDF CLI
        Descrição: Ferramenta de linha de comando (CLI), capaz de receber o caminho de um arquivo PDF em português como entrada, extrair informações 
        estruturais do documento egerar um resumo do seu conteúdo usando um modelo de linguagem local da Hugging Face.
        Autor: Adriana Raffaella S. F.
        Ferramentas utilizadas:
            - PyMuPDF (fitz): Para manipulação e extração de dados de arquivos PDF.
            - Hugging Face, Ollama e Langchain: Para sumarização do texto extraído.
            - Rich argparse: Para melhorar a interface de linha de comando.
    """),
        epilog=textwrap.dedent("""
            Exemplos:
                pdf_cli -t -p ./teste.pdf "Extrai as informações do texto."
                pdf_cli -i -n nome_teste -p ./teste.pdf "Extrai as figuras do documento."
                pdf_cli -s -p ./teste.pdf "Retorna o resumo do texto."
                pdf_cli -e -n nome_teste -p ./teste.pdf "Extrai informações, imagens e o resumo."
                
                Observações: 
                    - Para extrair as imagens, é necessário especificar o nome com que as imagens serão salvas utilizando a flag -n.
                    - As informações extraídas e o resumo são salvos em um arquivo markdown na pasta 'markdown'.
                    - As imagens extraídas são salvas na pasta 'images/nome_do_arquivo/nome_da_imagem'.
                    - Todas as pastas são criadas automaticamente e salvas no diretório correspondente ao que está sendo executado.
        """), 
    formatter_class=rich_argparse.RawDescriptionRichHelpFormatter)

    # Caminho do arquivo
    parser.add_argument(
        '-p', 
        '--path', 
        type=validate_path, 
        help="Caminho do arquivo.", 
        required=True, 
        metavar="pdf_path"
    )

    # Extrair apenas o texto
    parser.add_argument(
        '-t', 
        '--text_only',
        help="Extrai apenas as informações do texto e gera markdown com conteúdo.",
        action='store_true'
    )

    # Extrair apenas a imagem
    parser.add_argument(
        '-i',
        '--image',
        action='store_true',
        help='Extrai apenas as imagens.'
    )

    # Nome da imagem
    parser.add_argument(
        '-n',
        '--image_name',
        type=validate_str,
        help="Nome com que as imagens serão salvas",
        metavar='name_image'
    )

    # Extrair apenas o resumo
    parser.add_argument(
        '-s',
        '--summarize',
        action='store_true',
        help="Resume o PDF e gera markdown com conteúdo."
    )

    # Extrair tudo
    parser.add_argument(
        "-e",
        '--everything',
        action='store_true',
        help='Extraia informações, imagens e o resumo do PDF. Salva as informações e o resumo em um arquivo markdown.'
    )

    parser.set_defaults(func=handle_extract)

    return parser

def handle_extract(args):
    """Comunicação entre argumentos e funções."""

    logger.debug(f"Argumentos recebidos: {vars(args)}")

    if not args.path:
        logger.error("Caminho do arquivo não foi especificado.")
    path_pdf = args.path
    filename = define_name(path_pdf)

    if args.text_only:
        logger.info(f"Extraindo apenas as inforações do texto de: {filename}\n")
        metadata = extract_pdf(path_pdf)
        make_markdown(metadata=metadata, filename=filename)
        logger.info("Metadados extraidos e markdown criado com sucesso.")

    elif args.image:
        if args.image_name:
            logger.info(f"Extraindo apenas as imagens de: {filename}\n")
            extract_image(path_pdf, args.image_name, filename)
            logger.info("Imagens extraidas com sucesso.")
        else:
            logger.error("Nome das imagens não foi especificado. Utilize -n para especificar como as imagens devem ser nomeadas.")
        
    elif args.summarize:
        logger.info(f"Construindo Resumo de: {filename} com LLM.\n")
        logger.info("Isso pode levar alguns minutos dependendo do tamanho do documento e do modelo utilizado.")
        summa = summarize(path_pdf)
        make_markdown(summarize=summa, filename=filename)
        logger.info("Resumo criado e markdown salvo com sucesso.")

    elif args.everything:
        logger.info("Extraindo informações do texto (Dados, imagens, resumo).")

        if args.image_name:
            logger.info(f"Etapa 1: Extraindo todas as informações de: {filename}\n")
            metadata = extract_pdf(path_pdf)

            logger.info("Etapa 2: Extraindo todas as imagens.\n")
            extract_image(path_pdf, args.image_name, filename)

            logger.info("Etapa 3: Construindo Resumo com LLM.\n")
            summa = summarize(path_pdf)
            make_markdown(summarize=summa, metadata=metadata, filename=filename)
            logger.info("Todas as informações extraidas e markdown criado com sucesso.")
        else:
            logger.error("Nome das imagens não foi especificado. Utilize -n para especificar como as imagens devem ser nomeadas.")
    else:
        logger.error("Necessita de outras flags para indicar ação.")

def run() -> None:
    """Declara as funções necessárioas para construir a aplicação."""
    parser = build_parser()

    args = parser.parse_args()

    if hasattr(args, 'func'):
        try:
            args.func(args)
        except Exception:
            raise
    else:
        parser.print_help()