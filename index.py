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

voice = None
songsList = []

def playSong():
  global voice
  global songsList

  if not voice.is_playing():
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
        ydl.download([songsList.pop(0)])
    
    for file in os.listdir("./"):
        if file.endswith("mp3"):
            os.rename(file, "song.mp3")
    voice.play(
        discord.FFmpegPCMAudio(source="song.mp3"))

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  global voice
  global songsList

  if message.author == client.user:
      return

  channel = message.channel
  if message.content.startswith('-play'):
    command = message.content.split()
    
    if(len(command)!=2):
      await message.channel.send('Digita o comando certo seu bocó')
    else:
      url = command[1]
      songsList.append(url)

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
      if voice == None:
        voice = await channel.connect()
      playSong()
#Stop
  elif (message.author.voice) and message.content.startswith('-stop') and channel.guild.voice_client.is_connected():
    await channel.send("Paro")
    channel.guild.voice_client.stop()
#Pause
  elif (message.author.voice) and message.content.startswith('-pause') and channel.guild.voice_client.is_playing():
    await channel.send("Musica pausada")
    channel.guild.voice_client.pause()
#Resume
  elif (message.author.voice) and message.content.startswith('-resume') and channel.guild.voice_client.is_paused():
    channel.guild.voice_client.resume()
#Leave
  elif (message.author.voice) and message.content.startswith('-leave'):
      voice = None
      await channel.send("Forte Abraço!!")
      await channel.guild.voice_client.disconnect()
  elif message.author.voice == None and message.content.startswith('-leave'):
      await channel.send("Tu não ta on no voice")
#Boobs
  #elif message.content.startswith('-sena'):
    


client.run(TOKEN)