import discord
import os
from magnuswebserver import keep_alive
import discord,random,asyncio
from discord.ext import commands
from discord.ext import tasks, commands
import requests
import json

magnus = discord.Client()

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = "\"" + json_data[0]["q"] + "\" - " + json_data[0]["a"]
  return quote

# use client.event decorator to register an event. In the discord.py library, things are done with "call backs".

@magnus.event
async def on_ready(): 
  """Calls when the bot is ready for use"""
  await magnus.change_presence(activity=discord.Game(name="Chess"))
  sendmessage.start()
  sendmessage1.start()
  
  print("Bot has logged in as {0.user}".format(magnus))

@magnus.event
async def on_message(message):
  """Calls each time a message is received"""
  if message.author == magnus.user: # If the message is from the bot itself, do nothing.
    return

  if message.content.startswith("$himagnus"): # We use say that "$info" in a bot command for Carlsen Bot
    await message.channel.send("Hello! My name is Magnus Carlsen, and I'm here to explain the rules of this Discord Server! Please type \"$rules\" for more information!")

  if message.content.startswith("$rules"):
    await message.channel.send(" The rules are very simple: \n - Please be respectful. \n - Please follow Lagno's list of rules \n That's all!")

  if message.content.startswith("$merrychristmas"):
      await message.channel.send("Merry Christmas Everyone!")

@tasks.loop(seconds=196400)
async def sendmessage():
     channel = magnus.get_channel(890990298585497687)
     quote = get_quote()
     await channel.send(quote)

@tasks.loop(seconds=143200)
async def sendmessage1():
     channel = magnus.get_channel(905136842599432223)
     await channel.send("-puzzle", delete_after=10)


# Run the bot script (inside the parameter for the run() function we need to put our token for the bot (bot token))
keep_alive()


# We can use an "Environment Variable"
magnus_token = os.environ['magnus']
magnus.run(magnus_token)

# Setting `Playing ` status
# await bot.change_presence(activity=discord.Game(name="a game"))

# Setting `Streaming ` status
# await bot.change_presence(activity=discord.Streaming(name="My Stream", url=my_twitch_url))

# Setting `Listening ` status
# await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="a song"))

# Setting `Watching ` status
# await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="a movie"))


"""

@tasks.loop(seconds=40)  # How often the bot should change status, mine is set on every 40 seconds
async def changepresence():
    global x

    game = iter(
        [
            "Status 1",
            "Status 2",
            "Status 3",
            "Status 4",
            "Status 5?",
            "Status 6",
        ]
    )  # Every line above ^^ is one new status the bot can have
    for x in range(random.randint(1, 6)):  # Here you write the total of different status you have for the bot, I have 6 and that's why I have number 6 there. This makes it a 16.666% chance to change status every 40 second
        x = next(game)
    await bot.change_presence(activity=discord.Game(name=x))

"""

