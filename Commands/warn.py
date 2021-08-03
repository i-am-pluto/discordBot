from PIL import ImageSequence, Image, ImageChops
from discord import member
import requests
from PIL import Image, ImageDraw, ImageOps, ImageFont
import numpy as np
import json
from discord.channel import VoiceChannel
from discord.ext import commands
from discord.ext.commands import has_permissions, CheckFailure
import discord
from discord.utils import get
# import pip
from dotenv import load_dotenv
import asyncio
import os
import json





class warn(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    @commands.command()
    @has_permissions(kick_members=True)
    async def warn(self,ctx, userName: discord.Member, *, reason):
        embed = discord.Embed(title=reason,
                            description="You are being warned", color=0xFF5733)

        try:
            channel = await userName.create_dm()
            await channel.send(embed=embed)
        except:
            await ctx.send(content=f"{userName.mention}", embed=embed)

def setup(bot):
    bot.add_cog(warn(bot))