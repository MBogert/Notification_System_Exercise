from db.dao import mongo_dao as dao
from db.dao import field
from db.dao.collection import user

def insert_user_group(content):
    return dao.insert_one(field.DB_COL_USER, content)

def get_user_group(group_id):
    return dao.get_one(field.DB_COL_USER, {field.GROUP_ID: group_id})

def get_user_groups(group_ids):
    return dao.get_many(field.DB_COL_USER_GROUP, {field.GROUP_ID: {'$in': group_ids}})

def get_users_for_user_group(group_id):
    return user.get_users_in_group(group_id)