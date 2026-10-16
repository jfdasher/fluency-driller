import json
import datetime

def serialize_with_datetime(obj):
    def default(o):
        if isinstance(o, datetime.datetime):
            return o.isoformat()
        raise TypeError(f'Object of type {type(o)} is not JSON serializable')
    return json.dumps(obj, default=default)
