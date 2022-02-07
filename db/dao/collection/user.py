from db.dao import mongo_dao as dao
from db.dao import field
from db.dao.collection import dispatch, event_type, user_group

def insert_user(content):
    return dao.insert_one(field.DB_COL_USER, content)

def get_user_phone(user_id):
    return dao.get_one(field.DB_COL_USER)[field.PHONE]

def get_user_email(user_id):
    return dao.get_one(field.DB_COL_USER)[field.EMAIL]

def get_user_phone_numbers_for_dispatch(dispatch_id):
    return user_group.g(event_type.get_event_type(dispatch.get_dispatch_by_id(dispatch_id)[field.EVENT_TYPE_ID])[field.USER_GROUP_IDS])

def get_users_in_group(group_id):
    return dao.get_many(field.DB_COL_USER, {field.USER_GROUP_IDS: group_id})
