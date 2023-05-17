"""Datetime utility functions"""
from datetime import datetime
import time
from dateutil.tz import tzutc, tzlocal

def convert_to_local_timestamp(date: str) -> int:
    """Convert to unix timestamp from date string"""
    generated_utc_date = datetime.fromisoformat(date)
    generated_utc_date = generated_utc_date.replace(tzinfo=tzutc())

    generated_local_date = generated_utc_date.astimezone(tzlocal())

    return int(time.mktime(generated_local_date.timetuple()))
