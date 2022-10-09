from datetime import datetime
from uuid import uuid4


TimeRep = float

def get_current_time() -> TimeRep:
    present_date = datetime.now()
    unix_timestamp = datetime.timestamp(present_date) * 1000
    return unix_timestamp
    

def create_uuid() -> str:
    return str(uuid4())