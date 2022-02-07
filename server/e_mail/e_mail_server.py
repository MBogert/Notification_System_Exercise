from smtplib import SMTP
import config
from logger.server_logger import SERVER_LOGGER

def init_smtp():
    server = None
    try:
        SERVER_LOGGER.info('Starting Email Server...')
        server = SMTP(config.HOST_NAME + ':' + str(config.PORT_EMAIL))
    except ConnectionRefusedError as e:
        SERVER_LOGGER.info(e)
        SERVER_LOGGER.info('Confirm email server is already running. Have you run \'run_email_server.py\'?')
    return server

SMTP_SERVER = init_smtp()