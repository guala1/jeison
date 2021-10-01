import discord
#from discord.ext import commands
#from discord import FFmpegPCMAudio
#import json
#import requests
import youtube_dl
import os

import requests, json
import pyimgur

from math import *

#from decouple import config
from random import randint
import matplotlib.pyplot as plt

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

def getPhoto(name, url):
  # https://i.imgur.com/
  # Open HTML File
  html = open(name+'.html', 'r').read()

  urls=[]
  i = 0
  current = ''
  addElement = False
  while i<len(html):
      if (html[i]=='h' and i+len('ref="'+url)<len(html) and html[i:i+len('ref="'+url)+1]=='href="'+url):
          addElement = True
          i += len('ref="'+url)
      elif addElement and html[i]!='"':
          current+=html[i]
      elif addElement and html[i]=='"':
        if len(current) > 0:
          urls.append(url+current)
        addElement = False
        current=''
      i += 1
  return urls

  #======================================

client = discord.Client()
TOKEN = os.environ['TOKEN'] # config('TOKEN') -> se estiver no computador

voice = None
songsList = []

#https://www.instagram.com/p/ - MUSCLE
#https://youtu.be/ - MUSCLE
#https://gfycat.com/ - MUSCLE E BOOBS
#https://redgifs.com/watch/ - BOOBS
boobsList = getPhoto('imgStorage/BOOBS', 'https://i.imgur.com/')
muscleList = getPhoto('imgStorage/MUSCLE', 'https://i.imgur.com/') + getPhoto('imgStorage/MUSCLE', 'https://youtu.be/') + getPhoto('imgStorage/MUSCLE', 'https://www.instagram.com/p/')
photoList = [boobsList, muscleList]

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
  elif message.content.startswith('-sena'):
    rand = randint(0,1)
    currentList = photoList[rand]
    if rand == 0:
      photo = currentList[randint(0,len(boobsList)-1)]
    else:
      photo = currentList[randint(0,len(muscleList)-1)]
    await channel.send(photo)
  #elif message.content.startswith('-sena'):
# Plotagem
  elif message.content.startswith('-plota '):
    ent = message.content.split()
    funcs = []
    x = []
    y = []
    for index in range(1, len(ent)):
        p = ent[index].split(',')
        px = float(p[0][1:])
        py = float(p[1][:len(p[1])-1])
        x.append(px)
        y.append(py)
    #Envia uma equação do 1 grau
    for i in range(len(x)-1):
        funcs.append(f'y = {(y[i+1]-y[i])}/{(x[i+1]-x[i])}*x + ({(-(y[i+1]-y[i])*x[i])+(y[i]*(x[i+1]-x[i]))}/{(x[i+1]-x[i])})')
    for i in funcs:
      await channel.send(i)
    
    plt.plot(x,y)

    plt.xlabel('x values')
    plt.ylabel('y values')
    plt.title('plotted x and y values')
    plt.legend(['line 1'])

    plt.savefig('plotting/plot.png', dpi=300, bbox_inches='tight')
    plt.clf() 

    client_id = '298648bf6f7a17b'
    path = 'plotting/plot.png'
    im = pyimgur.Imgur(client_id)
    upload_image = im.upload_image(path, title='Plot')

    os.remove('plotting/plot.png')

    await channel.send(upload_image.link)

  # Realiza Calculo
  elif message.content.startswith('-uga '):
      calc = message.content[len('-uga '):]
      await channel.send(eval(calc))

client.run(TOKEN)