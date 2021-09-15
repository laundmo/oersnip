import datetime
import time


def environment():
    now = datetime.datetime.now()
    return {
        "TIME": now.strftime("%H:%M:%S"),
        "DATE": now.strftime("%Y-%m-%d"),
        "DATETIME": now.strftime("%Y-%m-%d %H:%M:%S"),
        "CTIME": time.ctime(),
    }
