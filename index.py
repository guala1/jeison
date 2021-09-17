import discord
import os
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

    if ('sena') in message.content:
        channel = message.channel
        await channel.send('Say hello!')
           
    if (message.author.voice) and message.content.startswith('sena'):
        channel = message.author.voice.channel
        await channel.connect()
    else:
        await message.send("Tu não ta on no voice macaco")
        
    if (message.author.voice) and message.content.startswith('-leave'):
        await message.voice_client.disconnect()
    else:
        await message.send("Tu não ta on no voice macaco")
        


client.run(TOKEN)