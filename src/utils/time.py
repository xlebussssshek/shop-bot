from datetime import datetime


def now_human() -> str:
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
