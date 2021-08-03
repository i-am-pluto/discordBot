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

class ban(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    @has_permissions(ban_members=True)
    async def ban(self,ctx, userName: discord.Member, *, reason=None):
        
        f = open(f"Moderation/{ctx.guild.id}.json","r")
        json_object=json.load(f)
        f.close()
        if json_object['ban']==False:
            print("Ban disabled")
            return
        
        
        
        if reason == None:
            reason = "No reason was given..."
        message = reason

        embed = discord.Embed(
            title=f"You have been __**BANNED**__ From **{ctx.guild.name}**", description=reason, color=0xFF5733)
        # embed.set_thumbnail(url=ctx.guild.icon_url)
        try:
            channel = await userName.create_dm()
            await channel.send(embed=embed)
        except:
            embed = discord.Embed(description="The user had his dm closed")
            await ctx.send(embed=embed)
        await userName.ban(reason=reason)
        embed = discord.Embed(
            title=f"{userName} has been **BANNED** From **{ctx.guild.name}**", description=reason, color=0xFF5733)
        embed.set_thumbnail(url=userName.avatar_url)
        embed.set_image(
            url="https://media.tenor.com/images/04c17a71eaecd5db93d22d38184bb73d/tenor.gif")
        await ctx.send(embed=embed)
    @commands.command()
    @has_permissions(ban_members=True)
    async def unban(self,ctx, id: int):
        user = await self.bot.fetch_user(id)
        await ctx.guild.unban(user)
        await ctx.send(embed=discord.Embed(description=f"{user} was unbanned"))    


def setup(bot):
    bot.add_cog(ban(bot))