import discord
from discord.ext import commands
from discord.voice_client import VoiceClient
from module.get_cfg import get_api_key
from corntab import thread_save_data
momoko = commands.Bot(command_prefix=commands.when_mentioned_or('!'))


@momoko.event
async def on_ready():
    print('bot online')


thread_save_data()
momoko.load_extension('mltd_bot')
momoko.run(get_api_key())
