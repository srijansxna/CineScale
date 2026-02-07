import redis
import json

r = redis.Redis(host="localhost", port=6379, db=2)

def set_status(job_id, status, extra=None):
    payload = {"status": status}
    if extra:
        payload.update(extra)
    r.set(job_id, json.dumps(payload))

def get_status(job_id):
    data = r.get(job_id)
    if not data:
        return None
    return json.loads(data)
