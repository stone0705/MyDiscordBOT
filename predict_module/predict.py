import predict_module.arima_predictor as arima_predictor
import predict_module.data_module as data_module
import module.mltd_api as mltd_api
from module.log_handler import get_file_and_stream_logger

logger = get_file_and_stream_logger('discord.predict')

def save_predictor(event_id, rank_num):
    data = data_module.get_pandas_data(event_id, rank_num)
    if len(data) > 6:
        predictor = arima_predictor.get_auto_arima_preditctor(data)
        arima_predictor.save_predictor(predictor, event_id, rank_num)
        logger.info('event:{} rank:{} save auto arima model DONE'.format(event_id, rank_num))
    else:
        logger.info('sample is too less for create predictor')
    

def thread_save_predictor(event_id):
    for rank_num in mltd_api.get_mltd_api_config()['monitor_rank']:
        save_predictor(event_id, rank_num)

def predict(event_id, rank_num, n_step):
    predictor = arima_predictor.load_predictor(event_id, rank_num)
    if predictor:
        predict_values = predictor.predict(n_step)
        last_value = mltd_api.get_last_rank(event_id)[rank_num]['score']
        sum_list = []
        for i in range(len(predict_values)):
            sum_list.append(sum(predict_values[0: i+1]))
        sum_list = [int(last_value + diff) for diff in sum_list]
        return sum_list, predictor.predictor_info
    else:
        return None