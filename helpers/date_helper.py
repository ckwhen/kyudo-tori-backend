from datetime import datetime
from zoneinfo import ZoneInfo

tokyo_tz = ZoneInfo("Asia/Tokyo")
utc_tz = ZoneInfo("UTC")

pgsql_format = "%Y-%m-%d %H:%M:%S%z"

def convert_reiwa_to_ce_year(year: int):
    return 2019 + year - 1

def get_annual_full_date(year: int, month: int, day: int):
    a = datetime(year, 4, 1, tzinfo=tokyo_tz)
    d = a.replace(month=month, day=day)
    return d if a < d else d.replace(year=(year + 1))