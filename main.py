##### IMPORTS #####
import random

import discord
from discord.ext import commands

from keep_alive import  keep_alive

##### GLOBALS #####
TOKEN = 'YOUR_TOKEN_HERE'
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
		#don't trigger on messages sent by this bot
		if message.author == client.user:
			return
		
		#ignore messages containing '!' to prevent triggering on commands
		if CMD in message.content:
			return

		#always convert to lower case for convenience in the checks below
		lowerContent = message.content.lower()

		for x in TRIGGERS:
			if x in lowerContent:
				await message.channel.send( random.choice(QUOTES) )
				break

##### CORE #####
keep_alive()
client.run(TOKEN)
