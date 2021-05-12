import discord
import os
import requests  # allows our code to make HTTP requests from API 
import json  # API returns json, making it easier to work with
import random
from replit import db  # allows our code to use Repl.it database

client = discord.Client()  # connection to discord

sad_words = ["sad", "depressed", "unhappy", "angry", "miserable"]
starter_encouragments = ["Cheer up!", "Hang in there!", "You are a great person / bot!"]
my_secret = os.environ['TOKEN']

def get_quote():
  response = requests.get("Http://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " - " + json_data[0]['a']
  return(quote)

def update_encouragments(encouraging_message):  # accepts an encouraging message as argument 
  if "encouragments" in db.keys():
    encouragments = db["encouragments"]
    encouragments.append(encouraging_message)
    db["encouragments"] = encouragments
  else:
    db["encouragments"] = [encouraging_message]

def delete_encouragment(index):
  encouragments = db["encouragments"]
  if len(encouragments) > index:
    del encouragments[index]
  db["encouragments"] = encouragments

@client.event  # done with a callback
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  
  msg = message.content

  if msg.startswith("$inspire"):
    quote = get_quote()
    await message.channel.send(quote)

  if db["responding"]:
    options = starter_encouragements
    if "encouragements" in db.keys():
      options = options + db["encouragements"]

    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))

  if msg.startswith("$new"):
    encouraging_message = msg.split("$new ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added.")

  if msg.startswith("$del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("$del",1)[1])
      delete_encouragment(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  if msg.startswith("$list"):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)
    
  if msg.startswith("$responding"):
    value = msg.split("$responding ",1)[1]

    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Responding is on.")
    else:
      db["responding"] = False
      await message.channel.send("Responding is off.")

keepAlive()  # helps keep the server alive for one hour after the bot "shuts down"
client.run(os.getenv("TOKEN"))
