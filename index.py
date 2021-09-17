import discord
import os
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
        await message.channel.send('.play https://soundcloud.com/user-363769748/friendzone')
        
    if ('Sena') in message.content:
        await message.channel.send('.play https://soundcloud.com/user-363769748/friendzone')

client.run(TOKEN)