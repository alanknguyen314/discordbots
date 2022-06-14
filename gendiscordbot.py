import discord # Discord dependency for discord Bot
import os # Os for .env files and environment variables 
import requests # For request data from API (for the quotes)
import json # For data manipulation from API (for the quotes)
import random # For printing random encouragement messages
from replit import db
from requests.api import delete
from discordbotwebserver import keep_alive # import webserver name and function


client = discord.Client() # Intialize Discord Client Object

sad_words = ["sad","depressed", "unhappy", "angry", "miserable", "misery", "depressing", "kms"]

starter_encouragements = [
    "Cheer up!",
    "Hang in there.",
    "You are a great person!"
    "Don't worry!"
]

# Responde only if True
if "responding" not in db.keys():
    db["responding"] = True

def get_quote():
    """Helper function that returns a quote from zenquotes.io and format it."""
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]["q"] + " - " + json_data[0]["a"]
    return quote

def update_encouragements(encouraging_msg):
    """Helper function that use database from Replit to add an encouragement message"""
    if "encouragements" in db.keys():
        encouragements = db["encouragements"]
        encouragements.append(encouraging_msg)
        db["encouragements"] = encouragements
    else:
        db["encouragements"] = [encouraging_msg]

def delete_encouragements(index):
    """Helper function that use database from Replit to remove an encouragement message"""
    encouragements = db["encouragements"]
    if len(encouragements) > index:
        del encouragements[index]
        db["encouragements"] = encouragements


# use client.event decorator to register an event. In the discord.py library, things are done with "call backs". 
@client.event
async def on_ready(): 
    """Calls when the bot is ready for use"""
  
    print("Bot has logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    """Calls each time a message is received"""
    if message.author == client.user: # If the message is from the bot itself, do nothing.
        return

    if message.content.startswith("$hello"): # We use say that "$info" in a bot command for Carlsen Bot
        await message.channel.send("Hello! I'm a bot, and I'm here to explain the rules of this Discord Server! \
        \ Please type \"$rules\" for more information!")

    msg = message.content # abbreviate the "message.content" part to msg for easy reference

    if message.content.startswith("$rules"):
        await message.channel.send(" 1. Be respectful to one another. \n 2. Do not argue with administrators and moderators. \n 3. Do not spam text or voice channels. \n 4. Avoid controversial topics that may be sensitive.\
             \n 5. No advertising or selling goods. \n 6. No raiding of this server \n 7. Do not post anything that’s not safe for work, school, or family. \n Thanks for reading! Please follow the rules above! ")

    if message.content.startswith("$quote"):
        quote = get_quote()
        await message.channel.send(quote)

    if db["responding"] == True:
        options = starter_encouragements # intialize encouragement options at the start (only three from the initial list)
        if "encouragements" in db.keys():
            options += db["encouragements"]


        if any(word in msg for word in sad_words):
            # await message.channel.send(random.choice(starter_encouragements)) -> Only pick from initial list starter_encouragements
            await message.channel.send(random.choice(options)) # Pick from Database

    if msg.startswith("$new"):
        encouraging_msg = msg.split("$new ", 1)[1] # only add what comes after the "$new" part and not $new itself. $new is only a trigger comand.
        update_encouragements(encouraging_msg)
        await message.channel.send("New encouraging message added.")

    if msg.startswith("$del"):
        encouragements = []
        if "encouragements" in db.keys():
            index = int(msg.split("$del", 1)[1])
            delete_encouragements(index)
            encouragements = db["encouragements"]
        await message.channel.send(encouragements)

    if msg.startswith("$list"):
        encouragements = []
        if "encouragements" in db.keys():
            encouragements = db["encouragements"]
        await message.channel.send(encouragements)

    if msg.startswith("$responding"):
        value = msg.split("responding ", 1)[1]
        
        if value.lower() == "true":
            db["responding"] = True
            await message.channel.send("Responding is On")

        elif value.lower() == "false":
            db["responding"] = False
            await message.channel.send("Responding is Off")

# USE REPLIT.IO Database to store:

# Run the bot script (inside the parameter for the run() function we need to put our token for the bot (bot token))
# We can use an "Environment Variable" to store values that viewers of the code cannot see explicitly.

# Initialize web server:
keep_alive()

# Copy webserver URL to UptimeRobot for it to ping the server https://Fabi-Bot.alanknguyen314.repl.co

token = os.environ['token_fabi'] #'client_token' is the environment variable that represent the token of the bot. 
client.run(token)
