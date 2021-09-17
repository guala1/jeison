import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import json
import requests
import youtube_dl
import os

from decouple import config

client = discord.Client()
TOKEN = os.environ['TOKEN'] # config('TOKEN') -> se estiver no computador

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    channel = message.channel
    if '-play' in message.content:
        command = message.content.split()
        print(len(command)!=2)
        if(len(command)!=2):
          await message.channel.send('Digita o comando certo seu bocó')
        else:
          url = command[1]
          song_there = os.path.isfile("song.mp3")
          try:
              if song_there:
                  os.remove("song.mp3")
          except PermissionError:
              await channel.send(
                  "Wait for the current playing music to end or use the 'stop' command"
              )
              return

          channel = message.author.voice.channel
          voice = await channel.connect()

          ydl_opts = {
              'format':
              'bestaudio/best',
              'postprocessors': [{
                  'key': 'FFmpegExtractAudio',
                  'preferredcodec': 'mp3',
                  'preferredquality': '192',
              }],
          }
          with youtube_dl.YoutubeDL(ydl_opts) as ydl:
              ydl.download([url])
        
          for file in os.listdir("./"):
              if file.endswith("mp3"):
                  os.rename(file, "song.mp3")
          voice.play(
              discord.FFmpegPCMAudio(source="song.mp3"))


#Play
#     if (message.author.voice) and message.content.startswith('-join'):
#         channel = message.author.voice.channel
#         voice = await channel.connect()
#         voice.play(discord.FFmpegPCMAudio(executable="C:\\Users\\nigga\\Documents\\GitJeison\\jeison\\ffmpeg\\ffmpeg.exe", source="teste.mp3"))

#Leave
    elif (message.author.voice) and message.content.startswith('-leave'):
        await channel.send("Forte Abraço!!")
        await channel.guild.voice_client.disconnect()
    elif message.author.voice == None and message.content.startswith('-leave'):
        await channel.send("Tu não ta on no voice")

client.run(TOKEN)
