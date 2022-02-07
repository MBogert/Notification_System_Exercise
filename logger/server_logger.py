import logging
import os
import time
import config

def clean_server_logs():
    print('Cleaning server logs')
    if os.path.exists(config.LOG_HOME + config.SERVER_LOG):
        print('Migrating old server log')
        archive_log_name = '/' + str(int(time.time())) + '_' + config.SERVER_LOG
        os.system('mv ' + config.LOG_HOME + config.SERVER_LOG + ' ' + config.LOG_SERVER_ARCHIVE + archive_log_name)
        print('Log archived to ' + archive_log_name)
    os.system('touch ' + config.LOG_HOME + config.SERVER_LOG)
    print('New server log created')

clean_server_logs()
SERVER_LOGGER = logging.getLogger('Server_Log')
SERVER_LOGGER.setLevel(logging.INFO)
s_f_handler = logging.FileHandler('logs/server_log.log')
s_f_handler.setFormatter(logging.Formatter(fmt=config.DATE_TIME_LOG_FORMAT))
s_f_handler.setLevel(logging.INFO)
SERVER_LOGGER.addHandler(s_f_handler)
SERVER_LOGGER.info('SERVER LOGGER INITIALIZED')