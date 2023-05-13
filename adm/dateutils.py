from datetime import datetime
import time
from dateutil.tz import *

def convert_to_local_timestamp(date: str):
    generated_utc_date = datetime.fromisoformat(date)
    generated_utc_date = generated_utc_date.replace(tzinfo=tzutc())

    generated_local_date = generated_utc_date.astimezone(tzlocal())

    return int(time.mktime(generated_local_date.timetuple()))