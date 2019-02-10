import module.mltd_api as mltd_api
import discord
import predict_module.predict as predict
from datetime import timezone
from discord.ext import commands
from time import strftime
from module.get_cfg import get_setting_cfg

def get_info_str(event_id):
    info = mltd_api.get_event_info(event_id)
    begin = info['schedule']['beginDate'].strftime("%Y-%m-%d %H:%M:%S")
    end = info['schedule']['endDate'].strftime("%Y-%m-%d %H:%M:%S")
    return '活動名稱:{} 開始時間:{} 結束時間:{}'.format(info['name'], begin, end)

def get_speed_str(event_id):
    speed = mltd_api.calculate_speed(event_id, 'hour')
    return_str = ''
    if speed:
        for key in speed:
            return_str += '{}名 時速:{}\n'.format(key, speed[key])
    else:
        return_str = '這個活動不是排名活動'
    return return_str

def get_ranking_status(event_id):
    ranking = mltd_api.get_last_rank(event_id)
    return_str = ''
    if ranking:
        for key in ranking:
            score = ranking[key]['score']
            update_time = ranking[key]['summaryTime'].strftime("%Y-%m-%d %H:%M:%S")
            return_str += '{}名 分數:{} 更新時間:{}\n'.format(key, score, update_time)
    else:
        return_str = '這個活動不是排名活動'
    return return_str

def get_remaining_status(event_id):
    remaining_time = mltd_api.calculate_remaining_time(event_id)
    return_str = ''
    if remaining_time < 0:
        return_str = '活動已經結束了'
    else:
        hours = int(remaining_time / 3600)
        mins = int((remaining_time - (hours * 3600)) / 60)
        secs = int(remaining_time - (hours * 3600) - (mins * 60))
        return_str = '活動剩下 {} 小時 {} 分 {} 秒'.format(hours, mins, secs)
    return return_str

def get_predict_status(event_id):
    return_str = ''
    rank_list = mltd_api.get_monitor_rank()
    n_step = get_setting_cfg().getint('ARIMA', 'n_step')
    for rank in rank_list:
        predict_value, predictor_info = predict.predict(event_id, rank, n_step)
        if predict_value:
            return_str += '下{}個時間點{}名的預測分數\n(預測器根據{}時間點 分數變動幅度:{}產生):\n{}\n'.format(n_step, 
                rank, 
                predictor_info['last_time'].strftime("%Y-%m-%d %H:%M:%S"), 
                predictor_info['last_score'], 
                ', '.join([str(value) for value in predict_value]))
    if return_str == '':
        return_str = '無法取得預測值，預測器尚未生成'
    return return_str


class mltd_bot(object):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='速度', aliases=['時速'])
    async def get_speed(self):
        event_id = mltd_api.get_last_event_id()
        info_str = get_info_str(event_id)
        speed = get_speed_str(event_id)
        await self.bot.say('{}\n{}'.format(info_str, speed))

    @commands.command(name='排行', aliases=['排名'])
    async def get_rank(self):
        event_id = mltd_api.get_last_event_id()
        info_str = get_info_str(event_id)
        r = get_ranking_status(event_id)
        await self.bot.say('{}\n{}'.format(info_str, r))

    @commands.command(name='剩下時間', aliases=['剩下', '剩餘', '還多久', '多久'])
    async def get_remaining_time(self):
        event_id = mltd_api.get_last_event_id()
        info_str = get_info_str(event_id)
        r = get_remaining_status(event_id)
        await self.bot.say('{}\n{}'.format(info_str, r))

    @commands.command(name='預測', aliases=['未來'])
    async def get_predict_rank(self):
        event_id = mltd_api.get_last_event_id()
        info_str = get_info_str(event_id)
        r = get_predict_status(event_id)
        await self.bot.say('{}\n{}'.format(info_str, r))
    

def setup(bot):
    print('load mltd bot')
    bot.add_cog(mltd_bot(bot))

if __name__ == '__main__':
    event_id = mltd_api.get_last_event_id()
    info_str = get_info_str("33")
    speed = get_speed_str("33")
    print(speed)