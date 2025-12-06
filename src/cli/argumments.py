import sys, argparse, textwrap, rich_argparse
from src.utils.validator import validate_str, validate_path
from src.cli.handler_extract import handle_extract

class ArgumentParserPT(argparse.ArgumentParser):
    """Classe personalizada para traduzir mensagens de erro para português."""
    def error(self, message):
            if "expected one argument" in message:
                message = message.replace(
                    "expected one argument", 
                    "esperava um caminho de arquivo"
                )
            
            sys.stderr.write(f'ERRO: {message}\n\n')

            self.exit(2)

def build_parser() -> None:
    """Construi os argumentos a serem passados."""
    parser = ArgumentParserPT(prog="pdf_cli", description=textwrap.dedent("""
        Projeto: Resumo PDF CLI
        Descrição: Ferramenta de linha de comando (CLI), capaz de receber o caminho de um arquivo PDF em português como entrada, extrair informações 
        estruturais do documento e  gerar um resumo do seu conteúdo usando um modelo de linguagem local da Hugging Face.
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
                    - Se a flag -n não for especificada, um nome padrão será usado para salvar as imagens.
                    - As informações extraídas são salvas na pasta 'output/'.
                    - Todas as pastas são criadas automaticamente e salvas no diretório correspondente ao que está sendo executado.
        """), 
    formatter_class=rich_argparse.RawDescriptionRichHelpFormatter,
    add_help=False
    )

    # Caminho do arquivo
    parser.add_argument(
        '-p', 
        '--path', 
        type=validate_path, 
        help="Caminho para o arquivo PDF (obrigatório).", 
        required=True, 
        metavar="pdf_path"
    )

    # Extrair apenas o texto
    parser.add_argument(
        '-t', 
        '--text_only',
        help="Extrai apenas o texto e gera um Markdown com as informações extraídas do PDF.",
        action='store_true'
    )

    # Extrair apenas a imagem
    parser.add_argument(
        '-i',
        '--image',
        action='store_true',
        help='Extrai apenas as imagens do PDF.'
    )

    # Nome da imagem
    parser.add_argument(
        '-n',
        '--image_name',
        type=validate_str,
        help="Nome base opcional para salvar imagens (usado com `-i` ou `-e`)",
        metavar='name_image'
    )

    # Extrair apenas o resumo
    parser.add_argument(
        '-s',
        '--summarize',
        action='store_true',
        help="Gera apenas o resumo usando a LLM e salva em um arquivo markdown."
    )

    # Extrair tudo
    parser.add_argument(
        "-e",
        '--everything',
        action='store_true',
        help='Executa todas as etapas (texto, imagens e resumo).'
    )

    parser.set_defaults(func=handle_extract)

    return parser

def run() -> None:
    """Declara as funções necessárioas para construir a aplicação."""
    parser = build_parser()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()

    if hasattr(args, 'func'):
        try:
            args.func(args)
        except Exception:
            raise
    else:
        parser.print_help()