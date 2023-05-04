##### IMPORTS #####
import os
import random
import time
import asyncio

import discord
from discord.ext import commands

from keep_alive import keep_alive

##### GLOBALS #####
TOKEN = 'YOUR_TOKEN_HERE' # <<---------------- ENTER YOUR TOKEN HERE ------------- <<
CMD = '!'
ALLOW_TTS = False
QUOTES = open('data/quotes.txt').read().splitlines()
TRIGGERS = open('data/triggers.txt').read().splitlines()

DEFAULT_ACTIVITY = discord.Activity(type=discord.ActivityType.playing,
                                    name="Deep Rock Galacitc")

##### HELPERS (cooldown) #####
COOLDOWN_SEC = 60 * 5
LAST_COOLDOWN_EXPIRE_TIME = 0


def IsCooldownFinished():
    now = int(time.time())

    ok = (now >= LAST_COOLDOWN_EXPIRE_TIME)
    print(">", "now:", now, "cooldown_expire:", LAST_COOLDOWN_EXPIRE_TIME,
          "dif:", now - LAST_COOLDOWN_EXPIRE_TIME, "ok:", ok)
    return ok


def BeginCooldown():
    global LAST_COOLDOWN_EXPIRE_TIME
    LAST_COOLDOWN_EXPIRE_TIME = int(time.time()) + COOLDOWN_SEC


def GetCooldownTminusSec():
    return LAST_COOLDOWN_EXPIRE_TIME - int(time.time())


##### DISCORD #####
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=CMD, intents=intents)


# READY #
@bot.event
async def on_ready():
    print('DwarfBot ready!')
    await bot.change_presence(activity=DEFAULT_ACTIVITY,
                              status=discord.Status.online)


# ON MESSAGE #
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if not IsCooldownFinished():
        return

    lowerContent = message.content.lower()
    print("trigger msg: " + message.content)

    for x in TRIGGERS:
        if x in lowerContent:
            print("creating message...")
            await message.channel.send(random.choice(QUOTES), tts=ALLOW_TTS)
            BeginCooldown()
            bot.loop.create_task(cooldown_update())
            break


##### CUSTOM (discord) #####
async def cooldown_update():
    await bot.wait_until_ready()
    while not bot.is_closed():
        if IsCooldownFinished():
            await bot.change_presence(activity=DEFAULT_ACTIVITY,
                                      status=discord.Status.online)
            return
        else:
            tminus = GetCooldownTminusSec()
            await bot.change_presence(activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=f"cooldown: {tminus}s"),
                                      status=discord.Status.do_not_disturb)

            #sleep and redo
            await asyncio.sleep(5)


##### CORE #####
keep_alive()
bot.run(TOKEN)
