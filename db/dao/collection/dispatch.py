from db.dao import mongo_dao as dao
from db.dao import field


def insert_dispatch(content):
    res = dao.insert_one(field.DB_COL_DISPATCH, content)
    return res

def get_dispatch_by_id(dispatch_id):
    return dao.get_one(field.DB_COL_DISPATCH, {field.DISPATCH_ID: dispatch_id})

