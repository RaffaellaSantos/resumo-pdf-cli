import logging
from .config.logging_config import setup_logging


def main():
    """Função que inicia toda a aplicação."""
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Iniciando a aplicação...")

    try:
        from .cli.argumments import run
        run()
        logger.info("Aplicação finalizada com sucesso.")

    except KeyboardInterrupt:
        logger.warning("Operação interrompida pelo usuário.")

    except Exception as e:
        logger.error(f"Ocorreu um erro: {e}")
        
if __name__ == '__main__':
    main()