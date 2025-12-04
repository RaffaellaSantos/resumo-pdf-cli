from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from typing import Dict

model = OllamaLLM(model="hf.co/tensorblock/SummLlama3.2-3B-GGUF:Q5_K_M")

def make_prompt() -> Dict:
    """Define o prompt que será usado e cria a cadeia."""
    try:
        template = """
            Sua tarefa é resumir textos, formatar tudo em Markdown e identificar palavras-chave.

            ## REGRAS
            - Responda sempre em Português-BR
            - Baseie-se exclusivamente no texto fornecido.
            - Mantenha a organização do documento em Markdown.
            - Não invente informações que não existam no texto original.

            ## INSTRUÇÕES DE SAÍDA
            Você deve produzir um único documento em Markdown contendo:
            - ## **[Título do texto]** (retirado do texto; caso não exista, gerar um título a partir do conteúdo)
            - ## **Resumo** (claro, objetivo e fiel ao conteúdo)
            - ## **Palavras-chave** (lista de 3 a 8 palavras relevantes)

            ## TEXTO PARA RESUMO
            "{text}"

        """

        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | model

        return chain
    except Exception as e:
        raise ValueError(f"[ERROR]: Ocorreu um erro na montagem do prompt - {e}")