import datetime
import json
from db.dao import field

def get_current_timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def add_dispatch_id(data, dispatch_id):
    j = json.loads(data)
    j[field.DISPATCH_ID] = str(dispatch_id)
    return str(j)