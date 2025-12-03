import argparse, textwrap, rich_argparse
from src.utils.validator import validate_str, validate_path
from src.pdf.extractor import extract_pdf
from src.pdf.image import extract_image

def build_parser() -> None:
    """Construi os argumentos a serem passados."""
    parser = argparse.ArgumentParser(prog="cli_pdf", description=textwrap.dedent("""
        Ferramenta de linha de comando (CLI), capaz de receber o caminho de
        um arquivo PDF em português como entrada, extrair informações estruturais do documento e
        gerar um resumo do seu conteúdo usando um modelo de linguagem local da Hugging Face.
    """), 
    formatter_class=rich_argparse.RawDescriptionRichHelpFormatter)

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Teste para verificar se está funcionando
    info_parser = subparsers.add_parser(
        "info",
        help='Informações básicas sobre a aplicação.',
        formatter_class=rich_argparse.RawDescriptionRichHelpFormatter
    )
    info_parser.set_defaults(command='info')

    # info_parser.add_argument(
    #     'echo',
    #     type=str
    # )

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
                cli_pdf extract_pdf -t -p [path_pdf] "Extrai as informações do texto."
                cli_pdf extract_pdf -i -n [image_name] -p [path_pdf] "Extrai as figuras do documento."
                cli_pdf extract_pdf -s -p [path_pdf] "Retorna o resumo do texto."
                cli_pdf extract_pdf -e -n [image_name] -p [path_pdf] "Extrai informações, imagens e o resumo."
                
                Obs: É possível utilizar 'pdf' ao invés de extract_pdf.
        """),
        formatter_class=rich_argparse.RawDescriptionRichHelpFormatter
    )

    extractor_parser.set_defaults(command="extract_pdf", func=handle_extract)

    # Caminho do arquivo
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
        action='store_true',
        help='Extrai apenas as imagens. Necessita colocar o nome principal que as imagens terão, para isso utiliza a flag -n.'
    )

    # Nome da imagem
    extractor_parser.add_argument(
        '-n',
        '--image_name',
        type=validate_str,
        help="Nome com que as imagens serão salvas",
        metavar='name_image'
    )

    # Extrair apenas o resumo
    extractor_parser.add_argument(
        '-s',
        '--summarize',
        action='store_true',
        help="Resumo do PDF."
    )

    # Extrair tudo
    extractor_parser.add_argument(
        "-e",
        '--everything',
        action='store_true',
        help='Extraia informações, imagens e o resumo do PDF.'
    )

    return parser

def handle_extract(args):
    """Comunicação entre argumentos e funções."""
    path_pdf = args.path

    if args.text_only:
        print(f"Extraindo apenas as inforações do texto de: {path_pdf}\n")
        extract_pdf(path_pdf)
    elif args.image:
        if args.image_name:
            print(f"Extraindo apenas as imagens de: {path_pdf}\n")
            extract_image(path_pdf, args.image_name)
        else:
            raise ValueError("[Erro]: Nome das imagens não foi especificado. Utilize -n para especificar como as imagens devem ser nomeadas.")
    elif args.summarize:
        print(f"Construindo Resumo de: {path_pdf}\n")
        # TODO Adicionar resumo por LLM
    elif args.everything:
        print("Extraindo informações do texto (Dados, imagens, resumo).")
        if args.image_name:
            extract_pdf(path_pdf)
            extract_image(path_pdf, args.image_name)
        else:
            raise ValueError("[Erro]: Nome das imagens não foi especificado. Utilize -n para especificar como as imagens devem ser nomeadas.")
    else:
        raise ValueError("[Error]: Necessita de outras flags para indicar ação.")

def run() -> None:
    """Declara as funções necessárioas para construir a aplicação."""
    parser = build_parser()

    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

