from db.dao import mongo_dao as dao
from db.dao import field
from db.dao.collection import dispatch


def insert_dispatch_program(content):
    return dao.insert_one(field.DB_COL_DISPATCH_PROGRAM, content)

def get_dispatch_program(program_id):
    return dao.get_one(field.DB_COL_DISPATCH_PROGRAM, {field.PROGRAM_ID: program_id})

def get_dispatch_program_message_for_dispatch(dispatch_id):
    return dao.get_one(field.DB_COL_DISPATCH_PROGRAM, {field.PROGRAM_ID: dispatch.get_dispatch_by_id(dispatch_id)[field.PROGRAM_ID]})[field.MESSAGE]