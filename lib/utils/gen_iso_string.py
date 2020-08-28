from datetime import datetime


def gen_iso_string(date=None):
    if not date:
        date = datetime.utcnow()

    return date.strftime("%Y-%m-%dT%H:%M:%SZ")
