import argparse, textwrap, rich_argparse
from src.utils.validator import validate_str, validate_path
from src.pdf.extractor import extract_pdf
from src.pdf.image import extract_image

def build_parser() -> None:
    parser = argparse.ArgumentParser(prog="Extrator_PDF", description=textwrap.dedent("""
        Ferramenta de linha de comando (CLI), capaz de receber o caminho de
        um arquivo PDF em português como entrada, extrair informações estruturais do documento e
        gerar um resumo do seu conteúdo usando um modelo de linguagem local da Hugging Face.
    """), 
    formatter_class=rich_argparse.RawDescriptionRichHelpFormatter)

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Teste para verificar se está funcionando
    health_parser = subparsers.add_parser(
        "health",
        help='Teste de comando',
        formatter_class=rich_argparse.RawDescriptionRichHelpFormatter
    )
    health_parser.set_defaults(command='health')

    health_parser.add_argument(
        'echo',
        type=str
    )

    # Comando para extrair PDF (Texto / imagem / resumo)
    extractor_parser = subparsers.add_parser(
        "extract_pdf", 
        aliases=['pdf'], 
        description=textwrap.dedent("""
        Use este comando para extrair informações do PDF (número de páginas, palavras escritas, palavras mais repetidas, etc).
        Forneça uma flag para extrair apenas o texto e/ou extrair as imagens.
    """),
        help='Extrair PDF.',
        epilog=textwrap.dedent("""
            Exemplos:
                cli_pdf extract_pdf -p "caminho do documento" # Extrai todas as informações
                cli_pdf extract_pdf -t -p "caminho do documento" # Apenas o texto
                cli_pdf extract_pdf -i -p "caminho do documento" # Apenas a imagem
                cli_pdf extract_pdf -s  -p "caminho do documento" # Apenas o resumo do LLM
        """),
        formatter_class=rich_argparse.RawDescriptionRichHelpFormatter
    )

    extractor_parser.set_defaults(command="extract_pdf", func=handle_extract)

    # Caminho do arquivo  (Se apenas este comando for usado ele entrega tudo.)
    extractor_parser.add_argument(
        '-p', 
        '--path', 
        type=validate_path, 
        help="Caminho do arquivo.", 
        required=True, 
        metavar="pdf_path"
    )

    # Extrair apenas o texto
    extractor_parser.add_argument(
        '-t', 
        '--text_only',
        help="Extrai apenas as informações do texto",
        action='store_true'
    )

    # Extrair apenas a imagem
    extractor_parser.add_argument(
        '-i',
        '--image',
        type=validate_str,
        help="Extrai apenas as imagens, necessita colocar o nome principal que as imagens terão.",
        metavar='name_image'
    )

    # Extrair apenas o resumo
    extractor_parser.add_argument(
        '-s',
        '--summarize',
        action='store_true',
        help="Resumo do PDF."
    )

    return parser

def handle_extract(args):
    path_pdf = args.path

    if args.text_only:
        print(f"Extraindo apenas as inforações do texto de: {path_pdf}\n")
        extract_pdf(path_pdf)
    elif args.image:
        print(f"Extraindo apenas as imagens de: {path_pdf}\n")
        extract_image(path_pdf, args.image)
    elif args.summarize:
        print(f"Construindo Resumo de: {path_pdf}\n")
    else:
        print("Extraindo informações do texto (Dados, imagens, resumo).")

def run() -> None:
    parser = build_parser()

    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

    print(args)

