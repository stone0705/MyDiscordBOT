import numpy as np
import pandas as pd
import json
import module.mltd_api as mltd_api
from module.get_cfg import get_setting_cfg

def get_pandas_data(event_id, rank_num):
    json_path = get_setting_cfg().get('path', 'event_rank')
    with open(json_path) as f:
        rank_data = json.load(f)
    score_diff_list = []
    time_list = []
    for i in range(1, len(rank_data[event_id][rank_num])):
        rank = rank_data[event_id][rank_num]
        score_diff_list.append(rank[i]['score'] - rank[i-1]['score'])
        time_list.append(rank[i]['summaryTime'])
    return pd.Series(score_diff_list, index=time_list)

def get_data(event_id, rank_num):
    json_path = get_setting_cfg().get('path', 'event_rank')
    with open(json_path) as f:
        data = json.load(f)
    return [rank['score'] for rank in data[event_id][rank_num]]

def get_function_data(score_list, interval):
    train_x = []
    train_y = []
    for i in range(interval, len(score_list)):
        train_x.append(np.array([score_list[i - j - 1] for j in range(interval)]))
        train_y.append(score_list[i])
    return np.array(train_x), np.array(train_y)

