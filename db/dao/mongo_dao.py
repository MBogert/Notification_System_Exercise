import json
from db.mongo_client import MONGO_CLIENT
from db.dao import field

def get_db():
    return MONGO_CLIENT.get_database(field.DB_DISPATCH)

#==========================#
# Abstract CRUD Operations #
#==========================#
def insert_one(collection, content):
    return get_db()[collection].insert_one(json.loads(content))

def insert_many(collection, content):
    return get_db()[collection].insert_many(content)

def get_one(collection, query = {}):
    return get_db()[collection].find_one(query)

def get_many(collection, query = {}):
    return get_db()[collection].find(query)

def get_all(collection):
    return get_db()[collection].find()

def edit_one(collection, query, new_values = {}):
    return get_db()[collection].update_one(query, new_values)

def edit_many(collection, query, new_values = {}):
    return get_db()[collection].update_many(query, new_values)

def delete_one(collection, query):
    return get_db()[collection].delete_one(query)

def delete_many(collection, query= {}):
    return get_db()[collection].delete_many(query)

def clear_collection(collection):
    return get_db()[collection].delete_many({})
