import discord
import os
import requests

client = discord.Client()
TOKEN = AQUI VEM A COISA CERTA

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    channel = message.channel
    if ('sena') in message.content:
        await channel.send('Say hello!')

    if (message.author.voice) and message.content.startswith('sena'):
        channel = message.author.voice.channel
        await channel.connect()
    elif (message.author.voice) and message.content.startswith('-leave'):
        await message.voice_client.disconnect()
    elif message.author.voice == None:
        await channel.send("Tu não ta on no voice macaco")


client.run(TOKEN)