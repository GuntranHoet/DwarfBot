import random

import discord
from discord.ext import commands

##### GLOBALS #####
TOKEN = 'YOUR_TOKEN'
CMD = '!'
QUOTES = open('quotes.txt').read().splitlines()
TRIGGERS = open('triggers.txt').read().splitlines()

##### DISCORD #####
client = commands.Bot(command_prefix = CMD)

# READY #
@client.event
async def on_ready():
    print('DwarfBot ready!')

# ON MESSAGE #
@client.event
async def on_message(message):
		if message.author == client.user:
			return
		
		if CMD in message.content:
			return

		lowerContent = message.content.lower()

		for x in TRIGGERS:
			if x in lowerContent:
				await message.channel.send( random.choice(QUOTES) )
				break

##### CORE #####
client.run(TOKEN)
