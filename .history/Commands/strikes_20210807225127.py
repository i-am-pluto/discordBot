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

class strikes(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    @has_permissions(manage_roles=True)
    async def strike(self,ctx,userName: discord.Member, count:int=1, reason=None):
        
        if reason == None:
            reason = "No reason was given.."
        if userName == ctx.author:
            await ctx.send(embed=discord.Embed(description="You cannot Strike yourself"))    
            return
        print(1)    
        f = open(f"Moderation/{ctx.guild.id}.json","r")
        j = json.load(f)
        if j['strike'] == False:
            print("strikes not enabled")
            return
        print(2)
        f.close()

        f = open(f"strikes/{ctx.guild.id}.json","r")
        print("here")
        j = json.load(f)
        f.close()
        print(3)
        f = open(f"strikes/{ctx.guild.id}.json","w")
        newCount=0
        for i in range (len(j[str(ctx.guild.id)])):
            if j[str(ctx.guild.id)][i]['id']==userName.id:
                j[str(ctx.guild.id)][i]['strike']+=count
                newCount = j[str(ctx.guild.id)][i]['strike']
                break
        
        json.dump(j,f)
        f.close()
        print(4)
        await ctx.send(content = userName.mention,embed=discord.Embed(title=f"{count} Strikes were given to {userName}",description=f"Now the user have {newCount} strikes\n{reason}"))
        print(5)
        try:
            channel = await userName.create_dm()
            await channel.send(content = userName.mention,embed=discord.Embed(title=f"{count} Strikes were given to {userName}",description=f"Now the user have {newCount} strikes\n{reason}"))
        except:
            pass
        # print(1)
        f = open(f"strikes/punishments/{ctx.guild.id}.json","r")
        k = json.load(f)
        c= []
        # print(k)
        # print(2)
        # print(k['p1']['count'])
        for i in range(1,len(k.keys())+1):
            # print("a")
            count = k['p'+str(i)]['count']
            c.append(count)
        # print(3)
        # print(c)
        for i in range(1,len(c)+1,1):
            # print(i,c[i-1],newCount)
            if i==len(c):
                if newCount>=c[i-1]:
                    punishment = k['p'+str(i)]['punishment']
                    if punishment == 'mute':
                        await ctx.invoke(self.bot.get_command('mute'), userName=userName,duration=k['p'+str(i)]['duration'],reason="Strike Punishment")
                    else:
                        await ctx.invoke(self.bot.get_command(punishment), userName=userName,reason="Strike Punishment")     
            elif newCount >= c[i-1] and newCount < c[i]:
                # print("here")
                punishment = k['p'+str(i)]['punishment']
                if punishment == 'mute':
                    await ctx.invoke(self.bot.get_command('mute'), userName=userName,duration=k['p'+str(i)]['duration'],reason="Strike Punishment")
                else:
                    await ctx.invoke(self.bot.get_command(punishment), userName=userName,reason="Strike Punishment")


    @commands.command()
    # @has_permissions(manage_roles=True)        
    async def strikes(self,ctx,userName: discord.Member=None):
        
        f = open(f"Moderation/{ctx.guild.id}.json","r")
        j = json.load(f)
        if j['strike'] == False:
            print("strikes not enabled")
            return

        
        if userName == None:
            userName = ctx.author
        a_file = open(f"strikes/{ctx.guild.id}.json","r")
        print(1)
        json_object = json.load(a_file)
        strikes=0
        for d in json_object[str(ctx.guild.id)]:
            if d['id'] == userName.id:
                strikes= d['strike']
        print(2)
        embed = discord.Embed(title=f"_Strikes_ of {userName}",
                            description=f"the user have {strikes} strikes")
        try:
            f = open(f"strikes/punishments/{ctx.guild.id}.json","r")
            d = json.load(f)
        except:
            pass
        s =""
        # print(2)
        print(3)
        try:
            for i in range(1,len(d.keys())+1):
                # print("D")
                count = d['p'+str(i)]['count']
                punishment = d['p'+str(i)]['punishment']
                duration = -1
                # print("I")
                
                if punishment == 'mute':
                        duration =  d['p'+str(i)]['duration']
                    # print("K")    
                s += str(count) + " = "+ punishment
                if duration != -1:
                        s += " for "+str(duration)+" minutes"
                s+='\n'
        except:
            s="0"        # print("C")
        print(4)    
        embed.add_field(name="Punishments",value=s)          
        await ctx.send(content=ctx.author.mention, embed=embed)
        a_file.close()
    @commands.command()
    @has_permissions(manage_roles=True)
    async def pardon(self,ctx,userName: discord.Member,count:int=1,*,reason=None):
        if reason == None:
            reason = "No reason was given.."
            
        f = open(f"Moderation/{ctx.guild.id}.json","r")
        j = json.load(f)
        if j['strike'] == False:
            print("strikes not enabled")
            return

        f.close()

        f = open(f"strikes/{ctx.guild.id}.json","r")
        j = json.load(f)
        f.close()
        
        t=0
        print("r")
        for i in range(len(j[str(ctx.guild.id)])):
            print(userName.id)
            if (j[str(ctx.guild.id)])[i]['id'] == userName.id:
                t=i

        print("o")
        
        j[str(ctx.guild.id)][t]['strike']-=count
        if j[str(ctx.guild.id)][t]['strike']<0:
            j[str(ctx.guild.id)][t]['strike']=0
        newCount = j[str(ctx.guild.id)][t]['strike']
        print("p")
        f = open(f"strikes/{ctx.guild.id}.json","w")
        json.dump(j,f)
        f.close()
        print("q")
        await ctx.send(content = userName.mention,embed=discord.Embed(title=f"{count} Strikes were pardoned of {userName}",description=f"Now the user have {newCount} strikes\n{reason}"))
        
        try:
            channel = await userName.create_dm()
            await channel.send(content = userName.mention,embed=discord.Embed(title=f"{count} Strikes were pardoned of {userName}",description=f"Now the user have {newCount} strikes\n{reason}"))
        except:
            pass


def setup(bot):
    bot.add_cog(strikes(bot))