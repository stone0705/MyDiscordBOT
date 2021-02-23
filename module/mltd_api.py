import json
import requests
import io
import os
import threading
import re
from time import strftime, sleep, time
from module.get_cfg import get_setting_cfg
from module.log_handler import get_file_and_stream_logger
from module.time_module import str_to_datetime, str_to_ts
from datetime import datetime, timezone

api_url = 'https://api.matsurihi.me/mltd/v1'

logger = get_file_and_stream_logger('discord.mltd_api')

def get_monitor_rank():
    return get_setting_cfg().get('monitor', 'monitor_rank').split(',')

def validate_event_id(event_id):
    pattern = '\d{1,}'
    if not re.match(pattern, event_id):
        raise Exception('event_id not match right pattern')

def get_json(file_path):
    with io.open(file_path, encoding='utf8') as f:
        return json.load(f)

def get_event_list(): 
    return get_json(get_setting_cfg().get('path', 'event_list'))

def get_event_id(event_name):
    event_list = get_event_list()
    for event in event_list:
        if event['name'] == event_name:
            return str(event['id'])
    return None

def get_last_event_id():
    event_list = get_event_list()
    return str(event_list[-1]['id'])

def get_event_info(event_id):
    json_path = get_setting_cfg().get('path', 'event_info')
    info = get_json(json_path)[event_id]
    for key in info['schedule']:
        info['schedule'][key] = str_to_datetime(info['schedule'][key])
    return info

def is_event_has_rank(event_id):
    return get_event_info(event_id)['type'] in [3, 4, 11]

def get_last_rank(event_id):
    if not is_event_has_rank(event_id): return None
    json_path = get_setting_cfg().get('path', 'event_rank')
    data = get_json(json_path)
    rank_list = {rank : data[event_id][rank][-1] for rank in data[event_id]}
    for rank in rank_list:
        rank_list[rank]['summaryTime'] = str_to_datetime(rank_list[rank]['summaryTime'])
    return rank_list
    
def calculate_speed(event_id, interval):
    if not is_event_has_rank(event_id): return None
    json_path = get_setting_cfg().get('path', 'event_rank')
    data = get_json(json_path)
    speed_dict = {}
    for rank in data[event_id]:
        if len(data[event_id][rank]) >= 2:
            now_score = data[event_id][rank][-1]['score']
            last_score = data[event_id][rank][-2]['score']
            now_time = str_to_ts(data[event_id][rank][-1]['summaryTime'])
            last_time = str_to_ts(data[event_id][rank][-2]['summaryTime'])
            speed = (now_score - last_score) / (now_time - last_time)
        else:
            speed_dict[rank] = speed = 0
        if interval == 'hour':
            speed_dict[rank] = speed * 3600
        elif interval == 'half_hour':
            speed_dict[rank] = speed * 1800
        elif interval == 'quarter_hour':
            speed_dict[rank] = speed * 900
        elif interval == 'min':
            speed_dict[rank] = speed * 60
    return speed_dict

def calculate_remaining_time(event_id):
    info = get_event_info(event_id)
    end_time = info['schedule']['endDate'].replace(tzinfo=timezone.utc)
    now_time = datetime.now().replace(tzinfo=timezone.utc)
    return (end_time - now_time).total_seconds()

def save_event_list():
    json_path = get_setting_cfg().get('path', 'event_list')
    r = requests.get('{}/events'.format(api_url))
    if r.status_code != 200: raise Exception('get event list fail with code:{}'.format(r.status_code))
    event_list = r.json()
    with io.open(json_path, 'w+', encoding='utf8') as f:
        json.dump(event_list, f, ensure_ascii=False, indent=4)
    convert_list_to_info()

def convert_list_to_info():
    event_list = get_event_list()
    new_data = {}
    for event in event_list:
        new_data[event['id']] = event
    json_path = get_setting_cfg().get('path', 'event_info')
    with io.open(json_path, 'w+', encoding='utf8') as f:
        json.dump(new_data, f, ensure_ascii=False, indent=4)

def save_event_ranking(event_id):
    validate_event_id(event_id)
    rank_num_list = ','.join(get_monitor_rank())
    json_path = get_setting_cfg().get('path', 'event_rank')
    r = requests.get('{}/events/{}/rankings/logs/eventPoint/{}'.format(api_url, event_id, rank_num_list))
    if r.status_code != 200: raise Exception('get event rank fail with code:{}'.format(r.status_code))
    rank_list = r.json()
    new_rank_list = {}
    if os.path.exists(json_path):
        new_rank_list = get_json(json_path)
    new_rank_list[event_id] = {rank['rank'] : rank['data'] for rank in rank_list}
    with io.open(json_path, 'w+', encoding='utf8') as f:
        json.dump(new_rank_list, f, ensure_ascii=False, indent=4)

def save_event_info(event_id):
    validate_event_id(event_id)
    json_path = get_setting_cfg().get('path', 'event_info')
    r = requests.get('{}/events/{}'.format(api_url, event_id))
    if r.status_code != 200: raise Exception('get event info fail with code:{}'.format(r.status_code))
    info = r.json()
    info_list = {}
    if os.path.exists(json_path):
        info_list = get_json(json_path)
    info_list[event_id] = info
    with io.open(json_path, 'w+', encoding='utf8') as f:
        json.dump(info_list, f, ensure_ascii=False, indent=4)
