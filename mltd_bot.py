import module.mltd_api as mltd_api
import discord
from datetime import timezone
from discord.ext import commands
from time import strftime

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

class mltd_bot(object):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='速度', aliases=['時速'])
    async def get_speed(self):
        event_id = mltd_api.get_last_event_id()
        info_str = get_info_str(event_id)
        speed = get_speed_str(event_id)
        await self.bot.say('{}\n{}'.format(info_str, speed))
    

def setup(bot):
    print('load mltd bot')
    bot.add_cog(mltd_bot(bot))

if __name__ == '__main__':
    event_id = mltd_api.get_last_event_id()
    info_str = get_info_str("33")
    speed = get_speed_str("33")
    print(speed)