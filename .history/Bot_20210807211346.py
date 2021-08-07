from fileinput import filename
from discord.channel import VoiceChannel
from discord.ext import commands
import discord
import asyncio
from PIL import ImageSequence, Image, ImageChops
import requests
from PIL import Image, ImageDraw, ImageOps, ImageFont
import numpy as np
import os
from dotenv import load_dotenv

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=',',case_insensitive=True, intents=intents)

@bot.event
async def on_ready():
    for file in os.listdir('Commands'):
        if file.endswith('.py'):
            bot.load_extension(f'Commands.{file[:-3]}')
    await bot.change_presence(activity=discord.Game("Badmashi na kro\n,help"))
    print("Ready")

@bot.event
async def on_command_error(ctx,error):
    if isinstance(error, commands.errors.CommandNotFound):
        await ctx.send("The command you specified was not found.")

    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You are missing a required argument.")

    elif isinstance(error, commands.errors.MissingPermissions) or isinstance(error, discord.Forbidden):
        await ctx.send("You don't have the permission for that command.")            
@bot.command()
async def ping(ctx):
    await ctx.send('Pong! {0}'.format(round(bot.latency, 1)))
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)        