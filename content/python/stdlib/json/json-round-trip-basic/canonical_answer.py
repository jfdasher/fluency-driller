import json

def json_round_trip(obj):
    return json.loads(json.dumps(obj))
