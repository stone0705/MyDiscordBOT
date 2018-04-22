import discord
from discord.ext import commands
from discord.voice_client import VoiceClient

momoko = commands.Bot('!')


@momoko.event
async def on_ready():
    print('bot online')

@momoko.event
async def on_message(message):
    print(message.content)



momoko.run('NDM1MDg4ODAxMDQwMTcxMDA4.DbT_5g.o64wiVzlu638vIBmgIglmyQLIqs')
