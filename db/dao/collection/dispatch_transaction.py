from db.dao import mongo_dao as dao
from db.dao import field

def create_dispatch_transaction(dispatch_id, timestamp, status, log):
    transaction_data = str({
        field.DISPATCH_ID: dispatch_id,
        field.TIMESTAMP: timestamp,
        field.STATUS: status,
        field.LOG: log,
    }).replace("\'", "\"")
    return insert_dispatch_transaction(transaction_data)

def insert_dispatch_transaction(content):
    return dao.insert_one(field.DB_COL_DISPATCH_TRANSACTION, content)

def get_dispatch_transaction(dispatch_id):
    return dao.get_one(field.DB_COL_DISPATCH_TRANSACTION, {field.DISPATCH_ID: dispatch_id})