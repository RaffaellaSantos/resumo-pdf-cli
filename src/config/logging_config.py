import logging, logging.config

def setup_logging():
    """Configura o logging para a aplicação."""
    logging_config = {
        'version': 1,
        'formatters': {
            'standard': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'standard',
                'level': logging.INFO,
            },
            'file': {
                'class': 'logging.FileHandler',
                'formatter': 'standard',
                'level': logging.DEBUG,
                'filename': 'app.log',
                'encoding': 'utf8'
            }
        },
        'root': {
            'handlers': ['console', 'file'],
            'level': logging.DEBUG,
        },
    }
    
    logging.config.dictConfig(logging_config)