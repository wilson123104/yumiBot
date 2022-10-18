from datetime import datetime,timezone,timedelta
def getNowTime() -> datetime:
    dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
    return dt1.astimezone(timezone(timedelta(hours=8)))