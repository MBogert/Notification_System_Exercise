from db.dao import mongo_dao as dao
from db.dao import field

def insert_event_type(content):
    return dao.insert_one(field.DB_COL_EVENT_TYPE, content)

def get_event_type(event_type_id):
    return dao.get_one(field.DB_COL_EVENT_TYPE, {field.EVENT_TYPE_ID: event_type_id})
