from pydoc import describe
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

class mute(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    @has_permissions(manage_roles=True)
    async def mute(self,ctx, userName: discord.Member, duration:int =5, *, reason=None):
        
        # get muted role
        f = open(f"Moderation/{ctx.guild.id}.json","r")
        json_object=json.load(f)
        f.close()
        if json_object['mute']==False:
            print("Mute disabled")
            return
        muted = json_object['muterole_id']
        muted = ctx.guild.get_role(muted)    
        perms = userName.guild_permissions
        if userName == ctx.author:
            await ctx.send(embed=discord.Embed(description="Can't mute yourself retard"))
        if perms.administrator == True:
            return
        if reason == None:
            reason = "No reason Given..."
        try:
            duration = int(duration)*60
        except:
            await ctx.send(content=ctx.author.mention,embed=discord.Embed(description="```<prefix>mute <duration in minutes> <reason>```"))
            return
        embed = discord.Embed()
        embed.title=f"{userName} got muted for {duration/60} minutes in {ctx.guild.name}", description=reason, color=0xFF5733)
        embed.set_thumbnail(url=userName.avatar_url)
        embed.set_image(
            url="https://media.tenor.com/images/9d608d7015ea4284450b35db979f7379/tenor.gif")
        await ctx.send(embed=embed)
        try:
            channel = await userName.create_dm()
            await channel.send(embed=embed)
        except:
            await ctx.send(embed=discord.Embed(description="The user had his dm closed"))
        await ctx.send(muted.mention)
        await userName.add_roles(muted)
        await asyncio.sleep(duration)
        await ctx.invoke(self.bot.get_command('unmute'), userName=userName,reason="Duration Expired")
    
    
    
    @commands.command()
    @has_permissions(manage_roles=True)
    async def unmute(self,ctx,userName:discord.Member,*,reason=None):
        f = open(f"Moderation/{ctx.guild.id}.json","r")
        json_object=json.load(f)
        f.close()
        if json_object['mute']==False:
            print("Mute disabled")
            return
        
        if reason == None:
            reason = "No reason given"
        f = open(f"Moderation/{ctx.guild.id}.json", "r")
        muted = json.load(f)
        muted = ctx.guild.get_role(muted['muterole_id'])
        await userName.remove_roles(muted)
        f.close()
        await ctx.send(f"{userName.mention} was unmuted")
        try:
            channel = await userName.create_dm()
            await channel.send(embed = discord.Embed(title=f"you have been unmuted from {ctx.guild.name}",description=reason))
        except:
            await ctx.send(embed = discord.Embed(description="The user had his dm closed"))
        

def setup(bot):
    bot.add_cog(mute(bot))            