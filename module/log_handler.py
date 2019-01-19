import logging
import module.get_cfg as get_cfg
import os
import errno
from logging import handlers

formatter = logging.Formatter(
    '%(asctime)s %(levelname)s %(message)s')


def get_mylogger(log_name):
    config = get_cfg.get_setting_cfg()
    log_path = config.get('log', 'log_path')
    log_file = config.get('log', log_name)
    is_debug = config.getboolean('log', 'is_debug')
    log_file = os.path.join(log_path, log_file)
    my_logger = logging.getLogger(log_name)
    level = logging.INFO
    if is_debug:
        level = logging.DEBUG
    my_logger.setLevel(level)
    return my_logger, level, log_file


def set_stream_handler(my_logger, level):
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    console.setLevel(level)
    my_logger.addHandler(console)


def set_file_handler(my_logger, level, file_name):
    file_hander = logging.handlers.RotatingFileHandler(file_name)
    file_hander.setFormatter(formatter)
    file_hander.setLevel(level)
    my_logger.addHandler(file_hander)


def get_file_logger(log_name):
    my_logger, level, log_file = get_mylogger(log_name)
    set_file_handler(my_logger, level, log_file)
    return my_logger


def get_stream_logger(log_name):
    my_logger, level, _ = get_mylogger(log_name)
    set_stream_handler(my_logger, level)
    return my_logger


def get_file_and_stream_logger(log_name):
    my_logger, level, log_file = get_mylogger(log_name)
    set_stream_handler(my_logger, level)
    set_file_handler(my_logger, level, log_file)
    return my_logger