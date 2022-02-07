import logging
from http.server import HTTPServer
from server.dispatch_handler import DispatchHandler
import config
from db.mongo_client import MONGO_CLIENT
from logger.server_logger import SERVER_LOGGER
from server.e_mail.e_mail_server import SMTP_SERVER


server_address = ('', config.DISPATCH_PORT)
httpd = HTTPServer(server_address, DispatchHandler)
SERVER_LOGGER.info('Starting dispatch server...\n')
print('Starting dispatch server...\n')
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    pass
httpd.server_close()
SERVER_LOGGER.info('Dispatch server terminated...')
print('Dispatch server terminated...')
MONGO_CLIENT.close()
SERVER_LOGGER.info('Mongo Client closed')
print('Mongo Client closed')
SMTP_SERVER.quit()
SERVER_LOGGER.info('Email Server terminated')
print('Email Server closed')
logging.shutdown()
print('Shutdown...')

