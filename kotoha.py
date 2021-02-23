import discord
import json
import os
from random import choice
from time import time, sleep
from discord.ext import commands
from module.get_cfg import get_api_key

kotoha = commands.Bot(command_prefix=commands.when_mentioned_or('!'))
interval = 7200
threshold = 4

def is_user_lock(user_id, interval):
    try:
        with open('./data/kotoha_lock.json')as f:
            data = json.load(f)
    except:
        data = {}
    finally:
        return data.get(user_id, {}).get('lock_time', 0) + interval > time()

def is_user_need_check(user_id, interval): 
    try:
        with open('./data/kotoha_lock.json')as f:
            data = json.load(f)
    except:
        data = {}
    finally:
        return data.get(user_id, {}).get('check_time', 0) + interval < time()

def set_user_checked(user_id, is_lock):
    try:
        with open('./data/kotoha_lock.json')as f:
            data = json.load(f)
    except :
        data = {}
    finally:
        print(data)
        data[user_id] = {
            'check_time': int(time())
        }
        if is_lock:
            data[user_id]['lock_time'] = int(time())
        with open('./data/kotoha_lock.json', 'w')as f:
            json.dump(data, f, indent=4)

def roll_dice(user_status):
    tmp = user_status.split('d')
    dice_num = int(tmp[0])
    dice_power = int(tmp[1])
    total = 0
    for _ in range(dice_num):
        total += choice(range(1, dice_power + 1))
    return total

def get_user_status(author_id):
    return '1d6'

async def start_check(message, threshold):
    user_id = str(message.author.id)
    user_status = get_user_status(user_id)
    await message.channel.send('{} 進行隱藏動圖判定 隱藏能力:{} 須達到{}才能不被琴葉發現'.format(message.author.name, user_status, threshold))
    sleep(0.5)
    total = roll_dice(user_status)
    await message.channel.send('{} 擲出 {}'.format(message.author.name, total))
    if total >= threshold:
        await message.channel.send('判定成功')
        set_user_checked(user_id, True)
        return True
    else:
        await message.channel.send('判定失敗')
        set_user_checked(user_id, True)
        return False

async def process_gif_msg(message):
    user_id = str(message.author.id)
    if any([attach for attach in message.attachments if 'gif' in str(attach).lower()]) or ('gif' in message.content.lower() and 'http' in message.content.lower()):
        print(is_user_need_check(user_id, interval))
        if is_user_need_check(user_id, interval):
            await start_check(message, threshold)
        print(is_user_lock(user_id, interval))
        if is_user_lock(user_id, interval):
            await message.delete()
            await message.channel.send('聊天室禁止宗仁貼動圖')

@kotoha.event
async def on_ready():
    ch = kotoha.get_channel(279591402046750720)
    messages = await ch.history(limit=123).flatten()
    for message in messages:
        if message.author.id == 96205233134260224:
            if any([attach for attach in message.attachments if 'gif' in str(attach).lower()]) or ('gif' in message.content.lower() and 'http' in message.content.lower()):
                #await process_gif_msg(message)
                pass
    print('bot online')

@kotoha.event
async def on_message(message):
    if message.author.id == 96205233134260224:
        await process_gif_msg(message)

kotoha.run(get_api_key('kotoha'))