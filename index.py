import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import json
import requests
from decouple import config

client = discord.Client()
TOKEN = config('TOKEN')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    channel = message.channel
    if ('sena') in message.content:
        await channel.send('fat and gay')



#Play
    if (message.author.voice) and message.content.startswith('-join'):
        channel = message.author.voice.channel
        voice = await channel.connect()
        voice.play(discord.FFmpegPCMAudio(executable=r"C:\Users\nigga\Documents\GitJeison\jeison\ffmpeg\bau\ffmpeg.exe", source="teste.wav"))
#       source = FFmpegPCMAudio("teste.wav")
#       player = voice.play(source)
#Leave
    elif (message.author.voice) and message.content.startswith('-leave'):
        await channel.send("Forte Abraço!!")
        await channel.guild.voice_client.disconnect()
    elif message.author.voice == None:
        await channel.send("Tu não ta on no voice macaco")


client.run(TOKEN)