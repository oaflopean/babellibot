# These are the dependecies. The bot depends on these to function, hence the name. Please do not change these unless your adding to them, because they can break the bot.
import discord
import asyncio
import requests
from flask_httpauth import HTTPBasicAuth
from discord.ext.commands import Bot
from discord.ext import commands
import platform
import markovify
import math
# Here you can modify the bot's prefix and description and wether it sends help in direct messages or not.
client = Bot(description="Babelli bot", command_prefix=".", pm_help = False)


# This is what happens everytime the bot launches. In this case, it prints information like server count, user count the bot is connected to, and the bot id in the console.
# Do not mess with it because the bot can break, if you wish to do so, please consult me or someone trusted.
@client.event
async def on_ready():
    print("Yep")
# This is a basic example of a call and response command. You tell it do "this" and it does it.
@client.command()
async def ping(*args):

    await client.say(":ping_pong: Pong!")
    await asyncio.sleep(3)
    await client.send(":warning: This bot was created by **CaesarNaples2**")

@client.command()
async def test(ctx, arg):
    await ctx.send(arg)

@client.command()
async def babelli(ctx,arg, arg2):
        msg=""
        key=arg
        url="http://oaflopean.pythonanywhere.com/?key="+key
        data=requests.post(url, auth=('oaflopean', 'babellibot'))

        if len(data.content.decode("utf-8"))==0:
            url = "http://oaflopean.pythonanywhere.com/?key=" + key+"?titles=yes"
            data = requests.post(url, auth=('oaflopean', 'babellibot'))
        text_model = markovify.Text(data.content.decode("utf-8"))
        for i in range(int(arg2)):
            try:

                try:
                    msg = msg + " " + text_model.make_sentence() + " "
                except TypeError:
                    msg = msg + " " + text_model.make_sentence() + " "
            except TypeError:
                continue
        if len(msg)==0:
            await ctx.send("Sorry! Try more options.")
        else:
            chunks, chunk_size = len(msg), len(msg) / (len(msg)/1995)
            list=[msg[i:i + int(chunk_size)] for i in range(0, chunks, int(chunk_size))]
            for msg_pt in list:
                await ctx.send(msg_pt)


client.run('NjE5MDQzNDk3NDcwNTkwOTk3.XXCffA.lYWvnSn6KdlFztKtGfikHUR9EHA')

# Basic Bot was created by Habchy#1665
# Please join this Discord server if you need help: https://discord.gg/FNNNgqb
# Please modify the parts of the code where it asks you to. Example: The Prefix or The Bot Token
# This is by no means a full bot, it's more of a starter to show you what the python language can do in Discord.
# Thank you for using this and don't forget to star my repo on GitHub! [Repo Link: https://github.com/Habchy/BasicBot]

# The help command is currently set to be not be Direct Messaged.
# If you would like to change that, change "pm_help = False" to "pm_help = True" on line 9.