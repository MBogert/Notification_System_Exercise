from pymongo import MongoClient
import certifi
from pymongo.errors import ConnectionFailure
from logger.server_logger import SERVER_LOGGER

import config

MONGO_CLIENT = MongoClient(config.MONGO_URI, tlsCAFile = certifi.where())

try:
    MONGO_CLIENT.admin.command('ping')
    SERVER_LOGGER.info('Mongo Client successfully initialized')
except ConnectionFailure as e:
    SERVER_LOGGER.info(e)
    SERVER_LOGGER.info('Mongo Client failed to connect to DB, please triage accordingly.')