import gplearn.genetic as gp
import pickle
import module.mltd_api as mltd_api
import predict_module.custom_function as cf
import os
import errno
import json
from module.get_cfg import get_setting_cfg


def mkdir(directory):
    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    return directory


def save_predictor(predictor, event_id, rank_num):
    info = mltd_api.get_event_info(event_id)
    event_type = info['type']
    save_dir = mkdir('./predictor_model/gp/{}'.format(event_type))
    with open(os.path.join(save_dir, '{}_{}.pkl'.format(event_id, rank_num)), 'wb+') as f:
        pickle.dump(predictor, f)


def load_predictor(event_id, rank_num):
    info = mltd_api.get_event_info(event_id)
    event_type = info['type']
    save_dir = './predictor_model/gp/{}'.format(event_type)
    try:
        with open(os.path.join(save_dir, '{}_{}.pkl'.format(event_id, rank_num)), 'rb') as f:
            return pickle.load(f)
    except:
        return None


def get_gp_parameter(parameter_name):
    json_path = get_setting_cfg().get('path', 'gp_parameter')
    core_num = get_setting_cfg().getint('GP', 'core_num')
    with open(json_path) as f:
        data = json.load(f)
    data[parameter_name]['predictor_parameter'].update({'n_jobs': core_num})
    data[parameter_name]['predictor_parameter'].update({'const_range': (data[parameter_name]['predictor_parameter'].pop(
        'min_const', -1), data[parameter_name]['predictor_parameter'].pop('max_const', 1))})
    return data[parameter_name]


def get_predictor(train_x, train_y, predictor_parameter_type=get_setting_cfg().get('GP', 'setting')):
    parameter = get_gp_parameter(predictor_parameter_type)
    mltd_predictor = gp.SymbolicRegressor(
        function_set=cf.get_custom_function_list(), **parameter['predictor_parameter'])
    return mltd_predictor.fit(train_x, train_y)
