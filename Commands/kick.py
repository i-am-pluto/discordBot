import discord
import datetime
from discord.ext import commands
import json
import asyncio
from PIL import ImageSequence, Image, ImageChops
# from PIL import gifmaker
# from tkinter import *
# from PIL import ImageTk,Image
import requests
from PIL import Image, ImageDraw, ImageOps, ImageFont
import numpy as np
import os
from discord.ext.commands import has_permissions, CheckFailure

class kick(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    @has_permissions(kick_members=True)
    async def kick(self,ctx, userName: discord.Member, *, reason=None):
        
        f = open(f"Moderation/{ctx.guild.id}.json","r")
        json_object=json.load(f)
        f.close()
        if json_object['kick']==False:
            print("Kick disabled")
            return
        
        
        
        if reason == None:
            reason = "No reason was given..."
        message = reason
        print(1)
        embed = discord.Embed(
            title=f"You have been kicked From **{ctx.guild.name}**", description=reason, color=0xFF5733)
        try:
            channel = await userName.create_dm()
            await channel.send(embed=embed)
            print(2)
        except:
            embed = discord.Embed(description="The user had his dm closed")
            await ctx.send(embed=embed)
            print(2)
        await userName.kick()
        print(3)
        embed = discord.Embed(
            title=f"{userName} has been kicked From **{ctx.guild.name}**", description=reason, color=0xFF5733)
        embed.set_thumbnail(url=userName.avatar_url)
        embed.set_image(
            url="https://media1.tenor.com/images/c0086dbd46e551b5aa1ea42de6960b3b/tenor.gif?itemid=10386441")
        print(4)
        await ctx.send(embed=embed)
        print(5)




def setup(bot):
    bot.add_cog(kick(bot))