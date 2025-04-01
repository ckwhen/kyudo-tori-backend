from datetime import datetime
from zoneinfo import ZoneInfo
from compose import compose
from functools import partial

_tokyo_tz = ZoneInfo("Asia/Tokyo")
_utc_tz = ZoneInfo("UTC")
def _set_tz(d: datetime, tz):
    return d.replace(tzinfo=tz)
def _to_tz(d: datetime, tz):
    return d.astimezone(tz)

_pgsql_format = "%Y-%m-%d %H:%M:%S%z"
def _to_d_f(d: datetime, f: str):
    return d.strftime(f)

def convert_reiwa_to_ce_year(year: int):
    return 2019 + year - 1

def to_date(*agrs):
    return datetime(*agrs)

to_pgsql_format = partial(_to_d_f, f=_pgsql_format)

set_tokyo_tz = partial(_set_tz, tz=_tokyo_tz)

to_utc_tz = partial(_to_tz, tz=_utc_tz)

get_tokyo_pgsql_date = compose(
    to_pgsql_format,
    to_utc_tz,
    set_tokyo_tz,
    to_date
)

def get_annual_full_date(year: int, month: int, day: int):
    a = to_date(year, 4, 1)
    a = set_tokyo_tz(a)
    d = a.replace(month=month, day=day)
    d = d if a < d else d.replace(year=(year + 1))
    d = to_utc_tz(d)

    return to_pgsql_format(d)