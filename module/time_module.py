from module.get_cfg import get_setting_cfg
from datetime import timezone, timedelta, datetime
from dateutil.parser import parse
import pandas as pd

def str_to_datetime(time_str, time_zone=get_setting_cfg().getint('common', 'timezone')):
    dt = parse(time_str)
    local_dt = dt.astimezone(timezone(timedelta(hours=time_zone)))
    return local_dt

def str_to_ts(time_str):
    return parse(time_str).timestamp()

def np_dt_to_dt(np_dt, time_zone=get_setting_cfg().getint('common', 'timezone')):
    return (pd.Timestamp(np_dt).to_pydatetime().astimezone(timezone(timedelta(hours=time_zone)))) + timedelta(hours=time_zone)
