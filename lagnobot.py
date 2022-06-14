import discord 
import os 
import requests 
import json 
import random 
from replit import db
from requests.api import delete
from lagnowebserver import keep_alive 


client = discord.Client() 

words = ["position","best move", "excellent move", "checkmate", "zugzwang", "stalemate", "gambit"]

starter_encouragements = [
    "You guys are all great Chess players!",
    "That does sound like something I'll do",
    "The position sounds difficult!"
    "We need Stockfish at depth 27 for this problem."
    "The Evans gambit is my favorite!"
    "The London is definitely not my favourite"
    "Don't worry!"
    "I don't think that's the best move!"
]

if "responding" not in db.keys():
    db["responding"] = True

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
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Airthings Masters"))
    print("Bot has logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    """Calls each time a message is received"""
    if message.author == client.user: # If the message is from the bot itself, do nothing.
        return

    if message.content.startswith("$hilagno"): # We use say that "$info" in a bot command for Carlsen Bot
        await message.channel.send("Hello! I'm Kateryna Lagno, and I'm here to explain the rules of this Discord Server! Please type \"$rules\" for more information!")

    msg = message.content # abbreviate the "message.content" part to msg for easy reference

    if message.content.startswith("$rules"):
        await message.channel.send(" Be low is a list of Boston University Chess Club Rules: \n \n 1. Be respectful to one another. \n 2. Do not argue with administrators and moderators. \n 3. Do not spam text or voice channels. \n 4. Avoid controversial topics that may be sensitive.\
             \n 5. No advertising or selling goods. \n 6. No raiding of this server \n 7. Do not post anything that’s not safe for work, school, or family. \n \n Please follow the rules above! Thanks! ")

    if db["responding"] == True:
        options = starter_encouragements # intialize encouragement options at the start (only three from the initial list)
        if "encouragements" in db.keys():
            options += db["encouragements"]


        if any(word in msg for word in words):
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
    
    if message.content.startswith("$merrychristmas"):
      await message.channel.send("Merry Christmas Everyone!")

keep_alive()

token = os.environ['token_lagno']
client.run(token)




