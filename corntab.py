import module.mltd_api as mltd_api
import threading
import predict_module.predict as predict
from time import sleep
from datetime import datetime
from module.log_handler import get_file_and_stream_logger

logger = get_file_and_stream_logger('discord.corntab')

def save_data_job():
    while(True):
        if (int(datetime.now().strftime('%M')) % 10) == 8:
            mltd_api.save_event_list()
            event_id = mltd_api.get_last_event_id()
            mltd_api.save_event_ranking(event_id)
            info = mltd_api.get_event_info(event_id)
            event_type = info['type']
            logger.info('current event_id:{} type:{}'.format(event_id, event_type))
            if event_type in [3, 4, 11]:
                predict.thread_save_predictor(event_id)
            #save_event_info(event_id)
            logger.info('save mltd data complete')
            sleep(60)
        sleep(30)

def thread_save_data():
    job = threading.Thread(target=save_data_job)
    job.start()
    logger.info('start save mltd data job')

if __name__ == '__main__':
    mltd_api.save_event_list()