from db.dao import mongo_dao as dao
from db.dao import field
from db.dao.collection import dispatch, event_type

# Comm Modal Instances
COMM_SMS = 'SMS'
COMM_EMAIL = 'EMAIL'

def insert_communication_modal(content):
    return dao.insert_one(field.DB_COL_COMMUNICATION_MODAL, content)

def get_communication_modal(code):
    return dao.get_one(field.DB_COL_COMMUNICATION_MODAL, {field.CODE: code})

def get_many_communication_modals(codes):
    return dao.get_many(field.DB_COL_COMMUNICATION_MODAL, {field.CODE: { '$in': codes}})

def get_communication_modals_for_dispatch(dispatch_id):
    modals = get_many_communication_modals(event_type.get_event_type(dispatch.get_dispatch_by_id(dispatch_id)[field.EVENT_TYPE_ID])[field.USER_GROUP_IDS])
    return modals
    return get_many_communication_modals()