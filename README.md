# Resumo PDF CLI

Ferramenta de linha de comando (CLI) para extrair texto e imagens de arquivos PDF em Português e gerar um resumo formatado em Markdown usando um modelo de linguagem local (via Ollama + LangChain).

**Principais recursos**
- Extrair metadados e texto estruturado de PDFs.
- Extrair imagens incorporadas no PDF.
- Gerar resumos em Português com saída em Markdown contendo título, resumo e palavras-chave.
- Salvar resultados automaticamente em pastas `markdown/` e `images/`, as duas pastas são salvas em `output/`.
- Possui logs em terminal e salva em arquivo.

**Estrutura do projeto (resumida)**

```
resumo-pdf-cli/
├── src/
│   ├── cli/          # argumentos e interface CLI
|   ├── config/       # arquivo de configuração (Logs)
│   ├── llm/          # integração com LLM (Ollama / LangChain)
│   ├── pdf/          # extração de texto e imagens do PDF
│   └── utils/        # helpers (arquivos, validações, formatação)
├── pdf_exemplos/     # PDFs utilizados para testar aplicação
├── pyproject.toml
└── README.md
```

## Ferramenta utilizadas

- **PyMuPDF** (fitz): Manipulação e extração de dados de arquivos PDF.

- **Hugging Face**: Utilizado para sumarização e processamento de linguagem natural.

- **Ollama**: Executa modelos de linguagem localmente de forma simples e rápida.

- **LangChain**: Framework para orquestrar modelos de linguagem e construir pipelines.

- **Rich Argparse**: Melhora e estiliza a interface de linha de comando.

## Requisitos
- Python 3.10+ (recomendado)
- Ter o `ollama` instalado e em execução localmente com o modelo necessário.
- Dependências Python definidas em `pyproject.toml`.

Observação: a biblioteca usa `OllamaLLM` via LangChain para se comunicar com modelos locais (ex.: `tensorblock/SummLlama3.2-3B-GGUF`).

## Instalação

1. Crie e ative um ambiente virtual:

```bash
python -m venv .venv
source .venv/bin/activate (Linux)
.venv/Scripts/Activate (Windows)
```

2. Instale o pacote em modo editável (a partir da raiz do projeto):

```bash
pip install -e .
```

3. Garanta que o `ollama` está em execução e que o modelo desejado está disponível localmente.

## Uso

O entrypoint da CLI é `pdf_cli`. Para ver as opções de linha de comando:

```bash
pdf_cli
```

Argumentos principais:
- `-p, --path`: caminho para o arquivo PDF (obrigatório)
- `-t, --text_only`: extrai apenas o texto e gera um Markdown
- `-i, --image`: extrai apenas as imagens
- `-n, --image_name`: nome base opcional para salvar imagens (usado com `-i` ou `-e`)
- `-s, --summarize`: gera apenas o resumo usando a LLM
- `-e, --everything`: executa todas as etapas (texto, imagens e resumo)

Exemplos:

```bash
# Extrair texto e criar markdown
pdf_cli -p ./teste.pdf -t

# Extrair imagens (salva em images/<nome_do_arquivo>/)
pdf_cli -p ./teste.pdf -i -n nome_exemplo

# Gerar resumo em Markdown
pdf_cli -p ./teste.pdf -s

# Executar tudo (texto, imagens e resumo)
pdf_cli -p ./teste.pdf -e -n nome_exemplo
```

## Saída
- Resumos e metadados são salvos como arquivos Markdown na pasta `output/markdown/`.
- Imagens extraídas são salvas em `output/imagens/<nome_do_arquivo>/` com o nome base padrão definido pelo sistema ou pelo inserido junto a flag `n`.
- Gera um arquivo `app.log` para visualização de logs da aplicação.

## Modelo / LLM

O projeto utiliza `OllamaLLM` integrado ao LangChain. O modelo padrão configurado no código é:

```
hf.co/tensorblock/SummLlama3.2-3B-GGUF:Q5_K_M
```

**[tensorblock/SummLlama3.2-3B-GGUF](https://huggingface.co/tensorblock/SummLlama3.2-3B-GGUF)**

## Autor

**Adriana Raffaella S. F.**