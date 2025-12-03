from .cli.argumments import run

def main():
    """Função que inicia toda a aplicação."""
    try:
        run()
    except Exception as e:
        print(e)
if __name__ == '__main__':
    main()