import configparser
import os

def get_setting_cfg(): 
    config = configparser.ConfigParser()
    try:
        config.read(['./conf/config.ini', './conf/custom.ini'])
    except:
        config.read('./conf/config.ini')
    return config


def get_api_key(bot_name=''):
    config = get_setting_cfg()
    if bot_name:
        return config.get(bot_name, 'token')
    else:
        return config.get('discord', 'token')