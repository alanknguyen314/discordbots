import discord
import os
import requests
import json
import random
from hikaruwebserver import keep_alive
from discord.ext import tasks, commands


bad_words = [
    "fuck",
    "n-word",
    "nigger",
    "cunt",
    "dick",
    "suck",
    "hentai",
    "porn",
    "asshole",
    "bastard",
    "shit",
    "slut",
    "f*ck",
    "fu*k",
    "anal",
    "bloody",
    "pussy",
    "fag",
    "damn",
    "cock",
    "coon",
    "boob",
    "blow job",
    "blowjob",
    "bitch",
    "biatch",
    "clitoris",
    "jizz",
    "twat",
    "whore"

]

responses = [
    "Chat, Please watch your profanity.",
    "Hey chat, please don't use those types of words here!",
    "Hey chat, no curses here!",
    "Language, chat",
    "Oh come on, chat! No profanity!",
    "Language.",
    "Look, chat, profanity is not allowed here.",
    "Look up the rules chat, no curses!",
    "Chat, stop being weird.",
    "I literally don't care but please don't curse.",
    "Not OK Chat, not OK."]


hikaru = discord.Client()

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]["q"] + " - " + json_data[0]["a"]
  return quote

@hikaru.event
async def on_ready():
  """Calls when the bot is ready for use"""
  await hikaru.change_presence(activity=discord.Streaming(name="Chess", url="https://www.twitch.tv/gmhikaru"))
  sendmessage.start()
  print("Bot has logged in as {0.user}".format(hikaru))

@hikaru.event
async def on_message(message):
  """Calls each time a message is received"""

  if message.author == hikaru.user:
    return

  if message.content.startswith("$hihikaru"):
    await message.channel.send("What's up man, it's GM Hikaru at your service! Please enter: \n \"$quote\" for a chess-related quote \n \"$rating\" for the most-to-date rating of the top 20 players!")

  if message.content.startswith("$quote"):

    quote = get_quote()

    await message.channel.send(quote)


  if any(word in ("".join(message.content.split(" "))).lower() for word in bad_words):

    await message.channel.send(random.choice(responses))

  if message.content.startswith("$merrychristmas"):
      await message.channel.send("Merry Christmas Everyone!")

@tasks.loop(seconds=240000)
async def sendmessage():
     channel = hikaru.get_channel(890990298585497687) #Insert channel here
     await channel.send("How are you guys doing today?", delete_after=60000)

keep_alive()

hikaru_token = os.environ['hikaru']
hikaru.run(hikaru_token)

