import pickle, os, errno
import module.mltd_api as mltd_api
from statsmodels.tsa.arima_model import ARIMA
from pmdarima.arima import auto_arima

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
    save_dir = mkdir('./predictor_model/arima/{}'.format(event_type))
    with open(os.path.join(save_dir, '{}_{}.pkl'.format(event_id, rank_num)), 'wb+') as f:
        pickle.dump(predictor, f)


def load_predictor(event_id, rank_num):
    info = mltd_api.get_event_info(event_id)
    event_type = info['type']
    save_dir = './predictor_model/arima/{}'.format(event_type)
    try:
        with open(os.path.join(save_dir, '{}_{}.pkl'.format(event_id, rank_num)), 'rb') as f:
            return pickle.load(f)
    except:
        return None

def get_arima_predictor(series):
    order=(2,1,2)
    predictor = ARIMA(series, order=order)
    predictor = predictor.fit()
    return predictor

def get_auto_arima_preditctor(series):
    predictor = auto_arima(series)
    predictor.fit(series)
    return predictor