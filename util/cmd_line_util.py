import os
import config
import subprocess
from logger.server_logger import SERVER_LOGGER

def run_email_server():
    try:
        SERVER_LOGGER.info('Initializing SMTP server on port ' + str(config.PORT_EMAIL))
        subprocess.run('python3 -m smtpd -c DebuggingServer -n localhost:' + str(config.PORT_EMAIL), check=True)
        SERVER_LOGGER.info('Running on port ' + str(config.PORT_EMAIL))
    except subprocess.CalledProcessError as e:
        SERVER_LOGGER.info(e)
        SERVER_LOGGER.info('Email Server failed to startup')
    except subprocess.SubprocessError as e:
        SERVER_LOGGER.info(e)
        SERVER_LOGGER.info('Email Server Subprocess unexpectedly terminated.')
    except KeyboardInterrupt as e:
        SERVER_LOGGER.info(str(e))
        SERVER_LOGGER.info('Terminating Email Server')


def create_transaction_log(dispatch_id):
    SERVER_LOGGER.info('Creating log for dispatch ' + str(dispatch_id))
    dispatch_log = config.LOG_TRANSACTION + str(dispatch_id) + '_txn.log'
    os.system('touch ' + dispatch_log)
    try:
        subprocess.run('touch ' + dispatch_log, check=True)
        SERVER_LOGGER.info('Initialized log ' + dispatch_log)
    except subprocess.CalledProcessError as e:
        SERVER_LOGGER.info(e)
        SERVER_LOGGER.info('Transaction Log failed to initialize for dispatch ' + dispatch_id)
        return ""
    return dispatch_log
